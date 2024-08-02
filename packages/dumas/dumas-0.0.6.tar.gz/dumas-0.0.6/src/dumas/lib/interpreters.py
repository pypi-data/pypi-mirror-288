from __future__ import annotations

import re
import textwrap
import urllib.parse
from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Dict, Type, Any

import libcst as cst
import tomllib
from black import Mode as black_Mode
from black import format_str
from IPython.core.interactiveshell import InteractiveShell
from marko.block import BlankLine, FencedCode
from pydantic import BaseModel


class ConfigModel(BaseModel): 
    def new_with(self, qsd):
            new_conf = self.model_validate(qsd)
            return self.model_copy(update=new_conf.model_dump(include=qsd.keys()))
            


class Interpreter:

    class Config(ConfigModel): ...

    base_config_profiles: dict[str, Config] = {"default": Config()}

    @classmethod
    @lru_cache
    def get_instance(cls, namespace: str, interpreter_id: str) -> "Interpreter":
        return cls(namespace=namespace, interpreter_id=interpreter_id)

    def __init__(self, namespace: str, interpreter_id: str) -> None:
        self.namespace = namespace
        self.interpreter_id = interpreter_id
        self.config_profiles = self.base_config_profiles.copy()
    
    def get_config(self, config_name: str) -> Config:
        return self.config_profiles[config_name]

    def get_config_with(self, config_name:str , qsd: None | dict[str, Any]) -> Config:
        conf = self.config_profiles[config_name]
        return conf.new_with(qsd) if qsd else conf
    
    def set_config(self, name, config):
        self.config_profiles[name] = config



    @property
    def instance_id(self):
        return f"{self.namespace}.{self.interpreter_id}"


class Config(Interpreter):

    class Config(ConfigModel): ...

    base_config_profiles: dict[str, Config] = {"default": Config()}

    def run(self, code: str, config: _Config | None = None):
        assert config is None or config is self.config_profiles["default"], "you cant pass a config to a config object"

        config = tomllib.loads(code)
        dumas_config = config.get("dumas", config.get("tools", {}).get("dumas", {}))
        interpreter_config = dumas_config.get("interpreter", {})
        for interpreter, configs in interpreter_config.items():
            interpreter_instance = get_interpreter_instance(interpreter, self.namespace, self.interpreter_id)
            for config_name, new_config in configs.get("config", {}).items():
                interpreter_instance.set_config(
                    config_name, interpreter_instance.get_config_with(config.pop("extends", "default"), new_config)
                )

        yield BlankLine(0)


class Python(Interpreter):
    language = "python"

    class Config(ConfigModel):
        apply_black: bool = True
        increase_execution_count: bool = True

        # how to hide stuff
        render: bool = True  # if this is False nothing is render, if true then
        split_render: bool = False
        render_input: bool = True
        render_output: bool = True

    base_config_profiles: dict[str, Config] = {
        "default": Config(),
        "hidden": Config(
            increase_execution_count=False,
            render=False,
        ),
    }

    def __init__(self, namespace: str, interpreter_id: str) -> None:
        super().__init__(namespace=namespace, interpreter_id=interpreter_id)
        self.shell = InteractiveShell()

    def run(self, code, config: Python.Config | None = None):
        config = config or self.config_profiles["default"]

        execution_count = self.shell.execution_count

        self.shell.user_ns.update(
            {
                "__dumas_config__": config,
                "__dumas_interpreter__": self,
            }
        )

        out = self.shell.run_cell(code)
        out.raise_error()

        if config.increase_execution_count:
            self.shell.execution_count += 1

        if not config.render:
            yield BlankLine(0)
            return

        in_ps1 = f"In [{execution_count}]: "
        len_in_ps1 = len(in_ps1)
        indent_ps1 = " " * (len_in_ps1 - (1 + 3 + 1)) + "...: "

        out_ps1 = f"Out[{execution_count}]: "

        if out.success:
            if out.result:
                result = f"\n\n{out_ps1}{out.result}"
            else:
                result = ""
        else:
            result = f"{out_ps1}\n{out.error_in_exec.__repr__()}"

        module = cst.parse_module(code)

        header = module.with_changes(body=[]).code
        body = module.with_changes(header=[]).code.strip()
        if config.apply_black:
            body = format_str(body, mode=black_Mode())

        render_body = in_ps1 + textwrap.indent(body, prefix=indent_ps1, predicate=lambda _: True)[len_in_ps1:]

        pattern = r"^```"
        # Replacement string
        replacement = r"\\```"
        # Use re.sub() to replace the matches
        content = re.sub(pattern, replacement, f"{header}{render_body}{result}", flags=re.MULTILINE)

        yield FencedCode(("python", "", content))


interpreters: Dict[str, Type[Interpreter]] = {"python": Python, "config": Config}


def get_interpreter(name:str) -> Type[Interpreter]:
    return interpreters[name]

def get_interpreter_instance(name, namespace:str, interpreter_id:str) -> Interpreter:
    return get_interpreter(name).get_instance(namespace=namespace, interpreter_id=interpreter_id)