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
from importio2 import ExtractorAPI
import os


class API(object):
    """
    Provides access to Import.io API
    """

    def __init__(self):
        self._extractor = ExtractorAPI()
        self._crawl_run = None

    @property
    def crawl_run(self):
        return self._crawl_run

    @property
    def extractor(self):
        return self._extractor


class ImportioAPI(object):

    def __init__(self):
        self._api_key = os.environ['IMPORT_IO_API_KEY']