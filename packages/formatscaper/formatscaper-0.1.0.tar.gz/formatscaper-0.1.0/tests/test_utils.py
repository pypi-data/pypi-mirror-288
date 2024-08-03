"""Testing the utility functions."""

import os
import tempfile

import yaml

from formatscaper.models import Format, RecordFile
from formatscaper.utils import load_formats, load_record_files, store_formats


def test_load_record_files_from_yaml():
    """Test loading of record files."""
    record_files = load_record_files("tests/data/test_record_files.yml")
    assert len(record_files) > 1

    for record_file in record_files:
        assert isinstance(record_file, RecordFile)


def test_load_formats():
    """Test loading of formats."""
    formats = load_formats("tests/data/test_formats.yml")
    assert len(formats) > 1

    for format in formats.values():
        assert isinstance(format, Format)
        assert 0 <= format.risk <= 5


def test_store_formats():
    """Test storing of formats."""
    formats = [
        Format(puid="x-fmt/111", name="Plain Text File", mime="text/plain", risk=1),
        Format(puid="fmt/615", name="Gimp Image File Format", mime=None, risk=3),
        Format(puid="UNKNOWN", name=None, mime=None, risk=5),
    ]

    try:
        filename = tempfile.mktemp(suffix=".yml")
        store_formats(formats, filename)
        with open(filename, "r") as f:
            result = yaml.safe_load(f)

        assert len(result) == len(formats)
        for format in formats:
            assert format.as_dict() in result

    finally:
        os.remove(filename)
