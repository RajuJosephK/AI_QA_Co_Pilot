# from readers.reader_factory import read_file
import os
from src.readers.reader_factory import read_file


def test_factory_txt(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("Test 123")

    assert read_file(str(file)) == "Test 123"
