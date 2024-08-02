import re
import urllib.parse
from pathlib import Path

from marko import Markdown, block
from marko.md_renderer import MarkdownRenderer

from dumas.lib.interpreters import interpreters, get_interpreter_instance

FENCED_CODE_LANG_REGEX = re.compile(
    r"dumas\[(?P<interpreter_name>[\d\w_]+)(@(?P<interpreter_id>[\w\d_-]+))?\](?P<extra>(#|\?).+)?"
)


class RenderError(Exception):
    def __init__(self, msg, element, raw, error):
        super().__init__(msg)
        self.element = element
        self.raw = raw
        self.error = error


class Renderer(MarkdownRenderer):
    namespace = "default"

    def __init__(self) -> None:
        super().__init__()

    def render_fenced_code(self, element: block.FencedCode) -> str:
        match = FENCED_CODE_LANG_REGEX.match(element.lang)

        if not match:
            return super().render_fenced_code(element)

        match_dict = match.groupdict()
        interpreter_id = match_dict.get("interpreter_id") or "default"
        interpreter_name = match_dict["interpreter_name"]

        extra = urllib.parse.urlparse(match_dict.get("extra", ""))

        interpreter = get_interpreter_instance(interpreter_name, namespace=self.namespace, interpreter_id=interpreter_id)

        try:
            qs = {
                k: v[0] if v and v[0] else None
                for k, v in urllib.parse.parse_qs(extra.query or "", keep_blank_values=True).items()
            }
            config = interpreter.get_config_with(extra.fragment or "default", qs)
        except KeyError as e:
            raw = super().render_fenced_code(element)
            msg = f"Can't find config profile `{extra.fragment}` to process element \n{raw}"
            raise RenderError(msg, element, raw=raw, error=e) from e

        if extra.query:
            config = config.new_with({
                k: v[0] if v and v[0] else None
                for k, v in urllib.parse.parse_qs(extra.query, keep_blank_values=True).items()
            })
            

        try:

            result = [self.render(r) for r in interpreter.run(self.render_raw_text(element.children[0]), config=config)]
        except AssertionError as e:
            raw = super().render_fenced_code(element)
            msg = f"[AssertionError] when process element \n{raw}\n -- \n"
            import traceback

            msg += "\n--\n".join(traceback.format_exception(e)[-2:])
            raise RenderError(msg, element, raw=raw, error=e) from e
        except Exception as e:
            raw = super().render_fenced_code(element)
            msg = f'error "[{e.__class__.__name__}] {e}" process element \n{raw}'
            raise RenderError(msg, element, raw=raw, error=e) from e

        return "".join(result)


def renderer(namespace):
    return type("Renderer", (Renderer,), {"namespace": namespace})


def render_text(text: str, *, renderer: Renderer | None = Renderer) -> str:
    rendered_text = Markdown(renderer=renderer)(text)
    if text and text[-1] != "\n":
        rendered_text = rendered_text[:-1]
    return rendered_text


def render_file(path_to_file: Path, *, renderer: Renderer | None = None) -> str:
    try:
        renderer = renderer or type("Renderer", (Renderer,), {"namespace": f"{path_to_file}"})
        return render_text(path_to_file.read_text(), renderer=renderer)
    except RenderError as e:
        msg = f"Error \"[{e.error.__class__.__name__}] {e.error}\" when processing file {path_to_file}'s element \n{e.raw}"
        raise RenderError(msg, element=e.element, raw=e.raw, error=e.error) from None
