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

from importio2.commands import AdDatabase
import petl
import pymysql
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class SqlToCsv(AdDatabase):
    def __init__(self):
        super(AdDatabase, self).__init__()
        self._connection = None
        self._sql = None
        self._sql_file = None
        self._db_user = None
        self._db_password = None
        self._db_database = None
        self._db_host = None

    def handle_arguments(self):
        """
        Adds the required argument handlers for this CLI
        :return:
        """
        self.add_file_output_path_arg(required=True)
        group = self._parser.add_mutually_exclusive_group(required=True)

        group.add_argument('--sql', action='store', metavar='sql', required=False,
                           help="SQL statement to run to populate CSV file")
        group.add_argument('--sql-file', action='store', metavar='sql_file', required=False,
                           help="SQL statement to run to populate CSV file")

        super(SqlToCsv, self).handle_arguments()

        self._args = self._parser.parse_args()

        self.get_arguments()

    def get_arguments(self):
        """
        Fetches the parsed arguments required by the CLI
        :return:
        """
        super(SqlToCsv, self).get_arguments()

        if 'sql' in self._args:
            self._sql = self._args.sql

        if 'sql_file' in self._args:
            self._sql_file = self._args.sql_file

    def sql_to_csv(self):
        """
        Execute SQL statement and writes output to a CSV file
        :return: None
        """

        logger.info("user: {0}, password: {1}, host: {2}, database: {3}".format(
                    self._db_user, self._db_password, self._db_host, self._db_database))

        connection = pymysql.connect(user=self._db_user,
                                     password=self._db_password,
                                     host=self._db_host,
                                     database=self._db_database)
        table = petl.fromdb(connection, self._sql)
        petl.tocsv(table, self._output_path)

    def run(self, user, password, database, host, sql_input, output_path):
        """
        Programmatic action to issue a SQL statement against the database and return
        :param user: User to use to authentication against the database
        :param password: Password to use to authentication against the database
        :param database: Which database to make current for the query
        :param host: Location of the database either hostname or IP address
        :param sql_input: Ether a bare SQL statement or path to file containing SQL if the path exists
        :param output_path: Path to write output from database query
        :return:
        """
        self._db_user = user
        self._db_password = password
        self._db_database = database
        self._db_host = host

        if os.path.exists(sql_input):
            with open(sql_input) as f:
                self._sql = f.read()
        else:
            self._sql = sql_input

        self._output_path = output_path

        logger.debug("user: {0}, password: {1}, database: {2}, host: {3}, output_path: {4}".format(
            self._db_user, self._db_password, self._db_database, self._db_host, self._output_path
        ))

        self.sql_to_csv()

    def execute(self):
        """
        Entry point for CLI
        :return: None
        """
        self.handle_arguments()
        self.sql_to_csv()


def main():
    """
    Function call by entry point code a specified in the setup.py
    :return:
    """
    cli = SqlToCsv()
    cli.execute()


if __name__ == '__main__':
    main()
