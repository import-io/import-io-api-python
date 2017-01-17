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

from importio2 import CSVData

from unittest import TestCase
import logging

logger = logging.getLogger(__name__)


class TestCSVData(TestCase):

    def setUp(self):
        self.header = ["red", "green", "blue"]
        self.data = []
        self.data.append([1, 2, 3])
        self.data.append([4, 5, 6])
        self.data.append([7, 8, 9])

    def test_constructor(self):
        csv = CSVData(header=self.header, data=self.data)

    def test_iterator(self):
        csv = CSVData(header=self.header, data=self.data)

        for c in csv:
            print(c)
