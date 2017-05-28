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
from ebayio import CsvDownload
from tempfile import NamedTemporaryFile
import os

EXTRACTOR_ID = '30f0adfb-a404-4eb6-9f7c-ac9a0a709106'


class TestCsvDownload(TestCase):

    def setUp(self):
        f = NamedTemporaryFile(delete=False)
        self.path = f.name

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_run(self):
        csv_download = CsvDownload()
        csv_download.run(extractor_id=EXTRACTOR_ID, output_path=self.path)
        with open(self.path) as f:
            lines = f.readlines()
            self.assertIsNotNone(lines)
            self.assertEqual(3, len(lines))

