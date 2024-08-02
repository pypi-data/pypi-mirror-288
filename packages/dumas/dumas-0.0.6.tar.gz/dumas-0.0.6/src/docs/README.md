# dumas

[![PyPI - Version](https://img.shields.io/pypi/v/dumas.svg)](https://pypi.org/project/dumas)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dumas.svg)](https://pypi.org/project/dumas)

* * *

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install dumas
```

## Using it (prepare your doc)

Using dumas on any markdown file will leave the file almost unchanged, 
we use [marko](https://github.com/frostming/marko) under the hood
and marko is opinionated on what gets output from a markdown document. 
But the power of dumas start when you use the dumas blocks,
right now there is only the "**dumas fenced code block**" (the one with the backticks). Just add to your document this

```markdown

\```dumas[python]
a = 1
def foo(o):
   return 2**o

foo(a+1)

\```

```

and this will turn the content into an ipython (jupyter notebook) cell.

## Using it (cli)

then execute:

```shell
$ dumas render-file example.md
```

and this will output to stdout:

```python

In [1]: a = 1
   ...: 
   ...: 
   ...: def foo(o):
   ...:     return 2**o
   ...: 
   ...: 
   ...: foo(a + 1)


Out[1]: 4
```

you can write to specific file

```shell
$ dumas render-file example.md --output-file  /tmp/myfile.md
```

or render the entire files of a dir into another

```shell
$ dumas render-dir docs/ --output-dir  publish/
```

## Using it (api)

You could use `dumas` as part of your own workflow/program

```dumas[python]
# First import the render functions

import textwrap
from dumas.lib.renderer import render_text, render_file


MD_TEXT = textwrap.dedent(
        """
        This is a regular MD
        ====================
        
        with some `funny text` and some text
        
        ```dumas[python@readme]
        x = 1+1
        
        x**2
        
        ```
    """
)

MD_TEXT

```

```dumas[python]
render_text(MD_TEXT)
```

# Interpreters

dumas comes with a python interpreter, I plan to expand interpreters as I need them.

# Contributing and a usage warning

Yes please, but not a lot... I'nm the only one mantaining this project, I'm mostly making it for me, and i want to be able to change
the interfaces without breaking the world, please 

## License

`dumas` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
