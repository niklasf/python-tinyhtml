tinyhtml
========

A tiny library to safely render compact HTML5 from Python expressions.

.. image:: https://github.com/niklasf/python-tinyhtml/workflows/Test/badge.svg
    :target: https://github.com/niklasf/python-tinyhtml/actions
    :alt: Test status

.. image:: https://badge.fury.io/py/tinyhtml.svg
    :target: https://pypi.python.org/pypi/tinyhtml
    :alt: PyPI package

Introduction
------------

This is the entire API. The following documentation is longer than the
implementation.

.. code:: python

    >>> from tinyhtml import html, h, frag, raw

The most important function is ``h()``. Below you see how to render attributes,
normal elements, and void/self-closing elements.

.. code:: python

    >>> html(lang="en")(
    ...     h("head")(
    ...         h("meta", charset="utf-8"),
    ...     ),
    ... ).render()
    '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"></head></html>'

Use ``frag()`` to pass around groups of elements.

.. code:: python

    >>> frag(
    ...     h("h1")("Lorem ipsum ..."),
    ...     h("p")("... dolor sit amet."),
    ... )
    raw('<h1>Lorem ipsum ...</h1><p>... dolor sit amet.</p>')

Of course all content and attributes are properly escaped. Use ``raw()`` as an
escape hatch to render unescaped HTML.

.. code:: python

    >>> print(h("a", title="&<>\"'")("&<>\"'").render())
    <a title="&amp;&lt;&gt;&quot;'">&amp;&lt;&gt;"'</a>

    >>> print(raw("<!-- 💥"))
    <!-- 💥


Installing
----------

::

    pip install tinyhtml


Features and patterns
---------------------

* Output is compact: Naturally produces no superfluous whitespace between
  elements.

* Fragments provide ``_repr_html_()`` for Jupyter notebook integration and
  ``__html__`` for integration with other ecosystems (see
  `MarkupSafe <https://markupsafe.palletsprojects.com/en/stable/html/>`_).

* Fragments can include and render objects providing ``_repr_html_()`` and
  ``__html__()``. This means objects that already render as HTML in a
  Jupyter notebook will be rendered by tinyhtml.

* Includes mypy typings.

  .. code:: python

      >>> from tinyhtml import Frag

* Write **templates** as functions.

  .. code:: python

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
      ... ))
      raw('<!DOCTYPE html><html><head><title>Hello world</title></head><body><h1>Hello world</h1><p>Lorem ipsum dolor sit amet.</p></body></html>')

* Use ``str``, ``int``, other fragments, ``None``, or iterables of these as
  **child elements**. (Note that rendering consumes the iterables, so fragments
  using generators can be rendered only once.)

  .. code:: python

      >>> h("ul")(
      ...     h("li")(n) for n in range(3)
      ... )
      raw('<ul><li>0</li><li>1</li><li>2</li></ul>')

      >>> h("ul")(
      ...     h("li")("Foo") if False else None,
      ...     h("li")("Bar"),
      ... )
      raw('<ul><li>Bar</li></ul>')

* Use ``str``, ``int``, ``None``, iterables of these, ``bool``, or dictionaries
  with boolean values as **attributes**.

  .. code:: python

      >>> h("input", type="checkbox", checked=True, disabled=False)
      raw('<input type="checkbox" checked>')

      >>> h("body", klass=["a", "b"])()
      raw('<body class="a b"></body>')

      >>> h("body", klass={
      ...    "a": True,
      ...    "b": False,
      ... })()
      raw('<body class="a"></body>')


* Use ``klass`` instead of ``class``, append a trailing underscore (``for_``),
  or use underscores instead of dashes (``http_equiv``) for attribute names
  that cannot be Python identifiers.

  .. code:: python

      >>> h("div", klass="container")()
      raw('<div class="container"></div>')

      >>> h("label", for_="name")("Name")
      raw('<label for="name">Name</label>')

      >>> h("meta", http_equiv="refresh", content=10)
      raw('<meta http-equiv="refresh" content="10">')

* Render fragments as ``str``, or into a list of ``str`` for efficient string
  building.

  .. code:: python

      >>> frag("Hello world", "!").render()
      'Hello world!'

      >>> builder = []
      >>> frag("Hello world", "!").render_into(builder)
      >>> builder
      ['Hello world', '!']
      >>> "".join(builder)
      'Hello world!'

* Does not support comment nodes, unescapable raw text elements
  (like inline styles and scripts), or foreign elements (like inline SVG).
  Instead, reference external files, or use ``raw()`` with appropriate caution.


Interoperability
----------------

Fragments implement ``_repr_html_`` and can be displayed in Jupyter notebooks
as HTML, but they can also render object that implement ``_repr_html_``.
Similarly fragments can include and be included in other template systems that
use the ``__html__`` convention, such as Jinja2 via
`MarkupSafe`_.

* Render fragments into a Jinja2 template.

  .. code:: python

      >>> import jinja2
      >>> template = jinja2.Template('<div>{{ fragment }}</div>')
      >>> frag = h('ul')(h('li')(i) for i in range(2))
      >>> template.render(fragment=frag)
      '<div><ul><li>0</li><li>1</li></ul></div>'


* Render an object the supports display in a Jupyter notebook, such as a pandas
  dataframe.

  .. code:: python

      >>> import pandas as pd
      >>> table = pd.DataFrame({'Fruit': ['apple', 'pear'], 'Count': [3, 4]})
      >>> h('div')(h('h1')('A table'), table) # doctest: +ELLIPSIS
      raw('<div><h1>A table</h1><div>...<table ...>...<td>apple</td>...</table>...</div>')


License
-------

Licensed under the
`Apache License, Version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_,
or the `MIT license <https://opensource.org/licenses/MIT>`_, at your option.
