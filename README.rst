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
    ... ).render()
    '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"></head></html>'

Use ``frag()`` to pass around concatenated elements.

.. code:: python

    >>> frag(
    ...     h("h1")("Lorem ipsum ..."),
    ...     h("p")("... dolor sit amet."),
    ... ).render()
    '<h1>Lorem ipsum ...</h1><p>... dolor sit amet.</p>'

Of course all attributes and content is properly escaped. Use ``raw()`` as an
escape hatch to render unescaped HTML.

.. code:: python

    >>> raw("<!--").render()
    '<!--'

Features and patterns
---------------------

* Supports Python 3.7+.

* Includes mypy typings.

* Write templates as functions.

  .. code:: python

      >>> from tinyhtml import Frag

      >>> def layout(title: str, body: Frag) -> Frag:
      ...     return html()(
      ...        h("head")(
      ...            h("title")(title),
      ...        ),
      ...        h("body")(body)
      ...     )

      >>> layout("Hello world", frag(
      ...     h("h1")("Hello world"),
      ...     h("p")("Lorem ipsum dolor sit amet."),
      ... )).render()
      '<!DOCTYPE html><html><head><title>Hello world</title></head><body><h1>Hello world</h1><p>Lorem ipsum dolor sit amet.</p></body></html>'

* Use ``klass``, append a trailing underscore (`for_`), and underscores instead
  of dashes (``http_equiv``) to refer to attribute names.

  .. code:: python

      >>> h("div", klass="container")()
      raw('<div class="container"></div>')

      >>> h("label", for_="name")("Name")
      raw('<label for="name">Name</label>')

      >>> h("meta", http_equiv="refresh", content=10)
      raw('<meta http-equiv="refresh" content="10">')
