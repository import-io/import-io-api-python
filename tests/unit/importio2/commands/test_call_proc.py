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

import os
from unittest import TestCase

from importio2.commands import CallProc
from importio2.commands import RunSql

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_HOST = os.getenv('DB_HOST')

PROCEDURE_SQL = """
CREATE PROCEDURE test_now(dt DATETIME)
BEGIN
    SELECT dt;
END
"""


class TestCallProc(TestCase):

    def setUp(self):
        run_sql = RunSql()
        run_sql.run(user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE, host=DB_HOST,
                    sql_input='DROP PROCEDURE IF EXISTS test_now')
        run_sql.run(user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE, host=DB_HOST, sql_input=PROCEDURE_SQL)

    def tearDown(self):
        run_sql = RunSql()
        run_sql.run(user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE, host=DB_HOST,
                    sql_input='DROP PROCEDURE IF EXISTS test_now')

    def test_constructor(self):
        call_proc = CallProc()
        self.assertIsNotNone(call_proc)

    def test_create_and_run_prodcedure(self):
        call_proc = CallProc()
        call_proc.call_proc(user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE, host=DB_HOST,
                            proc='test_now', args=('2018-05-06',))
