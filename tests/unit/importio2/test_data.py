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

from __future__ import absolute_import

EXTRACTOR_CSV_ID = 'b8debacc-b50d-46ce-a666-a1fb20420792'


class ExtractorCSVTestData(object):

    EXTRACTOR_ID = '366a3b3b-926c-4b58-88a0-445526b87f93'

    BAD_EXTRACTOR_ID = '3d38e829-cb92-4b73-8816-6eaf0172fc83'
    BAD_CSV_LENGTH = 56
    BAD_COLUMN_LENGTH = 3

    CSV_LEN = 5361
    COLUMN_LENGTH = 3


class ExtractorJSONTestData(object):

    EXTRACTOR_ID = '366a3b3b-926c-4b58-88a0-445526b87f93'

    JSON_LEN_API = 6
    JSON_LEN_RAW = 7


class ExtractorCrawlRunsTestData(object):

    EXTRACTOR_ID = 'a4727192-804f-47b1-b562-3f7d5fc89c78'

    GUID = 'a7b72673-78e0-4bdc-b100-b2d65b423199'

    CRAWL_RUNS_LEN = 12

    TOTAL_URL_COUNT = 1
    SUCCESS_URL_COUNT = 1
    FAILED_URL_COUNT = 0

    STATE = 'FINISHED'

    TYPE = 'CrawlRun'


class ExtractorCrawlRunStartTestData(object):


    EXTRACTOR_ID = 'bcbb4893-e914-485b-bf82-90874c51fe3b'


class ExtractorQueryTestData(object):

    EXTRACTOR_ID = 'fdc32e96-78b4-41a0-97a8-60af0febeba5'

    PAGE_QUERY_URL = 'http://www.ikea.com/us/en/search/?query=Towels'
    PAGE_2_QUERY_URL = 'http://www.ikea.com/us/en/search/?query=Towels&pageNumber=2'



