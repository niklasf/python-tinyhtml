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
