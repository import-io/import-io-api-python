#!/usr/bin/env python
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

from importio2 import CrawlRunAPI
from importio2 import ExtractorAPI

# Create instances of the crawl run and extractor APIs
crawlRunAPI = CrawlRunAPI()
extractorAPI = ExtractorAPI()

# GUID of extractor that has a crawl run with file downloads
extractor_id = '35b38835-575e-49c3-b236-1ba6103c038a'

# Get the list of the crawl runs by the extractor
crawl_runs = extractorAPI.get_crawl_runs(extractor_id)

# Get the first one in list, which is the last one that was created
last_crawl_run = crawl_runs[0]

# Get the crawl run id which has the files we want to download
crawl_run_id = last_crawl_run['fields']['guid']

# Get the attachment id that has the zip file to download
file_id = last_crawl_run['fields']['files']

# Download the files to files.zip
crawlRunAPI.get_files(crawl_run_id=crawl_run_id, file_id=file_id, path='files.zip')
