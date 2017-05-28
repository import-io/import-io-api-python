#
# Copyright 2017 Import.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from importio2.commands import AdBase
import argparse
import logging
import petl
import pymysql


logger = logging.getLogger(__name__)


class CsvToDatabase(AdBase):

    def __init__(self):
        self._db_user = None
        self._db_password = None
        self._db_database = None
        self._db_host = None
        self._db_table = None
        self._csv_path = None
        self._table = None
        self._create = False
        self._append = False

    def cli_description(self):
        return 'Loads a CSV to specified file in a database'

    def handle_arguments(self):

        parser = argparse.ArgumentParser(description=self.cli_description())

        parser.add_argument('-u', '--user', action='store', dest='db_user', required=True, metavar='user',
                            help='User name to use for authentication to the database')
        parser.add_argument('-p', '--password', action='store', dest='db_password', required=True, metavar='password',
                            help='Password to use for authentication to the database')
        parser.add_argument('-d', '--database', action='store', dest='db_database', required=True, metavar='hostname',
                            help='Database to use')
        parser.add_argument('-i', '--host', action='store', dest='db_host', required=True, metavar='hostname',
                            help='Hostname or IP address of the database')
        parser.add_argument('-t', '--table', action='store', dest='db_table', required=True, metavar='table_name',
                            help='Name of the table to insert the data into')
        parser.add_argument('-f', '--csv-path', action='store', dest='csv_path', required=True, metavar='path',
                            help='Path to CSV file')
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument('-a', '--append', action='store_true', dest='append', help='Flag to append data')
        group.add_argument('-c', '--create', action='store_true', dest='create', help='Flag to create data')

        args = parser.parse_args()

        if 'db_user' in args:
            self._db_user = args.db_user

        if 'db_password' in args:
            self._db_password = args.db_password

        if 'db_database' in args:
            self._db_database = args.db_database

        if 'db_host' in args:
            self._db_host = args.db_host

        if 'db_table' in args:
            self._db_table = args.db_table

        if 'csv_file' in args:
            self._csv_path = args.csv_path

        if 'append' in args:
            self._append = args.append

        if 'create' in args:
            self._create = args.create

    def load_data(self):
        """
        Loads data from CSV into specified database
        :return: None
        """
        table = petl.fromcsv(self._csv_path)
        connection = pymysql.connect(host=self._db_host,
                                     user=self._db_user,
                                     password=self._db_password,
                                     database=self._db_database)
        connection.cursor().execute('SET SQL_MODE=ANSI_QUOTES')

        # If append option is set the add the CSV file to existing table
        if self._append:
            petl.appenddb(table, connection, self._db_table)
        else:
            # Pass in flag that indicates creating the table or replacing the contents
            petl.todb(table, connection, self._db_table, create=self._create)

    def run(self, user, password, database, host, table, csv_path, append=False, create=False):
        """
        Call to perform action to load a CSV file to the database
        :param user: User to authenticate against the database
        :param password: Password to use to authenticate against the database
        :param database: Database to move to after login
        :param host: Location of the database host
        :param table: Table to add CSV file to
        :param csv_path: Path to CSV file to load
        :param append: Flag that indicates to add the data to the existing table
        :param create: Create the table and populate with the CSV data. Error if table already exists
        :return: None
        """
        self._db_user = user
        self._db_password = password
        self._db_database = database
        self._db_host = host
        self._db_table = table
        self._csv_path = csv_path
        self._append = append
        self._create = create

        self.load_data()

    def execute(self):
        """
        Performs the command via the CLI
        :return:
        """
        self.handle_arguments()
        self.load_data()


def main():
    """
    Functioned called by the entry point
    :return:
    """
    o = CsvToDatabase()
    o.execute()


if __name__ == '__main__':
    main()
