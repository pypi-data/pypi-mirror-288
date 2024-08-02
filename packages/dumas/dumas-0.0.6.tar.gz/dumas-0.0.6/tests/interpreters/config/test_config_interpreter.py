
def test_config_change_config(render_text):
    text = """
Sets new configs

```dumas[config@int1]

[dumas.interpreter.python.config.config1]
apply_black=false
split_render=true

[dumas.interpreter.python.config.config2]
extends="config1"
apply_black=true
split_render=true

[dumas.interpreter.python.config.config3]
extends="config2"

```

check configs are applied
```dumas[python@int1]#config1
assert __dumas_interpreter__.interpreter_id == "int1", __dumas_interpreter__.instance_id
assert __dumas_config__.apply_black == False, __dumas_config__
assert __dumas_config__.split_render, __dumas_config__
```

```dumas[python@int1]#config2
assert __dumas_interpreter__.interpreter_id == "int1", __dumas_interpreter__.instance_id
assert __dumas_config__.apply_black, __dumas_config__
assert __dumas_config__.split_render, __dumas_config__
```


```dumas[python@int1]?apply_black=false#config3
assert __dumas_config__.apply_black == False, __dumas_config__
```

```dumas[python@int1]#config3
assert __dumas_config__.apply_black, __dumas_config__
```

    """

    render_text(text=text)