#!/usr/bin/env python

import os.path
import setuptools

setuptools.setup(
    name="tinyhtml",
    version="1.2.0",  # Remember to update version in __init__.py and changelog
    author="Niklas Fiekas",
    author_email="niklas.fiekas@backscattering.de",
    description="A tiny library to safely render compact HTML5 from Python expressions.",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    long_description_content_type="text/x-rst",
    license="MIT/Apache-2.0",
    license_files=["LICENSE-APACHE", "LICENSE-MIT"],
    keywords="html html5 vdom functional-programming",
    url="https://github.com/niklasf/python-tinyhtml",
    packages=["tinyhtml"],
    zip_safe=False,  # For mypy
    package_data={
        "tinyhtml": ["py.typed"],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Typing :: Typed",
    ],
)
