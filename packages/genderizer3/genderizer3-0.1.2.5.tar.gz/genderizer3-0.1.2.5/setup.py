#!/usr/bin/env python

try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup


setup(
    name="genderizer3",
    version="0.1.2.5",
    license="MIT",
    description="Genderizer tries to infer gender information looking at first name and/or making text analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # Change this if your README is in Markdown
    packages=["genderizer3"],
    package_data={"genderizer3": ["data/*"]},
    platforms="any",
)
