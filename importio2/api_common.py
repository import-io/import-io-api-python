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
import logging
import os
from importio2 import ApiCall


logger = logging.getLogger(__name__)


class ApiCommon(ApiCall):
    """
    Base class to implement common features of Import.io API
    """

    def __init__(self, api_host=None, api_key=None):
        super(ApiCommon, self).__init__(api_host, api_key)
        self.get_environment_variables()

    def get_environment_variables(self):
        """
        Get API Host and API key from environment variables
        if available
        :return: None
        """

        if 'IMPORT_IO_API_KEY' in os.environ:
            self.api_key = os.environ['IMPORT_IO_API_KEY']

        if 'IMPORT_IO_API_HOST' in os.environ:
            self.api_key = os.environ['IMPORT_IO_API_HOST']
