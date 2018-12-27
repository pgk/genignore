===========
genignore
===========

Command line tool that generates ``.gitignore`` files using github's collection
of `gitignore templates <https://github.com/github/gitignore>`_.

Features
========

* syncs with https://github.com/github/gitignore
* You can specify a custom output file other than ``.gitignore``
* Merges contents of existing `.gitignore`


Install
=========

::

    pip install --upgrade genignore

Usage
=========

* Get help: ``genignore --help``
* Grab the latest https://github.com/github/gitignore master: ``genignore sync``
* List available templates: ``genignore list``
* Generate .gitignore for python, osx and linux: ``genignore gen python osx linux``
* Generate .gitignore for python, osx and linux, save it as ``.foo``: ``genignore gen python osx linux --out=.foo``
* To add into an existing .gitignore, use ``genignore gen --add jetbrains``
* You can also redirect stdout ``genignore gen python osx linux > .foo``

Bugs/Features
=============

Open a github issue `here <https://github.com/pgk/genignore/issues>`_.


Contributors
============

* `svisser <https://github.com/svisser>`_.
