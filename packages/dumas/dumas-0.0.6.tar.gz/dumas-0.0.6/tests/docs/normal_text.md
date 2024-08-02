# This is a dummy text.

should probably test most stuff


```dumas[python@foo]#hidden
#    ///
#    [dumas.interpreter.python.default]
#    base_profile = None
#    split_input_and_output = True
#    input_render_language = "python"
#    output_render_language = "markdown"
#    \\\
assert False
```


```dumas[python@foo]?black=true&name=my_cell_name
#    ///
#    [dumas.interpreter.python.default]
#    base_profile = None
#    split_input_and_output = True 
#    show
#    input_render_language = "python"
#    output_render_language = "markdown"
#    
#    [dumas.interpreter.python.cell]
#    base_profile = hidden
#    apply_black = False 
#    \\\
assert False
```


```dumas[python@foo]#assert
#    ///
#    [dumas.interpreter.python.default]
#    split_input_and_output = True 
#    show
#    input_render_language = "python"
#    output_render_language = "markdown"
#    
#    [dumas.interpreter.python.cell]
#    apply_black = False 
#    \\\
assert False
```

```dumas[python@foo]#test
assert False
```

```dumas[podman@some]
ls -ll /
```

```dumas[config]
[dumas.interpreter.podman.centos8]
base_image = "centos/centos8"
```