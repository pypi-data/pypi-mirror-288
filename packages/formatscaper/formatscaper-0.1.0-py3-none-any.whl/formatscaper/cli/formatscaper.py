#!/bin/env python3

"""The file format identification command for formatscaper."""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading

import progressbar as pb
import yaml

from ..models import Format, RecordFile, Result, create_db_session
from ..utils import load_record_files

completed_tasks = 0


def parse_cli_args():
    """Run the formatscaper command."""
    # set up the argument parser
    parser = argparse.ArgumentParser(
        description=(
            "Tool for identifying the formats of listed files (and nested ones "
            "in case of archives) associated to records uploaded in Invenio."
        ),
    )
    parser.add_argument(
        "--input",
        "-i",
        default="-",
        help="input file for files of per record to check (default: stdin)",
    )
    parser.add_argument(
        "--parallel",
        "-p",
        default=1,
        type=int,
        help=(
            "number of siegfried processes to run in parallel; 0 and negative numbers "
            "will subtract from the number of CPU cores (default: 1)"
        ),
    )
    parser.add_argument(
        "--sf-binary",
        default="sf",
        help="name of the siegfried binary to call (default: sf)",
    )
    parser.add_argument(
        "--sf-error-log",
        default="sf.log",
        help="file in which to store sf error logs (default: sf.log)",
    )
    parser.add_argument(
        "--no-progressbar",
        "-B",
        default=False,
        action="store_true",
        help="disable the progress bar",
    )
    parser.add_argument(
        "--tempdir",
        "-t",
        default=None,
        help="set directory for storing temporary files",
    )
    return parser.parse_args()


