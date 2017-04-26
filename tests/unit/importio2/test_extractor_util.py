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
from importio2 import ExtractorUtilities
from tests.unit.importio2.test_data import ExtractorRunAndWait


class TestExtractorAPI(TestCase):

    def test_constructor(self):
        utils = ExtractorUtilities
        self.assertIsNotNone(utils)

    def test_start_and_wait_extractor(self):
        utils = ExtractorUtilities()

        utils.extractor_run_and_wait(ExtractorRunAndWait.EXTRACTOR_ID)
