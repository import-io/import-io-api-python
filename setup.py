"""
Handles the building of python package
"""
from setuptools import setup
from distutils.util import convert_path

PACKAGE_NAME = 'importio2'

main_ns = {}
version_path = convert_path(PACKAGE_NAME + '/version.py')
with open(version_path) as version_file:
        exec(version_file.read(), main_ns)

setup(
    name=PACKAGE_NAME,
    version=main_ns['__version__'],
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
        'python-dateutil>=2.6.0',
    ],
)
