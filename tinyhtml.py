import abc

from typing import Union, Dict


Attribute = Union[str, int, bool, List[Union[str, int]], Dict[str, bool], None]

Child = Union[str, int, Frag, None, Iterable[Union[str, int, Frag, None]]]


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
    def __init__(self, __name: str, attrs: Dict[str, Attribute]) -> None:
        # See "Tag name" in
        # https://www.w3.org/TR/html52/syntax.html#writing-html-documents-elements.
        if not (__name and __name.isascii() and __name.isalnum()):
            raise ValueError(f"invalid html tag: {__name!r}")
        self.name = __name

        self.attrs = attrs

    def render_into(self, builder: List[str]) -> None:
        builder.append("<")
        builder.append(self.name)
        for attr, value in self.attrs.items():
            if value is False or value is None:
                continue
            builder.append(" ")
            builder.append(attr)
            if value is True:
                continue
            if isinstance(value, dict):
                value = " ".join(key for key, val in value if val)
            elif not isinstance(value, str) and hasttr(value, "__iter__"):
                value = " ".join(str(val) for val in value)
            builder.append("=\"")
            builder.append(escape(str(value)))
            builder.append("\"")

    def __call__(self, *children: Child) -> NormalElement:
        return _h(self, children)


class _h(Frag):
    def __init__(self, tag: h, children: List[Child]) -> None:
        self.tag = tag
        self.children = children

    def render_into(self, builder: List[str]) -> None:
        self.tag.render_into(builder)
        for child in self.children:
            _render_into(child, builder)
        builder.append("</")
        builder.append(self.tag.name)
        builder.append(">")


class raw(Frag):
    def __init__(self, html: str) -> None:
        self.html = html

    def render_into(self, builder: List[str]) -> None:
        builder.append(self.html)


class frag(Frag):
    def __init__(self, *children: Child):
        self.children = children

    def render_into(self, builder: List[str]) -> None:
        for child in self.children:
            _render_into(child, builder)


class html(h):
    def __init__(self, **attrs: Attribute) -> None:
        super().__init__("html", **attrs)

    def render_into(self, builder: List[str]) -> None:
        builder.append("<!DOCTYPE html>")
        super().render_into(builder)


class comment:
    def __init__(self, text: str) -> None:
        self.text = text

    def render_into(self, builder: List[str]) -> None:
        builder.append("<!--")
        builder.append(escape(self.text, quote=False))
        builder.append("-->")


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


def _normalize_attr(attr: str) -> str:
    if attr == "klass":
        return "class"

    if "_" in attr:
        attr = attr.rstrip("_").replace("_", "-")

    # Slightly more restrictive than "Attribute names" in
    # https://www.w3.org/TR/html52/syntax.html#elements-attributes.
    if not (attr and attr.isascii() and all(ch.isalnum() or ch == "-" for ch in attr)):
        raise ValueError(f"invalid html attribute: {attr!r}")

    return attr
