#
# Copyright 2018 Import.io
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

from importio2.report_api_core import report_get
from importio2.report_api_core import report_list

DEFAULT_GUID=''


class TestReportsAPI(TestCase):

    def setUp(self):
        self._api_key = os.environ['IMPORT_IO_API_KEY']

    def test_api_report_get(self):
        report = report_get(self._api_key, DEFAULT_GUID, 1)
        self.assertIsNotNone(report)

    def test_api_reports_list(self):
        result = report_list(self._api_key, 1)
        print(result)
