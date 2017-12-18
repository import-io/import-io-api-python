#!/usr/bin/env python
# NOTE: Need to be running Python 3.4 or later
from importio2 import ExtractorAPI
from importio2 import ExtractorUtilities
from importio2 import CrawlRunAPI
from time import sleep
import logging
import sys
import os

logging.basicConfig(level=logging.NOTSET)

# Check to see if the extractor id was
# passed on the command line
if len(sys.argv) != 2:
    print("usage: {0} extractor_id".format(os.path.basename(sys.argv[0])))
    sys.exit(1)
else:
    extractor_id = sys.argv[1]

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
crawlrun_state = crawlrun_api.state(crawlrun_id)
print("Extractor Id: {0}, Crawlrun Id: {1}, state: {2}".format(extractor_id, crawlrun_id, crawlrun_state))

sleep(5)

crawlrun_state = crawlrun_api.state(crawlrun_id)
print("Extractor Id: {0}, Crawlrun Id: {1}, state: {2}".format(extractor_id, crawlrun_id, crawlrun_state))

sleep(30)

crawlrun_state = crawlrun_api.state(crawlrun_id)
print("Extractor Id: {0}, Crawlrun Id: {1}, state: {2}".format(extractor_id, crawlrun_id, crawlrun_state))

#
# This is a utility method for starting and blocking
# until the Extractor crawl run completes.
#
# The method returns the crawl run when the Extractor
# crawlrun is complete
#

crawlrun_id = extractor_utils.extractor_run_and_wait(extractor_id)
crawlrun_state = crawlrun_api.state(crawlrun_id)
print("Extractor Id: {0}, Crawlrun Id: {1}, state: {2}".format(extractor_id, crawlrun_id, crawlrun_state))



