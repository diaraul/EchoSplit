import os
import re

import pytest


@pytest.fixture(scope="module")
def file():
    mydir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.realpath(os.path.join(mydir, "static"))
    vocab_html = os.path.join(templates_dir, "js/calc.js")
    with open(vocab_html, "r") as file:
        file_content = file.read()
    return file_content


def test_check_uses_getJSON(file):
    getjson_pattern = r"\$\.getJSON"
    has_getjson = re.findall(getjson_pattern, file, re.MULTILINE)
    assert has_getjson, "No jQuery getJSON function found in js/calc.js"


def test_check_uses_jquery(file):
    jquery_pattern = r"\$\(.*\)"
    has_jquery = re.findall(jquery_pattern, file, re.MULTILINE)
    assert has_jquery, "No jQuery found in js/calc.js"
