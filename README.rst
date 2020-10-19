tinyhtml
========

Introduction
------------

This is the entire API.

.. code:: python

    >>> from tinyhtml import html, h, frag, raw

The most important function is ``h()``. Below you see how to render attributes,
normal elements and void/self-closing elements.

.. code:: python

    >>> html(lang="en")(
    ...     h("head")(
    ...         h("meta", charset="utf-8"),
    ...     ),
    ... )
    raw('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"></head></html>')

Use ``frag()`` to pass around concatenated elements.

.. code:: python

    >>> frag(
    ...     h("h1")("Lorem ipsum ..."),
    ...     h("p")("... dolor sit amet."),
    ... )
    raw('<h1>Lorem ipsum ...</h1><p>... dolor sit amet.</p>')

Of course all attributes and content is properly escaped. Use ``raw()`` as an
escape catch to render unescaped HTML.

.. code:: python

    >>> raw("<!--").render()
    raw('<!--')

Features and patterns
---------------------

* Supports Python 3.7+.

* Includes mypy typings.

* Write templates as functions.

  .. code:: python

      >>> from tinyhtml import Frag

      >>> def layout(title: str, body: Frag) -> Frag:
      ...     return html(
      ...        h("head")(
      ...            h("title")(title),
      ...        ),
      ...        h("body")(body)
      ...     )
      ...
      ... layout("Hello world", frag(
      ...     h("h1")("Hello world"),
      ...     h("p")("Lorem ipsum dolor sit amet."),
      ... )
      raw('<!DOCTYPE html><html><head><title>Hello world</title></head><body>Lorem ipsum dolor sit amet</body></html>')
