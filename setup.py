import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "genignore",
    version = "0.2.5",
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
