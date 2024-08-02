import textwrap

from dumas.lib.renderer import render_text


def test_empty_text_render():
    assert render_text("") == ""


def test_some_text_render():
    assert render_text("some text") == "some text"


def test_some_text_with_end_line_render():
    assert render_text("some text\n") == "some text\n"


def test_render_no_code_render():
    test_text = textwrap.dedent(
        """
        This is a regular MD
        ====================

        with some `funny text` and some text

        ```dumas[python@readme]
        x = 1+1

        x**2

        ```"""
    )
    result_text = textwrap.dedent(
        """
        # This is a regular MD

        with some `funny text` and some text

        ```python

        In [1]: x = 1 + 1
           ...: 
           ...: x**2


        Out[1]: 4
        ```"""
    )
    assert render_text(test_text) == result_text
