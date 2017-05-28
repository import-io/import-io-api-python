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
import pymysql
import os


class RunSql(AdDatabase):

    def __init__(self):
        super(RunSql, self).__init__()
        self._sql_input = None

    def handle_arguments(self):
        self.add_database_arguments()
        self._parser.add_argument('--sql-input', action='store', dest='sql_input', metavar="sql | path", required=True,
                                  help="Path or SQL statement to run")
        super(RunSql, self).handle_arguments()
        self.get_arguments()

    def get_arguments(self):
        super(RunSql, self).get_arguments()

        if 'sql_input' in self._args:
            self._sql_input = self._args.sql_input

    def run(self, user, password, database, host, sql_input):
        self._db_user = user
        self._db_password = password
        self._db_database = database
        self._db_host = host
        self._sql_input = sql_input

        self.run_sql()

    def run_sql(self):
        query = None
        if os.path.exists(self._sql_input):
            with open(self._sql_input) as f:
                query = f.read()
        else:
            query = self._sql_input

        cnx = pymysql.connect(user=self._db_user,
                              password=self._db_password,
                              database=self._db_database,
                              host=self._db_host)
        cursor = cnx.cursor()

        cursor.execute(query)
        for row in cursor:
            print(row)
        cursor.close()

        cnx.close()

    def execute(self):
        """
        Main entry point for CLI
        :return:
        """
        self.handle_arguments()
        self.run_sql()


def main():
    """
    Entry point call be setup.py
    :return:
    """
    cli = RunSql()
    cli.execute()

if __name__ == '__main__':
    main()