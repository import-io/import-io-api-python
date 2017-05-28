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
import os
import filecmp
import json
from tempfile import NamedTemporaryFile
from importio2.commands import CsvToJson

CSV_FILENAME = 'csv_to_json.csv'
JSON_FILENAME = 'csv_to_json.json'


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


class TestCsvToJson(TestCase):

    def setUp(self):
        f = NamedTemporaryFile(delete=False)
        self.json_path = f.name
        self.csv_path = os.path.join(os.path.dirname(__file__), CSV_FILENAME)
        self.json_example_path = os.path.join(os.path.dirname(__file__), JSON_FILENAME)
        print(self.json_path)

    def tearDown(self):
        if os.path.exists(self.json_path):
            os.remove(self.json_path)

    def test_constructor(self):
        cli = CsvToJson()
        self.assertIsNotNone(cli)



