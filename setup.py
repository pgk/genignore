from setuptools import setup, find_packages

setup(
    name = "genignore",
    version = "0.2.1",
    url="https://pypi.python.org/pypi/genignore",
    packages = find_packages(),
    author="Panos Kountanis",
    author_email="panosktn@gmail.com",
    short_description="Generate gitignore files based on templates provided by github",
    long_description="""\
=========
genignore
=========

Generate gitignore files based on templates provided by github

    """,
    entry_points = {
        'console_scripts': [
            'genignore = genignore.genignore:main_func'
        ]
    },
    install_requires = ['requests>=2.3.0'],
)