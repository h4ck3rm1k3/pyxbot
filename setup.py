import os
from setuptools import setup, find_packages

setup(
    name = "osmbot",
    version = "0.0.1",
    description = ("Python OSM bot derived from xybot"),
    author = "James Michael DuPont, derived from emacsen's bot",
    author_email = "jamesmikedupont+osm@gmail.com",
    url = "https://github.com/h4ck3rm1k3/xybot",
    packages = ["osmbot"],
    install_requires = ['quadpy==0.1'],
    dependency_links = ['git://github.com/h4ck3rm1k3/quadpy.git#egg=quadpy-0.1'],
    scripts=["scripts/dup_houses.py","scripts/katebot.py"],
)
