"""
Handles the building of python package
"""
from setuptools import setup
from importio2.version import __version__

setup(
    name='importio2',
    version=__version__,
    url='http://github.io/import.io/import-io-api-python',
    author='Andrew Fogg, David Gwartney',
    author_email='david.gwartney@import.io',
    packages=['importio2', ],
    license='LICENSE',
    entry_points={
        'console_scripts': [
            'extractor = importio2.exractor_cli:main',
        ],
    },
    description='Import.io API for Python',
    long_description=open('README.txt').read(),
    install_requires=[
        'requests >= 2.11.1',
        'six>=1.10.0',
    ],
)
