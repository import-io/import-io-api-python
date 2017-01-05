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
import requests
import os

logger = logging.getLogger(__name__)


class ExtractorAPI(object):
    def __init__(self):
        pass

    @staticmethod
    def json_to_extractor(document):
        guid = document['guid']
        name = document['name']
        return Extractor(guid=guid, name=name)

    def get(self, guid):
        """
        Returns a surrogate instance to manipulate an Extractor
        :param guid: Identifier of the extractor
        :return: instance of Extractor
        """

        url = "https://store.import.io/store/extractor/{0}".format(guid)

        querystring = {
            "_apikey": os.environ['IMPORT_IO_API_KEY']
        }

        headers = {
            'cache-control': "no-cache",
            'postman-token': "e550717b-851f-0951-2471-9578b2b86e97"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)

        def list(self):
            return []

        def get_url_list(self, extractor):
            pass


class ExtractorUrl(object):
    def __init__(self, url):
        self._url = None


class Extractor(object):
    def __init__(self, guid=None, name=None):
        if guid is None and name is None:
            raise ValueError()
        self._guid = guid
        self._name = name
        self._last_editor_guid = None
        self._timestamp = None
        self._owner_guid = None
        self._creator_guid = None
        self._creation_timestamp = None
        self._fields = None

    @property
    def guid(self):
        return self._guid

    @property
    def name(self):
        return self._name

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def last_editor_guid(self):
        return self._last_editor_guid

    @property
    def owner_guid(self):
        pass

    @property
    def creator_guid(self):
        return self._creator_guid

    @property
    def creation_timestamp(self):
        return self._creation_timestamp

    @property
    def fields(self):
        return self._fields

    @property
    def url_list(self):
        return []

    def refresh(self):
        pass
