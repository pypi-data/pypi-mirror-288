"""Utility functions for handling formats and results."""

import pickle
import re
import sys
from typing import Dict, List, Optional

import yaml

from .models import Format, RecordFile, Result


def load_record_files(file_name: str) -> List[None]:
    """Load the record files from the file with the given name.

    If ``file_name`` is ``"-"``, then standard in will be read.
    """
    record_files = []
    if file_name == "-":
        record_files = yaml.safe_load(sys.stdin)
    else:
        with open(file_name, "r") as input_file:
            record_files = yaml.safe_load(input_file)

    return [RecordFile(**rf) for rf in record_files or []]


def load_formats(file_name: str) -> Dict[str, Format]:
    """Load the known formats from the given YAML file."""
    formats = {}

    try:
        with open(file_name, "r") as formats_file:
            known_formats = yaml.safe_load(formats_file)
            for f in known_formats:
                format = Format(**f)
                formats[format.puid] = format

    except FileNotFoundError:
        pass

    return formats


def store_formats(formats: Dict[str, Format] | List[Format], file_name: str) -> bool:
    """Store the known formats to the given YAML file."""
    try:
        if isinstance(formats, dict):
            formats = formats.values()

        updated_formats = [f.as_dict() for f in formats]
        with open(file_name, "w") as formats_file:
            yaml.dump(updated_formats, formats_file, sort_keys=False)

    except OSError:
        print(
            f"ERROR: couldn't update the formats file ({file_name})",
            file=sys.stderr,
        )


def store_results(results: List[Result], file_name: str, file_format: str) -> bool:
    """Store the results in the specified file.

    The ``file_name`` can contain ``"{FORMAT}``, which will be replaced by the
    specified ``file_format``.
    The latter has to be either ``yaml`` or ``pickle``.
    """
    try:
        file_name = file_name.format(FORMAT=file_format)
        simple_results = [res.as_dict() for res in results]
        file_mode = "w" if file_format == "yaml" else "wb"
        with open(file_name, file_mode) as output_file:
            if file_format.lower() == "yaml":
                yaml.dump(simple_results, output_file, sort_keys=False)
            elif file_format.lower() == "pickle":
                pickle.dump(simple_results, output_file)
            else:
                print(
                    f"WARN: unknown format for results file ({file_format})",
                    file=sys.stderr,
                )
                return False

        return True

    except OSError:
        print(
            f"WARN: couldn't store the results to file ({file_name})",
            file=sys.stderr,
        )
        return False


def load_results(
    file_name: str,
    file_format: Optional[str] = None,
    strict: bool = True,
    formats: Optional[List[Format]] = None,
) -> Optional[List[Result]]:
    """Load the results from the given file.

    In case the ``file_format`` isn't specified, auto-detection is attempted.
    If ``strict`` is set, then the result loading will fail if it cannot parse
    the format for a result.
    Optionally, a list of already known ``formats`` can be supplied to avoid
    creating duplicate ``Format`` instances.
    Newly encountered formats will be appended to the supplied list.
    """
    if file_format is None:
        if re.search(r"\.ya?ml$", file_name, re.IGNORECASE):
            file_format = "yaml"
        elif re.search(r"\.pickle$", file_name, re.IGNORECASE):
            file_format = "pickle"

    if file_format not in {"pickle", "yaml"}:
        print(f"WARN: invalid file format ({file_format})", file=sys.stderr)
        return None

    raw_results = []
    if file_format == "pickle":
        with open(file_name, "rb") as results_file:
            raw_results = pickle.load(results_file)
    elif file_format == "yaml":
        with open(file_name, "r") as results_file:
            raw_results = yaml.safe_load(results_file)

    # note: we deduplicate formats so that manipulation of one entry updates all entries
    results = []
    formats = formats or []
    known_formats = {format.puid: format for format in formats}

    for res in raw_results:
        format = None
        try:
            format = known_formats.get(res["format"]["puid"], None)
            if format is None:
                format = Format(**res["format"])
                known_formats[format.puid] = format
                formats.append(format)
        except (TypeError, KeyError) as e:
            # TypeError: the result doesn't have all required parts for Format()
            # KeyError:  either the result doesn't have a format or it lacks the PUID
            if strict:
                raise e

        res.pop("format", None)
        result = Result(**res, format=format)
        format.results.append(result)
        results.append(result)

    return results
