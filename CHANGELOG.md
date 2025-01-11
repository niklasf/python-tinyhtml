Chanelog for tinyhtml
=====================

New in v1.3.0
-------------

* Now supports interoperability with Jupyter (`_repr_html_`) and MarkupSafe
  (`__html__`) in both directions.

New in v1.2.0
-------------

* Stop eliding attribute quotes. The barely noticable file size improvements
  can flip when using compression (especially Brotli, with its dictionary
  built from sites using mostly quoted attributes).

New in v1.1.0
-------------

* Empty list and dictionary attriutes will now be omitted entirely.
  Example:

  ```python
  >>> h("div", klass={
  ...    "active": False,
  ... })()
  raw('<div></div>')
  ```

New in v1.0.0
-------------

First stable release.
