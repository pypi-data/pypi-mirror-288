import textwrap

from dumas.lib.renderer import render_text, renderer


def test_hidden_config():
    input_text = """
    ```dumas[python] 

    assert isinstance(__dumas_config__, __dumas_interpreter__.Config) , "__dumas_config__ is not an instance of Config"
    assert __dumas_interpreter__.interpreter_id == 'default', \
        f"non default interpreter id {__dumas_interpreter__.interpreter_id}"
    ```
    """

    render_text(textwrap.dedent(input_text), renderer=renderer(namespace=f"{__file__}.{test_hidden_config}"))
