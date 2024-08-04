#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module contains the build information for this project
"""
import setuptools

from borb.license.version import Version

# open readme
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# requirements
required = [
    "cryptography>=37.0.4",     # license handling
    "fonttools>=4.22.1",        # TTF fonts
    "lxml>=4.9.1",              # XML processing
    "Pillow>=7.1.0",            # image processing
    "python-barcode>=0.13.1",   # generating barcodes
    "qrcode[pil]>=6.1",         # generating QR codes
    "requests>=2.24.0",         # generating images from a URL
    "setuptools>=51.1.1",       # standard
]

setuptools.setup(
    name="borb",
    version=Version.get_version(),
    author=Version.get_author(),
    author_email="joris.schellekens.1989@gmail.com",
    description="borb is a library for reading, creating and manipulating PDF files in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorisschellekens/borb",
    packages=setuptools.find_packages(include=["borb", "borb.*"]),
    include_package_data=True,
    install_requires=required,
    python_requires=">=3.6",
)
