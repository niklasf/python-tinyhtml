from typing import Union, Dict


Attribute = Union[str, int, bool, Dict[str, bool], None]

Child = Union[str, int, Frag, None, List[Union[str, int, Frag, None, int]]]


class Frag:
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


def comment(Frag):
    def __init__(self, __text: str) -> None:
        self.text = __text

    def render_into(self, builder: List[str]) -> None:
        builder.append("<!--")
        builder.append(html.escape(self.text))
        builder.append("-->")


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



def html(*children: Child) -> Frag:
    return frag(raw("<!DOCTYPE html>"), h("html")(*children))
