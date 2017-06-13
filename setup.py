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
    packages=['importio2', 'importio2/commands'],
    license='LICENSE',
    entry_points={
        'console_scripts': [
            'extractor = importio2.extractor_cli:main',
            'io-change-ownership = importio2.commands.change_ownership:main',
            'io-csv-download = importio2.commands.csv_download:main',
            'io-create-crawl-run = importio2.commands.create_crawl_run:main',
            'io-csv-to-crawl-run = importio2.commands.csv_to_crawl_run:main',
            'io-csv-to-db = importio2.commands.csv_to_db:main',
            'io-csv-to-json = importio2.commands.csv_to_json:main',
            'io-date-to-epoch = importio2.commands.date_to_epoch:main',
            'io-json-to-crawl-run = importio2.commands.json_to_crawl_run:main',
            'io-run-sql = importio2.commands.run_sql:main',
            'io-sql-to-csv = importio2.commands.sql_to_csv:main',
            'io-upload = importio2.commands.upload:main',
        ],
    },
    description='Import.io API for Python',
    long_description=open('README.txt').read(),
    install_requires=[
        'requests >= 2.11.1',
        'six>=1.10.0',
        'python-dateutil>=2.6.0',
        'petl>=1.1.1',
        'pytz>=2017.2',
        'PyMySQL>=0.7.11',

    ],
)
