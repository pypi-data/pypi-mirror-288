# Interpreters

Dumas interpreters are the thing that runs dumas, try to imagine them as jupyter kernels, but much simpler (and less safe).

The way you use them is by using a **fenced code block** with a dumas string as the language, the string has the following shape 

```markdown

\```dumas[python]
1+1
\``` 

```

This will render that particular **fenced code block** as using the python interpreter, each interpreter is unique to a particular document (values on one document does not bleed into another document), and in general shared between the cells, this means that what ever you do on one cell (import a library, assign a variable, define a function), can then be used on another cell, for instance, the following code is valid.

```markdown

\```dumas[python]
x = 1
\``` 


\```dumas[python]
x + 41
\```

```

you can have isolation by specifying a `interpreter_id`, thats just any string that you put after the language prefixed by an @ symbol... you can have as many inrpreters as you like, and if you dont specify an interpreter, the default interpreter is used

```python
# set x in interpreter one using this code
# 
#   ```dumas[python@one]
#   x = 1
#   ``` 

In [1]: x = 1
```

```python
# set x in interpreter two using this code
# 
#   ```dumas[python@two]
#   x = 2
#   ``` 

In [1]: x = 2
```

```python
# Using x defined for interpreter one as x=1 here to get 42
# 
#   ```dumas[python@one]
#   x + 41
#   ``` 

In [2]: x + 41


Out[2]: 42
```

```python
# Using x defined for interpreter two as x=2 here to get 42 but from adding 40 instead of 41
# 
#   ```dumas[python@one]
#   x + 40
#   ``` 

In [2]: x + 40


Out[2]: 42
```

# configuring interpreters

Each interpreter has a configuration that can be alter at the file level, or at the cell level. There are multiple ways of configuring the interpreters, because i could not decide on a single one, i'll explain them here from easier to more complex.

## predefined configurations

Each interpreter comes with at least one predefined configuration, `default`, then they bring a few extra confiuration that they deem usefull. you access this by adding a `#config_name` to the language, this example would use the "hidden config" (what that config does is particular to the python interpreter, and you can read about it more later, but in a nutshell it does not display the content of the cell), by calling the language `dumas[python]#hidden`



```python
#  we have a  
#  
#    ```dumas[python]#hidden
#    from pathlib import Path
#    tmpdir = Path("/tmp")
#    ```
#
#   ```dumas[python]
#   tmpdir / "new_file.txt"
#   ```
# 

In [1]: tmpdir / "new_file.txt"


Out[1]: /tmp/new_file.txt
```

even though the block with the `#hidden` fragment was executed (as evidenced that the variable `tmpdir` is defined), the content wont be displaed, and the execution count is not increased.

## changing specific config options

In the context of a cell, you might want to change only some configs, or maybe you want to use a predefined confif but want to change a single config option... you can do this by using a query string (like in a url), the following are two examples

```markdown

\```dumas[python]?apply_black=false
x = [1,2,3,4,]
\```


\```dumas[python@new-int]?increase_execution_count=true#hidden
x = [1,2,3,4,]
\```

```

The first example uses the default config, but will not reformat your code to apply black in the input. and the second uses the hidden config profile, but it will overwrite the  `increase_execution_count` to actually add 1.

```python
# Using apply_black=false will disable black for this cell.
#
#    ```dumas[python]?apply_black=false
#    x = [1,2,3,4,]
#    ```

In [1]: x = [1,2,3,4,]
```

without ignore black the array would look like

```python
#    ```dumas[python]
#    x = [1,2,3,4,]
#    ```

In [2]: x = [
   ...:     1,
   ...:     2,
   ...:     3,
   ...:     4,
   ...: ]
```

# Python

# Extending