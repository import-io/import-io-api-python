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
import importio2.apicore as apicore
import json

logger = logging.getLogger(__name__)


class ExtractorAPI(object):
    """
    API level abstraction, handles the authentication via environment variables
    """
    def __init__(self):
        self._api_key = os.environ['IMPORT_IO_API_KEY']

    def get(self, guid):
        """
        Returns a dictionary of the contents of extractor
        :param guid: Identifier of the extractor
        :return: dictionary of values representing the extractor
        """
        extractor = None
        try:
            # TODO: What are the failure conditions we need to handle
            # TODO: What exceptions should we throw based on Network available, etc
            response = apicore.extractor_get(self._api_key, guid)

            # If the HTTP result code is not 200 then throw our hands up and
            # raise an exception
            if response.status_code == requests.codes.ok:
                extractor = json.loads(response.text)
            else:
                raise Exception()
            return extractor
        except Exception as e:
            print(e)

    def get_by_name(self, name):
        # Todo: Exception if you cannot find the Extractor in the account then throw an exception
        return {}

    def get_url_list(self, guid):
        return []

    def list(self):
        return []

    def put_url_list(self, guid, url_list):
        pass

    def query(self, guid, url):
        pass

    def start(self, guid):
        pass


class ExtractorUrl(object):
    def __init__(self, url):
        self._url = None


class ExtractorField(object):

    def __init__(self, field):
        self._field = field

    @property
    def id(self):
        return self._field['id']

    @property
    def name(self):
        return self._field['name']

    @property
    def capture_link(self):
        return self._field['captureLink']

    @property
    def type(self):
        return self._field['type']


class ExtractorFields(object):

    def __init__(self, fields):
        self._fields = fields

    def __getitem__(self, key):
        return ExtractorField(self._fields[key])

    def __len__(self):
        return len(self._fields)


class Extractor(object):
    def __init__(self, guid=None, name=None):
        if guid is None and name is None:
            raise ValueError()
        self._guid = guid
        self._name = name
        self.extractor = None

        self.refresh()

    @property
    def guid(self):
        return self.extractor['guid']

    @property
    def name(self):
        return self.extractor['name']

    @property
    def timestamp(self):
        return self.extractor['_meta']['timestamp']

    @property
    def last_editor_guid(self):
        return self.extractor['_meta']['lastEditorGuid']

    @property
    def owner_guid(self):
        return self.extractor['_meta']['ownerGuid']

    @property
    def creator_guid(self):
        return self.extractor['_meta']['creatorGuid']

    @property
    def creation_timestamp(self):
        return self.extractor['_meta']['creationTimestamp']

    @property
    def fields(self):
        return ExtractorFields(self.extractor['fields'])

    @property
    def url_list(self):
        return self.extractor['urlList']

    def refresh(self):
        api = ExtractorAPI()
        if self._name is not None:
            self.extractor = api.get_by_name(self._name)
        else:
            self.extractor = api.get(self._guid)



