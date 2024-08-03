#!/bin/env python3

"""Textual user interface for managing the results."""

import argparse
import math
from collections import defaultdict
from typing import Optional

import urwid as uw
from urwid.command_map import Command

from ..models import Format, Result, create_db_session


class SText(uw.Text):
    """A selectable Text widget."""

    _selectable = True

    def keypress(self, size, key):
        """Don't do anything on keypress."""
        return key


class SimpleButton(uw.Button):
    """Button widget with simpler decoration."""

    button_left = uw.Text("*")
    button_right = uw.Text(" ")
    format: Optional[Format] = None


def parse_cli_args():
    """Parse the CLI arguments for resultman."""
    # parsing CLI arguments
    parser = argparse.ArgumentParser(
        description="TUI tool for managing file format information"
    )
    parser.add_argument(
        "--invenio-domain",
        default="researchdata.tuwien.ac.at",
        help="domain name of the repository for building links",
    )
    return parser.parse_args()


def run_resultman_cli():
    """Run the resultman CLI command."""
    run_resultman(parse_cli_args())


def run_resultman(config):
    """Run resultman with the given config."""

    # helper functions
    def fallback_key_handler(key: str) -> None:
        """Handle keys that haven't been handled by any widgets."""
        if key == "Q":
            raise uw.ExitMainLoop()

        elif key in ["q", "h", "esc"]:
            # ideally these keys would be handled by the right side when it's focused
            # as this action only makes sense then
            columns.set_focus(left)

    # TODO make configurable
    session = create_db_session("sqlite:///db.sqlite")

    # loading formats & results
    formats = []
    try:
        formats = session.query(Format).all()
    except Exception as e:
        print(e)

    # color palette & settings: (name, fg, bg)
    palette = [
        ("border", "light gray,bold", "dark gray"),
        ("bold", "bold", ""),
        ("darkbg", "", "black"),
        ("reversed", "bold,standout", ""),
        # styling for formats based on risk
        ("vlr", "black", "dark green"),
        ("lr", "light green", "black"),
        ("mr", "black", "yellow"),
        ("hr", "white", "dark red"),
        ("vhr", "black,bold", "dark red"),
    ]

    uw.command_map["j"] = Command.DOWN
    uw.command_map["k"] = Command.UP
    uw.command_map["ctrl d"] = Command.PAGE_DOWN
    uw.command_map["ctrl u"] = Command.PAGE_UP

    PRONOM_BASE_URL = "https://www.nationalarchives.gov.uk/PRONOM/%(puid)s"
    REPOSITORY_BASE_URL = f"https://{config.invenio_domain}/records/%(recid)s"

    # event handlers
    def handle_select_format(format: Format, button: uw.Button):
        """Set up the format details side (right) based on the selected format."""
        results = (
            session.query(Result)
            .filter(Result.format_id == format.id)
            .order_by(Result.record, Result.filename)
            .all()
        )
        relevant_results = defaultdict(list)
        for res in results:
            relevant_results[res.record].append(res)

        content = []
        i, num_files = 0, 0
        for rec, results in relevant_results.items():
            i += 1
            repository_url = REPOSITORY_BASE_URL % {"recid": rec}
            content.append(uw.Filler(uw.Text([f"  {i}) ", ("bold", repository_url)])))

            for res in results:
                try:
                    if res.risk == 0:
                        attribute = None
                    else:
                        # min: 1×1=1, max: 5×5=25
                        risk = int(res.risk / 5)
                        attribute = ["vlr", "lr", "mr", "hr", "vhr"][risk]
                except IndexError:
                    attribute = "vhr"

                content.append(
                    uw.AttrMap(
                        SText(["    * ", res.filename], wrap="any"),
                        attribute,
                        focus_map="reversed",
                    )
                )
            content.append(uw.Divider())
            num_files += len(results)

        bottom = uw.SolidFill(".")
        if relevant_results:
            _files = "file" if num_files == 1 else "files"
            _records = "record" if len(relevant_results) == 1 else "records"
            bottom = uw.ScrollBar(
                uw.ListBox(
                    uw.SimpleFocusListWalker(
                        [
                            uw.Divider(),
                            uw.AttrMap(
                                uw.Text(
                                    f"  {num_files:,} {_files} in "
                                    f"{len(relevant_results):,} {_records}:"
                                ),
                                None,
                                focus_map="reversed",
                            ),
                            uw.Divider(),
                            *content,
                        ]
                    )
                )
            )

        pronom_url = PRONOM_BASE_URL % {"puid": format.puid}
        format_header = uw.Pile(
            [
                uw.Filler(uw.Divider()),
                uw.Filler(uw.Text(["  Name:   ", format.name or "-"])),
                uw.Filler(uw.Text(["  MIME:   ", format.mime or "-"])),
                uw.Filler(uw.Text(["  PRONOM: ", pronom_url])),
                uw.Filler(uw.Divider()),
            ]
        )

        format_details = uw.Pile(
            [
                ("pack", format_header),
                ("pack", uw.AttrMap(uw.Filler(uw.Divider()), "border")),
                bottom,
            ]
        )

        right.contents.pop()
        right.contents.append((format_details, ("weight", 1)))

        # if the details side has actual content to display, focus it
        # columns: contains the format list (left) and the format details (right)
        # right: has the format info header, divider, and files list
        if relevant_results:
            columns.set_focus(right)
            right.set_focus(format_details)

    # defining the basic layout
    def create_format_buttons():
        format_buttons = []
        max_len_results = max([len(f.results) for f in formats]) if formats else 0
        max_num_files = math.ceil(math.log10(max_len_results) if max_len_results else 0)

        for format in sorted(formats, key=lambda f: f.name or ""):
            try:
                attribute = [None, "vlr", "lr", "mr", "hr", "vhr"][format.risk]
            except IndexError:
                attribute = "vhr"

            prefix = str(len(format.results)).rjust(max_num_files)
            button = SimpleButton(f"[{prefix}] {format.name or '[UNKNOWN]'}")
            button.format = format
            uw.connect_signal(button, "click", handle_select_format, user_args=[format])
            format_buttons.append(uw.AttrMap(button, attribute, focus_map="reversed"))

        return format_buttons

    content = create_format_buttons() or [uw.Text("No formats available")]
    formats_list = uw.ScrollBar(uw.ListBox(uw.SimpleFocusListWalker(content)))
    formats_list._command_map["l"] = "activate"
    formats_label = uw.Filler(uw.AttrMap(uw.Text("FORMATS", align="center"), "border"))
    left = uw.Pile([("pack", formats_label), formats_list])

    num_res, num_fmts = session.query(Result).count(), session.query(Format).count()
    help_text = f"""
    Formatscaper results manager help

    +---------------------------------------------------------------+
    | Up/Down/j/k/^d/^u:   navigate up and down                     |
    | Enter/Space/l:       select current format                    |
    | Esc/h/q:             go back to formats list                  |
    | Q/^c:                quit with/without saving changes         |
    +---------------------------------------------------------------+

    Loaded {num_res:,} results for {num_fmts:,} formats
    """
    details = uw.AttrMap(uw.Filler(uw.Text(help_text, align="center")), "darkbg")
    details_label = uw.Filler(uw.AttrMap(uw.Text("DETAILS", align="center"), "border"))
    right = uw.Pile([("pack", details_label), details])

    div = uw.AttrMap(uw.SolidFill(" "), "border")
    columns = uw.Columns([("weight", 1, left), (1, div), ("weight", 2, right)])

    info = uw.Text(f"Showing {len(formats)} formats")
    status_line = uw.Filler(uw.AttrMap(info, "border"))
    top = uw.Pile([uw.AttrMap(columns, "darkbg"), ("pack", status_line)])

    loop = uw.MainLoop(top, palette, unhandled_input=fallback_key_handler)

    try:
        loop.run()
        if session.dirty:
            session.commit()

    except KeyboardInterrupt:
        loop.stop()


if __name__ == "__main__":
    run_resultman()
