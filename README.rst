===========
genignore
===========

A command line tool that generates .gitignore files using github's collection 
of `gitignore templates <https://github.com/github/gitignore>`_.

Install
=========

::

    pip install --upgrade genignore
  
Usage
=========

After installation it is possible to use the tool like this::

    usage: genignore [-h] [-o OUT] [--sync] [--update] N [N ...]

	positional arguments:
	  N                  Name(s) of things to include to the .gitignore

	optional arguments:
	  -h, --help         show this help message and exit
	  -o OUT, --out OUT  file to output the generated gitignore (default
	                     .gitignore of pwd)
	  --sync             sync to latest templates (requires internet connection)
	  --update           update the file if it exists, keeping custom entries

  
