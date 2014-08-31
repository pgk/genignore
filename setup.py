from setuptools import setup, find_packages

setup(
    name = "genignore",
    version = "0.2.2",
    url="https://pypi.python.org/pypi/genignore",
    packages = find_packages(),
    author="Panos Kountanis",
    author_email="panosktn@gmail.com",
    description="Generate gitignore files based on templates provided by github",
    long_description="""\
=========
genignore
=========

Command line tool that generates .gitignore files based on templates provided by github

Install the latest with `pip install --upgrade genignore`

    """,
    entry_points = {
        'console_scripts': [
            'genignore = genignore.genignore:main_func'
        ]
    },
    install_requires = ['requests>=2.3.0'],
)