from __future__ import annotations

import abc
from html import escape

from typing import Union, Dict, Iterable


class Frag(abc.ABC):
    @abc.abstractmethod
    def render_into(self, builder: List[str]) -> None:
        ...

    def render(self) -> str:
        return render(self)

    _repr_html_ = __str__ = render

    def __repr__(self) -> str:
        return f"raw({self.render()!r})"


SupportsFrag = Union[str, int, Frag, None, Iterable[Union[str, int, Frag, None]]]


def render_into(frag: SupportsFrag, builder: List[str]) -> None:
    if frag is None:
        return
    elif isinstance(frag, str):
        builder.append(escape(frag, quote=False))
    elif isinstance(frag, Frag):
        frag.render_into(builder)
    elif hasattr(frag, "__iter__"):
        for c in frag:
            render_into(c, builder)
    else:
        builder.append(escape(str(frag), quote=False))


def render(frag: SupportsFrag) -> str:
    builder: List[str] = []
    render_into(frag, builder)
    return "".join(builder)


Attribute = Union[str, int, bool, Iterable[Union[str, int]], Dict[str, bool], None]


class h(Frag):
    def __init__(self, __name: str, **attrs: Attribute) -> None:
        # See "Tag name" in
        # https://www.w3.org/TR/html52/syntax.html#writing-html-documents-elements.
        if not (__name and __name.isascii() and __name.isalnum()):
            raise ValueError(f"invalid html tag: {__name!r}")
        self.name = __name

        self.attrs = {_normalize_attr(attr): value for attr, value in attrs.items()}

    def render_into(self, builder: List[str]) -> None:
        builder.append("<")
        builder.append(self.name)
        for attr, value in self.attrs.items():
            if value is False or value is None:
                # Falsy boolean attributes are omitted altogether:
                # https://www.w3.org/TR/html52/infrastructure.html#sec-boolean-attributes
                continue

            builder.append(" ")
            builder.append(attr)

            if value is True:
                # Use the empty string as the value for truthy boolean
                # attributes:
                # https://www.w3.org/TR/html52/infrastructure.html#sec-boolean-attributes
                value = ""
            elif isinstance(value, dict):
                value = " ".join(key for key, val in value.items() if val)
            elif not isinstance(value, str) and hasattr(value, "__iter__"):
                value = " ".join(str(val) for val in value)
            else:
                value = str(value)

            # Attribute value syntax:
            # https://www.w3.org/TR/html52/syntax.html#elements-attributes
            if not value:
                # If the value is an empty string, use empty attribute syntax.
                continue
            elif value.isalnum() and value.isascii():
                # Conservatively use unquoted attribute value syntax.
                builder.append("=")
                builder.append(value)
            else:
                # Double-quoted attribute value syntax. No need to escape
                # single quotes, as quote=True would do:
                # https://github.com/python/cpython/blob/v3.9.0/Lib/html/__init__.py#L12-L25
                builder.append("=\"")
                builder.append(escape(value, quote=False).replace("\"", "&quot;"))
                builder.append("\"")
        builder.append(">")

    def __call__(self, *children: SupportsFrag) -> _h:
        return _h(self, children)


class _h(Frag):
    def __init__(self, tag: h, children: List[SupportsFrag]) -> None:
        self.tag = tag
        self.children = children

    def render_into(self, builder: List[str]) -> None:
        self.tag.render_into(builder)
        for child in self.children:
            render_into(child, builder)
        builder.append("</")
        builder.append(self.tag.name)
        builder.append(">")


class raw(Frag):
    def __init__(self, html: str) -> None:
        self.html = html

    def render_into(self, builder: List[str]) -> None:
        builder.append(self.html)


class frag(Frag):
    def __init__(self, *children: SupportsFrag):
        self.children = children

    def render_into(self, builder: List[str]) -> None:
        for child in self.children:
            render_into(child, builder)


class html(h):
    def __init__(self, **attrs: Attribute) -> None:
        super().__init__("html", **attrs)

    def render_into(self, builder: List[str]) -> None:
        builder.append("<!DOCTYPE html>")
        super().render_into(builder)


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
