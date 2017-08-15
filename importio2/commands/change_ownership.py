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
from importio2 import CrawlRunAPI, ExtractorAPI
import logging

logger = logging.getLogger(__name__)


class ChangeOwnership(AdBase):
    """
    Implements a command that changes the ownership of:
      crawlrun
      extractor
    """

    def __init__(self):
        super(ChangeOwnership, self).__init__()
        self._object_id = None
        self._object_type = None
        self._object_user_id = None

    def handle_arguments(self):
        """
        Add the arguments specific to this command
        :return: None
        """
        self._parser.add_argument('-i', '--object-id', action='store', dest='object_id',
                                  metavar='object_id', required=True,
                                  help='Identifier of the object to change ownership of')
        self._parser.add_argument('-o', '--object-type', action='store', choices=['crawlrun', 'extractor'],
                                  default='crawl_run',
                                  help='Type of object to have its ownership changed')
        self._parser.add_argument('-u', '--object-user-id', action='store', dest='object_user_id', metavar='user-id',
                                  required=True, help='User to change ownership to')
        super(ChangeOwnership, self).handle_arguments()

    def get_arguments(self):
        """
        Collect arguments required for this command
        :return: None
        """
        super(ChangeOwnership, self).get_arguments()

        if self._args.object_id is not None:
            self._object_id = self._args.object_id

        if self._args.object_type is not None:
            self._object_type = self._args.object_type

        if self._args.object_user_id is not None:
            self._object_user_id = self._args.object_user_id

    def run(self, object_id, object_type, object_user_id, api_key=None):
        """
        Assigns the input variables and then runs the method to affect to the object
        owner change
        :param api_key:
        :param object_id: Object id in the object store
        :param object_type: Either: crawlrun or extractor
        :param object_user_id: User id to assign to the object
        :return: None
        """
        if api_key is not None:
            self._api_key = api_key
        self._object_id = object_id
        self._object_type = object_type
        self._object_user_id = object_user_id

        return self.change_ownership()

    def change_ownership(self):
        """
        Changes the ownership of an object in the object store. Callable form
        to be use by other code.
        :return:
        """
        if self._object_type == 'crawlrun':
            api = CrawlRunAPI()
            print(api.change_ownership(self._object_id, self._object_user_id))
        elif self._object_type == 'extractor':
            api = ExtractorAPI()
            print(api.change_ownership(self._object_id, self._object_user_id))

        return None

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


