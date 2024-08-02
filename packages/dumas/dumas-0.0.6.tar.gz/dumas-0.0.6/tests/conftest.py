import pytest
from functools import wraps

from dumas.lib.renderer import render_text as _render_text, renderer
from uuid import uuid4

@pytest.fixture
def render_text(request):

    @wraps(_render_text)
    def inner(text):
        return _render_text(text=text, renderer=renderer(namespace=f"{uuid4()}"))
    
    return inner
