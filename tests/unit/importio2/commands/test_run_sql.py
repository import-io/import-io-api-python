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
from importio2.commands import RunSql
import os

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_HOST = os.getenv('DB_HOST')


class TestRunSql(TestCase):

    def test_constructor(self):
        run_sql = RunSql()

    def test_run_sql(self):
        run_sql = RunSql()
        sql = "SELECT NOW()"
        run_sql.run(user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE, host=DB_HOST, sql_input=sql)