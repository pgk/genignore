===========
genignore
===========

A command line tool that generates ``.gitignore`` files using github's collection 
of `gitignore templates <https://github.com/github/gitignore>`_.

Features
========

* sync with remote functionality
* You can specify a custom output file other that ``.gitignore``
* Can keep and combine the contents of any existing .gitignore file


Install
=========

::

    pip install --upgrade genignore
  
Usage
=========

* To sync the templates with github, use ``genignore sync``
* To generate a .gitignore for python, osx and linux, use ``genignore gen python osx linux``
* To generate a .gitignore for python, osx and linux and save it as ``.foo``, use ``genignore gen python osx linux --out=.foo``
* To list available templates, run ``genignore list``
* Get help with ``genignore --help``

  
Bugs/Features
=============

Feel free to open a github issue `here <https://github.com/pgk/genignore/issues>`_.


Contributors
============

* `svisser <https://github.com/svisser>`_.
