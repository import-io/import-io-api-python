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
from importio2 import ApiCommon

logger = logging.getLogger(__name__)


class Schema(object):

    def __init__(self, guid=None):
        if guid is None:
            raise ValueError()
        self._guid = guid

    @property
    def guid(self):
        return self._guid

    # TBD other properties


class DataStore(ApiCommon):
    """
    Import.io APIs related to the data store
    """

    def __init__(self):
        pass

    def get_schema(self, cls):
        """
        Fetches the schema associated with an account in Import.io
        :return:
        """
        self.api_host = 'store.api.import.io'
        self.path = "/store/{0}".format(cls)
        return self.api_call()

    def get_object(self, cls=None, guid=None):
        self.api_host = 'store.api.import.io'
        self.path = "/store/{0}/{1}".format(cls, guid)
        return self.api_call()
