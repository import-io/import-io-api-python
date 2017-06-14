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
from collections import UserDict
from enum import Enum, unique
from importio2.apicore import object_store_create
import os


@unique
class CrawlRunState(Enum):
    CANCELLED = 1
    FINISHED = 2
    PENDING = 3
    STARTED = 4

    names = ["CANCELLED", "FINISHED", "PENDING", "STARTED"]

    def describe(self):
        return self.name, self.value

    def __str__(self):
        return '{0}'.format(self.names[self.value])


class CrawlRun(UserDict):
    @staticmethod
    def create_crawl_run(
            extractor_id,
            failed_url_count,
            success_url_count,
            total_url_count,
            row_count,
            started_at,
            stopped_at,
            state):
        data = {
            'extractorId': extractor_id,
            'failedUrlCount': failed_url_count,
            'successUrlCount': success_url_count,
            'totalUrlCount': total_url_count,
            'rowCount': row_count,
            'startedAt': started_at,
            'stoppedAt': stopped_at,
            'state': state
        }
        return CrawlRun(dict=data)


class ObjectStoreAPI(object):
    def __init__(self):
        self._api_key = os.environ['IMPORT_IO_API_KEY']

    def create_crawl_run(self, crawl_run):
        response = object_store_create(self._api_key, 'crawlrun', crawl_run)
        return response.json()

    def object_store_change_ownership(self, object, object_type):
        pass
