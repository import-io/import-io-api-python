#!/usr/bin/env python
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
from pytz import timezone
import argparse


class Date2Epoch(object):

    def __init__(self):
        self._year = None
        self._month = None
        self._day = None

    def handle_arguments(self):
        parser = argparse.ArgumentParser(description="Display the midnight to morning in epoch milliseconds given"
                                                     "year, month, and day")

        parser.add_argument('-y', '--year', action='store', dest='year', metavar='year', type=int, required=True,
                            help='Input year')
        parser.add_argument('-m', '--month', action='store', dest='month', metavar='month', type=int, required=True,
                            help='Input month')
        parser.add_argument('-d', '--day', action='store', dest='day', metavar='day', type=int, required=True,
                            help='Input day')

        args = parser.parse_args()

        if 'year' in args:
            self._year = args.year
        if 'month' in args:
            self._month = args.month
        if 'day' in args:
            self._day = args.day

    def compute_epochs(self):
        gmt = timezone('GMT')
        begin = datetime(self._year, self._month, self._day, 0, 0, 0)
        end = datetime(self._year, self._month, self._day, 23, 59, 59)
        begin_gmt = gmt.localize(begin)
        end_gmt = gmt.localize(end)
        print(begin_gmt)
        print(int(begin_gmt.timestamp()*1000))
        print(end_gmt)
        print(int(end_gmt.timestamp()*1000))

    def execute(self):
        self.handle_arguments()
        self.compute_epochs()


def main():
    cli = Date2Epoch()
    cli.execute()


if __name__ == '__main__':
    main()




