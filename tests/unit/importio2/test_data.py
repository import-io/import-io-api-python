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
from datetime import datetime

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


class ExtractorUrlListPutTestData(object):

    EXTRACTOR_ID = '8fd833ca-6b6b-4ecb-abf4-a7223251a97e'

    URL_LIST = "http://www.ikea.com/us/en/search/?query=chairs&pageNumber=1\nhttp://www.ikea.com/us/en/search/?query=chairs&pageNumber=2\nhttp://www.ikea.com/us/en/search/?query=chairs&pageNumber=3\nhttp://www.ikea.com/us/en/search/?query=chairs&pageNumber=4\nhttp://www.ikea.com/us/en/search/?query=chairs&pageNumber=5\nhttp://www.ikea.com/us/en/search/?query=chairs&pageNumber=6\nhttp://www.ikea.com/us/en/search/?query=chairs&pageNumber=7\nhttp://www.ikea.com/us/en/search/?query=chairs&pageNumber=8\nhttp://www.ikea.com/us/en/search/?query=chairs&pageNumber=9\nhttp://www.ikea.com/us/en/search/?query=chairs&pageNumber=10"


class ObjectStoreCrawlRunTestData(object):

    EXTRACTOR_ID = '8fd833ca-6b6b-4ecb-abf4-a7223251a97e'
    STARTED_AT = int(datetime(2017, 1, 1, 9, 0, 0).strftime('%s')) * 1000
    STOPPED_AT = int(datetime(2017, 2, 15, 18, 0, 0).strftime('%s')) * 1000
    ROW_COUNT = 1000
    TOTAL_URL_COUNT = 100
    SUCCESS_URL_COUNT = 100
    FAILED_URL_COUNT = 0
    STATE = 'FINISHED'


class ObjectStoreExtractorPutUrlListAttachment(object):

    EXTRACTOR_ID = '0d1c19f0-399a-4310-b48b-e76131e9ee4c'
    OBJECT_TYPE = 'extractor'
    ATTACHMENT_FIELD = 'urlList'
    ATTACHMENT_CONTENTS = """http://www.example.com?foo=bar
http://www.example.com/?red=green
"""
    ATTACHMENT_TYPE = 'text/plain'


class ObjectStoreExtractorPutCsvAttachment(object):

    CRAWL_RUN_ID = '4cabd98f-72c3-4b99-9fc6-85ebc1dc6e60'
    OBJECT_TYPE = 'crawlrun'
    ATTACHMENT_FIELD = 'csv'
    ATTACHMENT_CONTENTS = """http://www.example.com?foo=bar
http://www.example.com/?red=green
"""
    ATTACHMENT_TYPE = 'text/csv'


class ObjectStoreExtractorPutJsonAttachment(object):

    CRAWL_RUN_ID = '3e9a9971-618e-4dc1-aea1-c4b8323cbb7d'
    OBJECT_TYPE = 'crawlrun'
    ATTACHMENT_FIELD = 'json'
    ATTACHMENT_CONTENTS = """{"url":"http://www.example.com/?foo=bar","result":{"extractorData":{"url":"http://www.example.com/?foo=bar","resourceId":"8eac9d40c7b312e36c3518821bd7256c","data":[{"group":[{"header":[{"text":"Example Domain"}],"description":[{"text":"This domain is established to be used for illustrative examples in documents. You may use this domain in examples without prior coordination or asking for permission."}],"link":[{"text":"More information...","href":"http://www.iana.org/domains/example"}]}]}]},"pageData":{"resourceId":"8eac9d40c7b312e36c3518821bd7256c","statusCode":200,"timestamp":1488670639095},"timestamp":1488670639860,"sequenceNumber":0}}
{"url":"http://www.example.com/?red=green","result":{"extractorData":{"url":"http://www.example.com/?red=green","resourceId":"c5355c6a9536e87d978a4417d01206ff","data":[{"group":[{"header":[{"text":"Example Domain"}],"description":[{"text":"This domain is established to be used for illustrative examples in documents. You may use this domain in examples without prior coordination or asking for permission."}],"link":[{"text":"More information...","href":"http://www.iana.org/domains/example"}]}]}]},"pageData":{"resourceId":"c5355c6a9536e87d978a4417d01206ff","statusCode":200,"timestamp":1488670639954},"timestamp":1488670640902,"sequenceNumber":1}}
"""
    ATTACHMENT_TYPE = 'application/x-ldjson'


