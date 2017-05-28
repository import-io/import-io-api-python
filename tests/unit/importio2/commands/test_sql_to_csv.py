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

from unittest import TestCase
from importio2.commands import SqlToCsv
import os
from tempfile import NamedTemporaryFile
import logging
import pymysql

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')

SIMPLE_SQL_PATH = os.path.join(os.path.dirname(__file__), 'test_sql_to_csv_query.sql')
PROCEDURE_SQL_PATH = os.path.join(os.path.dirname(__file__), 'test_sql_to_csv_proc.sql')


TEST_SQL_TO_CSV_PROC_FILE = os.path.join(os.path.dirname(__file__), 'test_sql_to_csv_proc_file.csv')
TEST_SQL_TO_CSV_QUERY_FILE = os.path.join(os.path.dirname(__file__), 'test_sql_to_csv_query_file.csv')


class TestSqlToCSV(TestCase):

    @staticmethod
    def file_to_str(path):
        """
        Reads the contents of a file an returns as a string
        :param path: Path to file contents to load
        :return: Str containing the contents of the file specified by path
        """
        contents = None
        with open(path) as f:
            contents = f.read()

        return contents

    @staticmethod
    def execute_sql(sql, commit=False):
        # Connect to the database
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     db=DB_DATABASE,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                if commit:
                    connection.commit()
        finally:
            connection.close()

    def setUp(self):
        f = NamedTemporaryFile(delete=False)
        self.csv_path = f.name

        TestSqlToCSV.execute_sql("""
            DROP TABLE IF EXISTS test_sql_to_csv;
            CREATE TABLE test_sql_to_csv (
                id MEDIUMINT NOT NULL AUTO_INCREMENT,
                name CHAR(30) NOT NULL,
                dt DATETIME NOT NULL,
                PRIMARY KEY (id));
        """)

        TestSqlToCSV.execute_sql("""
            INSERT INTO test_sql_to_csv(name, dt) VALUES('Bob', '2013-10-09');
            INSERT INTO test_sql_to_csv(name, dt) VALUES('Ted', '2014-10-09');
            INSERT INTO test_sql_to_csv(name, dt) VALUES('Carol', '2015-10-09');
            INSERT INTO test_sql_to_csv(name, dt) VALUES('Alice', '2016-10-09');
        """, commit=True)

        TestSqlToCSV.execute_sql("""
            CREATE PROCEDURE test_sql_to_csv_proc(dt DATETIME)
            BEGIN
                SELECT * FROM test_sql_to_csv a
                WHERE DATE(dt) = DATE(a.dt);
            END
        """, commit=True)

    def tearDown(self):
        TestSqlToCSV.execute_sql('DROP TABLE IF EXISTS test_sql_to_csv')
        TestSqlToCSV.execute_sql('DROP PROCEDURE IF EXISTS test_sql_to_csv_proc')
        if os.path.exists(self.csv_path):
            pass
            # os.remove(self.csv_path)

    def test_constructor(self):
        sql_to_csv = SqlToCsv()

    def test_simple_sql(self):
        sql_to_csv = SqlToCsv()
        sql_to_csv.run(user=DB_USER,
                       password=DB_PASSWORD,
                       host=DB_HOST,
                       database=DB_DATABASE,
                       sql_input="SELECT * FROM test_sql_to_csv",
                       output_path=self.csv_path)
        source = TestSqlToCSV.file_to_str(TEST_SQL_TO_CSV_QUERY_FILE)
        target = TestSqlToCSV.file_to_str(self.csv_path)
        self.assertEqual(source, target)

    def test_simple_sql_file(self):
        sql_to_csv = SqlToCsv()
        sql_to_csv.run(user=DB_USER,
                       password=DB_PASSWORD,
                       host=DB_HOST,
                       database=DB_DATABASE,
                       sql_input=SIMPLE_SQL_PATH,
                       output_path=self.csv_path)
        source = TestSqlToCSV.file_to_str(TEST_SQL_TO_CSV_QUERY_FILE)
        target = TestSqlToCSV.file_to_str(self.csv_path)
        self.assertEqual(source, target)

    def test_stored_procedure_file(self):
        sql_to_csv = SqlToCsv()
        sql_to_csv.run(user=DB_USER,
                       password=DB_PASSWORD,
                       host=DB_HOST,
                       database=DB_DATABASE,
                       sql_input=PROCEDURE_SQL_PATH,
                       output_path=self.csv_path)
        source = TestSqlToCSV.file_to_str(TEST_SQL_TO_CSV_PROC_FILE)
        target = TestSqlToCSV.file_to_str(self.csv_path)
        self.assertEqual(source, target)

    def test_stored_procedure(self):
        sql_to_csv = SqlToCsv()
        sql_to_csv.run(user=DB_USER,
                       password=DB_PASSWORD,
                       host=DB_HOST,
                       database=DB_DATABASE,
                       sql_input="CALL test_sql_to_csv_proc('2016-10-09')",
                       output_path=self.csv_path)

        source = TestSqlToCSV.file_to_str(TEST_SQL_TO_CSV_PROC_FILE)
        target = TestSqlToCSV.file_to_str(self.csv_path)
        self.assertEqual(source, target)
