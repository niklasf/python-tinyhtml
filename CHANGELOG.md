Chanelog for tinyhtml
=====================

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
