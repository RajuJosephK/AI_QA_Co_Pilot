# from ..src.readers.txt_reader import read_txt   

from src.readers.txt_reader import read_txt


import os

def test_read_txt(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("Hello World")

    content = read_txt(str(test_file))

    assert content == "Hello World"
