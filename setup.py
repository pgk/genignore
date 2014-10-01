import os
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as file_handle:
        return file_handle.read()


setup(
    name = "genignore",
    version = "0.3.0",
    url="https://pypi.python.org/pypi/genignore",
    packages = find_packages(),
    author="Panos Kountanis",
    author_email="panosktn@gmail.com",
    description="Generate gitignore files based on templates provided by github",
    long_description=read("README.rst"),
    entry_points = {
        'console_scripts': [
            'genignore = genignore.genignore:main_func'
        ]
    },
    install_requires = [
        'requests>=2.3.0',
        'clint>=0.3.7'
    ],
    setup_requires= [
        'nose>=1.0',
        'mock'
    ]
)
