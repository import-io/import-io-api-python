#!/usr/bin/env python
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
from importio2 import ExtractorUtilities
from importio2 import CrawlRunAPI
from time import sleep
import logging
import sys
import os


# Check to see if the extractor id was
# passed on the command line
if len(sys.argv) != 2:
    print("usage: {0} extractor_id".format(os.path.basename(sys.argv[0])))
    sys.exit(1)
else:
    extractor_id = sys.argv[1]


def crawlrun_state(extractor, crawlrun):
    state = crawlrun_api.state(crawlrun)
    print("Extractor: {0}, Crawlrun: {1}, state: {2}".format(extractor, crawlrun, state))


#
# The environment variable IMPORT_IO_API_KEY needs to be set with your
# Import.io API key.
#
extractor_api = ExtractorAPI();
extractor_utils = ExtractorUtilities()
crawlrun_api = CrawlRunAPI()

#
# Call the API to start extractor which returns
# the crawl run Id
#
crawlrun_id = extractor_api.start(extractor_id)

#
# Call the state method on the CrawlRun API
# to get the current state of the call run
# started above
#

sleep(5)

crawlrun_state(extractor_id, crawlrun_id)

sleep(30)

crawlrun_state(extractor_id, crawlrun_id)

#
# This is a utility method for starting and blocking
# until the Extractor crawl run completes.
#
# The method returns the crawl run when the Extractor
# crawlrun is complete
#

crawlrun_id = extractor_utils.extractor_run_and_wait(extractor_id)
crawlrun_state(extractor_id, crawlrun_id)



