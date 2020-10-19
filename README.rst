tinyhtml
========

... code:: python

    >>> from tinyhtml import html, h, frag, raw

    >>> html(lang="en")(
    ...     h("head")(
    ...         h("meta", charset="utf-8"),
    ...     ),
    ... )
    raw('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"></head></html>')

    >>> raw("<!--")
    raw('<!--')

    >>> frag(
    ...     h("h1")("Lorem ipsum ..."),
    ...     h("p")("... dolor sit amet."),
    ... )
    raw('<h1>Lorem ipsum ...</h1><p>... dolor sit amet.</p>')
