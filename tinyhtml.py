import abc

from typing import Union, Dict


Attribute = Union[str, int, bool, Dict[str, bool], None]

Child = Union[str, int, Frag, None, Iterable[Union[str, int, Frag, None]]]


def _render_into(child: Child, builder: List[str]) -> None:
    if child is None:
        return
    elif isinstance(child, str):
        builder.append(html.escape(child, quote=False))
    elif isinstance(child, Frag):
        child.render_into(frag)
    elif hasttr(child, "__iter__"):
        for c in child:
            _render_into(c, builder)
    else:
        builder.append(html.escape(str(child), quote=False))


class Frag(abc.ABC):
    @abc.abstractmethod
    def render_into(self, builder: List[str]) -> None:
        ...

    def render(self) -> str:
        builder: List[str] = []
        self.render_into(builder)
        return "".join(builder)

    _repr_html_ = __str__ = render

    def __repr__(self) -> str:
        return f"raw({self.render()!r})"


class h(Frag):
    def __init__(self, __name: str, **attrs: Attribute):
        self.name = __name
        self.attrs = attrs

    def __call__(self, *arg: Child):
        return _h(self, arg)


class raw(Frag):
    def __init__(self, html: str) -> None:
        self.html = html

    def render_into(self, builder: List[str]) -> None:
        builder.append(self.html)


class frag(Frag):
    def __init__(self, *children: Child):
        self.children = children

    def render_into(self, builder: List[str]) -> None:
        for child in children:


def comment(text: str) -> Frag:
    return frag(raw("<!--"), raw(html.escape(text)), raw("-->"))


def html(*children: Child) -> Frag:
    return frag(raw("<!DOCTYPE html>"), h("html")(*children))