def scape_formats(config):
    """Run formatscaper."""
    # TODO make configurable
    session = create_db_session("sqlite:///db.sqlite")

    # check the siegfried binary
    try:
        sf_output = subprocess.check_output([config.sf_binary, "-v"], text=True)
        m = re.match(r"siegfried ((\d+\.?)+)", sf_output)
        if m and m.group(1):
            ver_nums = [int(num) for num in m.group(1).split(".")]
            if not (ver_nums[0] >= 1 and ver_nums[1] >= 11):
                print(
                    f"WARN: siegfried version too old ({m.group(1)})", file=sys.stderr
                )
        else:
            print("ERROR: siegfried version could not be determined", file=sys.stderr)
            sys.exit(1)
    except FileNotFoundError:
        print(
            f"ERROR: siegfried binary could not be found ({config.sf_binary})",
            file=sys.stderr,
        )
        sys.exit(1)

    # read the list of files to analyze
    record_files = load_record_files(config.input)

    # try to redirect the error logs from siegfried
    try:
        sf_error_log = open(config.sf_error_log, "w")
    except OSError as e:
        print(
            f"WARN: couldn't open sf log file, printing to stderr instead ({e})",
            file=sys.stderr,
        )
        sf_error_log = None

    # determine the level of threads to run in parallel
    # negative numbers mean "this much less than the number of CPUs I have",
    # as long as the result is greater than 0
    if (num_threads := config.parallel) <= 0:
        num_cores = os.cpu_count()
        if num_cores is None:
            num_threads = 1
            print(
                (
                    "WARN: couldn't determine number of CPU cores, "
                    "falling back to a single thread"
                ),
                file=sys.stderr,
            )
        else:
            num_threads = os.cpu_count() + num_threads
            if num_threads <= 0:
                print(
                    "ERROR: calculated number of threads would be less than 1:",
                    num_threads,
                    file=sys.stderr,
                )
                sys.exit(1)

    # progressbar curates its own list of ANSI terminals, and doesn't know about foot,
    # so we claim to use xterm instead of foot
    if os.environ.get("TERM") == "foot":
        os.environ["TERM"] = "xterm"

    # set the directory for storing temporary files
    if config.tempdir:
        if os.path.exists(config.tempdir):
            os.environ["TMPDIR"] = os.environ["TMP"] = config.tempdir
        else:
            print(
                "WARN: ignoring tempdir as it does not exist:",
                config.tempdir,
                file=sys.stderr,
            )

    # set up variables required in the collection of results
    sem = threading.Semaphore(num_threads)
    mutex = threading.Lock()
    pb_ws = [
        pb.Percentage(),
        " (",
        pb.SimpleProgress(),
        ") ",
        pb.Bar(),
        " ",
        pb.Timer(),
    ]
    progress_bar = pb.ProgressBar(max_value=len(record_files), widgets=pb_ws)
    base_dir = tempfile.mkdtemp()

    def process_record_file(record_file: RecordFile) -> None:
        with sem:
            # link the files under investigation into a scoped directory
            file_dir = os.path.join(base_dir, record_file.record)
            file_path = os.path.join(file_dir, record_file.filename)

            try:
                # if we already have an overridden result for the record file
                # in question, we skip it
                overridden_result = (
                    session.query(Result)
                    .filter(
                        Result.record == record_file.record,
                        Result.filename == record_file.filename,
                        Result.overridden.is_(True),
                    )
                    .one_or_none()
                )

                if overridden_result is not None:
                    file_infos = []

                else:
                    # create a symlink to the file with a proper name to help siegfried
                    # with file format identification as the file name plays a role
                    # (this will be deleted afterwards)
                    os.makedirs(file_dir, exist_ok=True)
                    os.symlink(record_file.uri, file_path)

                    sf_output = subprocess.check_output(
                        [
                            config.sf_binary,
                            "-sym",
                            "-z",
                            "-multi",
                            "1",
                            "-name",
                            record_file.filename,
                            file_path,
                        ],
                        stderr=sf_error_log,
                    )

                    # skip the sf info part
                    file_infos = yaml.safe_load_all(sf_output)
                    next(file_infos)

                # go through all the files analyzed by siegfried which can be several,
                # if the original input file was an archive
                for file_info in file_infos:
                    if not file_info.get("errors") and file_info.get("matches", []):
                        for match in file_info["matches"]:
                            if match["ns"] == "pronom":

                                # evaluate result in mutex to avoid race conditions
                                with mutex:
                                    # retrieve or add the format
                                    format = (
                                        session.query(Format)
                                        .filter(Format.puid == match["id"])
                                        .one_or_none()
                                    )
                                    if format is None:
                                        format = Format.from_sf_dict(match)
                                        session.add(format)

                                    # replace first occurrence of the URI with filename
                                    filename = file_info["filename"].replace(
                                        (file_dir + os.path.sep), "", 1
                                    )

                                    result = Result(
                                        filename=filename,
                                        record=record_file.record,
                                        format=format,
                                    )

                                    # check if we claim to know better than siegfried
                                    session.add(result)

                # when the task ends, update the progress bar
                with mutex:
                    global completed_tasks
                    completed_tasks += 1
                    if not config.no_progressbar:
                        progress_bar.update(completed_tasks, force=True)

            except (subprocess.CalledProcessError, ValueError) as e:
                print("WARN: error during sf execution:", str(e), file=sys.stderr)

            finally:
                try:
                    # in any case, remove the symlink to the file we generated
                    os.remove(file_path)
                except FileNotFoundError:
                    pass

    # analyze all files in parallel, and create the summary after all threads complete
    threads = []
    for record_file in record_files or []:
        thread = threading.Thread(target=process_record_file, args=[record_file])
        threads.append(thread)
        thread.start()

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        pass

    # clean up
    shutil.rmtree(base_dir)
    if sf_error_log is not None:
        sf_error_log.close()

    # write new results to disk
    session.commit()


def run_formatscaper_cli():
    """Run the formatscaper CLI command."""
    scape_formats(parse_cli_args())


if __name__ == "__main__":
    run_formatscaper_cli()
