#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

# RELEASE STEPS
# $ python setup.py bdist_wheel
# $ python twine upload dist/VX.Y.Z.whl
# $ git tag -a VX.Y.Z -m "release version VX.Y.Z"
# $ git push origin VX.Y.Z

NAME = "keybasechat"
VERSION = "0.0.1"
URL = "https://github.com/eternal-flame-AD/keybase-chat-api"
AUTHOR = "eternal_flame-AD"
AUTHOR_EMAIL = "ef@eternalflame.cn"
LICENSE = "Apache 2.0"
REQUIRES = ["syncer"]
DESC = "keybase chat api wrapper"
PYTHON_REQUIRES = ">=3.5.3"
CLASSIFIERS = [
    "License :: OSI Approved :: Apache Software License",
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Development Status :: 2 - Pre-Alpha",
    "Operating System :: POSIX",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
]


setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    name=NAME,
    version=VERSION,
    license=LICENSE,
    install_requires=REQUIRES,
    url=URL,
    packages=['keybasechat'],
    package_dir={'keybasechat':'keybasechat'},
    description=DESC,
    python_requires=PYTHON_REQUIRES,
    classifiers=CLASSIFIERS,
)