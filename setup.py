#!/usr/bin/env python

from setuptools import setup
import breakdown

version = ".".join(map(str, breakdown.VERSION))

try:
    longdesc = open("README.rst").read()
except Exception:
    longdesc = (
        "Breakdown is a lightweight python webserver that parses "
        "jinja2 templates. It's intended to be used by designers "
        "in rapid prototyping."
    )

setup(
    # Metadata
    name="breakdown",
    version=version,
    description="Lightweight jinja2 template prototyping server",
    long_description=longdesc,
    author="Concentric Sky",
    author_email="code@concentricsky.com",
    classifiers=[
        "Environment :: Console",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Framework :: Django",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    install_requires=["jinja2>=2.6", "clevercss", "six"],
    dependency_links=[
        'https://github.com/clevercss/clevercss/archive/master.zip#egg=clevercss'
    ],
    # Program data
    scripts=["scripts/breakdown"],
    packages=["breakdown"],
    package_data={"breakdown": ["img/*", "templates/*"]},
)
