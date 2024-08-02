import textwrap



def test_hidden_config(render_text):
    input_text = textwrap.dedent(
        """
        ```dumas[python]#hidden
        x=42
        ```
        ```dumas[python]
        x
        ```
        """
    )
    output_text = textwrap.dedent(
        """

        ```python

        In [1]: x

        
        Out[1]: 42
        ```
        """
    )
    assert render_text(input_text) == output_text


def test_disable_black(render_text):
    input_text = textwrap.dedent(
        """
        ```dumas[python@test_disable_black]?apply_black=false
        x = [1,2,3,4,]
        ```
        """
    )
    output_text = textwrap.dedent(
        """
        ```python
    
        In [1]: x = [1,2,3,4,]
        ```
        """
    )
    assert render_text(input_text) == output_text


def test_still_counts_on_hidden(render_text):
    input_text = textwrap.dedent(
        """
        ```dumas[python@new-int]?increase_execution_count=true#hidden
        x = [1,2,3,4,]
        ```

        ```dumas[python@new-int]
        x
        ```
        """
    )
    output_text = textwrap.dedent(
        """


        ```python

        In [2]: x
    
        
        Out[2]: [1, 2, 3, 4]
        ```
        """
    )
    assert render_text(input_text) == output_text
