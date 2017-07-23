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

from datetime import datetime
from unittest import TestCase
from importio2.commands import Date2Epoch
from pytz import timezone


class TestDateToEpoch(TestCase):

    def test_constructor(self):
        d2e = Date2Epoch()
        self.assertIsNotNone(d2e)

    def test_epoch_date(self):
        year = 2010
        month = 7
        day = 15
        gmt = timezone('GMT')
        begin = gmt.localize(datetime(year, month, day, 0, 0, 0))
        end = gmt.localize(datetime(year, month, day, 23, 59, 59))

        d2e = Date2Epoch()
        begin_dt, end_dt = d2e.run(year, month, day)
        self.assertEqual(begin, begin_dt)
        self.assertEqual(end, end_dt)

    def test_epoch_date_year_out_of_bounds(self):
        with self.assertRaises(ValueError):
            year = -1
            month = 1
            day = 1
            d2e = Date2Epoch()
            begin_dt, end_dt = d2e.run(year, month, day)

    def test_epoch_date_month_out_of_bounds(self):
        with self.assertRaises(ValueError):
            year = 2010
            month = 13
            day = 1
            d2e = Date2Epoch()
            begin_dt, end_dt = d2e.run(year, month, day)

    def test_epoch_date_day_out_of_bounds(self):
        with self.assertRaises(ValueError):
            year = 2010
            month = 32
            day = 1
            d2e = Date2Epoch()
            begin_dt, end_dt = d2e.run(year, month, day)




