#
# Copyright 2016 Import.io
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

from __future__ import absolute_import

from unittest import TestCase
from importio2 import Extractor
from importio2 import ExtractorAPI


class TestExtractorAPI(TestCase):

    def test_constructor(self):
        """
        Ensure default constructor runs
        :return:
        """
        extractor_api = ExtractorAPI()
        self.assertIsNotNone(extractor_api)


class TestExtractor(TestCase):

    def test_constructor_by_guid(self):
        extractor = Extractor(guid='')
        self.assertIsNotNone(extractor)

    def test_constructor_by_name(self):
        extractor = Extractor(name='')
        self.assertIsNotNone(extractor)

    def test_fields(self):
        pass

    def test_empty_guid(self):
        try:
            extractor = Extractor()
            self.assertTrue(True)
        except ValueError:
            pass