class CrawlRunCreateCrawlRun(object):

    EXTRACTOR_ID = '8359345f-a2ac-45c1-be03-39812f13b9ef'

    FAILED_URL_COUNT = 1
    SUCCESS_URL_COUNT = 999
    TOTAL_URL_COUNT = 1000
    ROW_COUNT = 12345
    STARTED_AT = int(datetime(2016, 6, 4, 6, 0, 0).strftime('%s')) * 1000
    STOPPED_AT = int(datetime(2016, 6, 4, 18, 0, 0).strftime('%s')) * 1000
    STATE = 'FINISHED'


class CrawlRunCreateCrawlRunDateTime(object):

    EXTRACTOR_ID = 'e9afda7b-2f5c-4c33-a7c3-8068c2d65fa8'
    FAILED_URL_COUNT = 1

    SUCCESS_URL_COUNT = 999
    TOTAL_URL_COUNT = 1000
    ROW_COUNT = 12345
    STARTED_AT = datetime(2016, 6, 4, 6, 0, 0)
    STOPPED_AT = datetime(2016, 6, 4, 18, 0, 0)
    STATE = 'FINISHED'


class CrawlRunJsonAttachment(object):
    EXTRACTOR_ID = '8279069a-7a85-4905-8ffd-bf47faa28859'
    CRAWL_RUN_ID = 'e2d66cc2-e09a-4784-8576-8c88857624bf'
    FAILED_URL_COUNT = 0
    SUCCESS_URL_COUNT = 1
    TOTAL_URL_COUNT = 1
    ROW_COUNT = 2
    STARTED_AT = int(datetime(2016, 6, 4, 6, 0, 0).strftime('%s')) * 1000
    STOPPED_AT = int(datetime(2016, 6, 4, 18, 0, 0).strftime('%s')) * 1000
    STATE = 'FINISHED'


class CrawlRunJsonAttachmentNew(object):
    EXTRACTOR_ID = '26ccf0ae-3d13-47d0-8939-4567c17e06fe'
    FAILED_URL_COUNT = 1
    SUCCESS_URL_COUNT = 999
    TOTAL_URL_COUNT = 1000
    ROW_COUNT = 12345
    STARTED_AT = int(datetime(2016, 6, 4, 6, 0, 0).strftime('%s')) * 1000
    STOPPED_AT = int(datetime(2016, 6, 4, 18, 0, 0).strftime('%s')) * 1000
    STATE = 'FINISHED'

    FILE_NAME = 'crawl_run.json'


class CrawlRunCsvAttachmentNew(object):
    EXTRACTOR_ID = 'c08e937c-3d40-4c41-a313-ac232d70da77'
    FAILED_URL_COUNT = 1
    SUCCESS_URL_COUNT = 999
    TOTAL_URL_COUNT = 1000
    ROW_COUNT = 12345
    STARTED_AT = int(datetime(2016, 6, 4, 6, 0, 0).strftime('%s')) * 1000
    STOPPED_AT = int(datetime(2016, 6, 4, 18, 0, 0).strftime('%s')) * 1000
    STATE = 'FINISHED'
    FILE_NAME = 'crawl_run.csv'


class CrawlRunCsvJsonAttachment(object):
    EXTRACTOR_ID = '49f10801-3593-47f1-b704-a757480cb36a'
    CRAWL_RUN_ID = 'f273af4c-599b-4dce-8023-ca6c78875953'
    FAILED_URL_COUNT = 0
    SUCCESS_URL_COUNT = 1
    TOTAL_URL_COUNT = 1
    ROW_COUNT = 2
    STARTED_AT = 1488768583669
    STOPPED_AT = 1488768587368
    STATE = 'FINISHED'

    CSV_FILENAME = 'csv_attachment.csv'
    JSON_FILENAME = 'json_attachment.json'


class CrawlRunCsvJsonAttachmentNew(object):
    EXTRACTOR_ID = 'c6ca928e-1dae-4860-b19a-b195f22e7a78'
    FAILED_URL_COUNT = 0
    SUCCESS_URL_COUNT = 3
    TOTAL_URL_COUNT = 3
    ROW_COUNT = 6
    STARTED_AT = 1488768583669
    STOPPED_AT = 1488768587368
    STATE = 'FINISHED'

    CSV_FILENAME = 'csv_attachment.csv'
    JSON_FILENAME = 'json_attachment.json'






