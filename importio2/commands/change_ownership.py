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

from importio2.commands import AdBase
from importio2 import CrawlRunAPI
import logging


class ChangeOwnership(AdBase):

    def __init__(self):
        super(ChangeOwnership, self).__init__()

    def handle_arguments(self):

        self._parser.add_argument()
        super(ChangeOwnership, self).handle_arguments()

    def run(self, api_key, object_id, object_type):
        pass

    def change_ownership(self):
        pass

    def execute(self):
        """
        Entry point for CLI
        :return:
        """
        self.handle_arguments()
        self.change_ownership()


def main():
    """
    Main entry point from setup.py
    :return:
    """
    cli = ChangeOwnership()
    cli.execute()


if __name__ == '__main__':
    main()


