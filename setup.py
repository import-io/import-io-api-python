from distutils.core import setup
from importio.version import __version__

setup(
    name='importio',
    version=__version__,
    url='http://github.io/import.io/import-io-api-python',
    author='Andrew Fogg, David Gwartney',
    author_email='andrew.fogg@import.io, david.gwartney@import.io',
    packages=['importio', ],
    license='LICENSE',
    entry_points={
        'console_scripts': [
            'tsp-etl = tspetl.etl_cli:main',
         ],
    },
    description='Import.io API for Python',
    long_description=open('README.txt').read(),
    install_requires=[
       'requests >= 2.11.1',
    ],
)
