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
import logging
from pytz import timezone
from importio2.commands import AdBase

logger = logging.getLogger(__name__)


class Date2Epoch(AdBase):
    def __init__(self):
        super(Date2Epoch, self).__init__()
        self._year = None
        self._month = None
        self._day = None

    def cli_description(self):
        """
        Returns the description of the command
        :return: None
        """
        return 'Display the midnight to morning in epoch milliseconds given year, month, and day'

    def handle_arguments(self):
        """
        Parse the arguments from the command line
        :return: None
        """
        self._parser.add_argument('-y', '--year', action='store', dest='year', metavar='year', type=int, required=True,
                                  help='Input year')
        self._parser.add_argument('-m', '--month', action='store', dest='month', metavar='month', type=int,
                                  required=True,
                                  help='Input month')
        self._parser.add_argument('-d', '--day', action='store', dest='day', metavar='day', type=int, required=True,
                                  help='Input day')

        super(Date2Epoch, self).handle_arguments()

    def get_arguments(self):
        """
        Retrieves the command line arguments required by the command.
        :return: None
        """
        super(Date2Epoch, self).get_arguments()

        if self._args.year is not None:
            self._year = self._args.year
        if self._args.month is not None:
            self._month = self._args.month
        if self._args.day is not None:
            self._day = self._args.day

    def run(self, year, month, day):
        """
        Execute the method provide by this class
        :param year:
        :param month:
        :param day:
        :return: begin, end date in GMT epoch seconds
        """

        # Assign our instance variables
        self._year = year
        self._month = month
        self._day = day
        return self.compute_epochs()

    def compute_epochs(self):
        """
        Computes the epoch times in milliseconds from input year, month, day
        :return: begin_gmt, end_gmt
        """
        gmt = timezone('GMT')
        begin = datetime(self._year, self._month, self._day, 0, 0, 0)
        end = datetime(self._year, self._month, self._day, 23, 59, 59)
        begin_gmt = gmt.localize(begin)
        end_gmt = gmt.localize(end)
        logger.debug("begin_gmt: {0}, end_gmt: {1}".format(begin_gmt, end_gmt))
        return begin_gmt, end_gmt

    def output_epochs(self):
        """
        Output the epoch times in milliseconds and human readable form
        :return:
        """
        begin_gmt, end_gmt = self.compute_epochs()
        print(begin_gmt)
        print(int(begin_gmt.timestamp() * 1000))
        print(end_gmt)
        print(int(end_gmt.timestamp() * 1000))

    def execute(self):
        """
        Entry point for CLI
        :return:
        """
        self.handle_arguments()
        self.output_epochs()


def main():
    cli = Date2Epoch()
    cli.execute()


if __name__ == '__main__':
    main()
