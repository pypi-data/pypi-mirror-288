#! /usr/bin/env python

from setuptools import setup, find_packages

vers = "0.0.0.942"

setup(
    name="extvip",
    version=vers,
    description="Extvip // @antilagvip",
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    packages=find_packages(exclude=["tests"]),
    author="@antilagvip",
    url=f"http://pypi.python.org/pypi/extvip",
    author_email="dev@antilag.dev",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    project_urls={
        "Homepage": "https://github.com/antilagg/extvip",
        "Suggestions": "https://github.com/antilagg/extvip/issues",
    },
    python_requires="~=3.8",
    install_requires=[
        "colorama>=0.4.6", 
        "requests>=2.30.0"
    ],
)
