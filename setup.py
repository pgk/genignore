from setuptools import setup, find_packages

setup(
    name = "genignore",
    version = "0.1",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'genignore = genignore.genignore:main_func'
        ]
    },
    install_requires = ['requests>=2.3.0'],
)