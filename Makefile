.PHONY: test publish

test:
	python -m mypy --strict tinyhtml
	python -m doctest README.rst
	flake8 tinyhtml setup.py

publish:
	rm -rf build dist tinyhtml.egg-info
	python setup.py --long-description | rst2html --strict --no-raw > /dev/null
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --skip-existing --sign dist/*
