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

from unittest import TestCase, skip

from tests.unit.importio2.commands.db_test_utils import *

from importio2.commands import CsvToDatabase


CSV_TO_DB_TABLE = 'test_csv_to_db'
CSV_PATH = os.path.join(os.path.dirname(__file__), 'test_csv_to_db.csv')


@skip
class TestCsvToDatabase(TestCase):

    def setUp(self):
        DbTestUtils.execute_sql("""
            DROP TABLE IF EXISTS test_csv_to_db;
            CREATE TABLE test_csv_to_db (
                id BIGINT NOT NULL AUTO_INCREMENT,
                name CHAR(30) NOT NULL,
                dt DATETIME NOT NULL,
                PRIMARY KEY (id));
        """)

    def tearDown(self):
        pass
#        DbTestUtils.execute_sql("""
#            DROP TABLE IF EXISTS test_csv_to_db;
#        """)

    def test_constructor(self):
        csv_to_db = CsvToDatabase()

    def test_csv_to_db_table_append(self):
        csv_to_db = CsvToDatabase()
        csv_to_db.run(
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE,
            host=DB_HOST,
            table=CSV_TO_DB_TABLE,
            csv_path=CSV_PATH,
            append=True,
            create=False)

