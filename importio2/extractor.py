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
from importio2 import CSVData

logger = logging.getLogger(__name__)


class ExtractorAPI(object):
    """
    API level abstraction, handles the authentication via environment variables
    """
    def __init__(self):
        self._api_key = os.environ['IMPORT_IO_API_KEY']

    def change_ownership(self, extractor_id, owner_id):
        result = None
        try:
            response = apicore.object_store_change_ownership(
                api_key=self._api_key, object_type='extractor',  object_id=extractor_id)
            # If the HTTP result code is not 200 then throw our hands up and
            # raise an exception
            if response.status_code == requests.codes.ok:
                result = response.json()
            else:
                raise Exception()
        except Exception as e:
            logger.exception(e)
        return result

    def cancel(self, guid):
        """
        Cancel a crawl run in progress

        :param guid: Identifier of the extractor
        :return: dictionary of values representing the extractor
        """
        try:
            crawl_run_guid = None
            response = apicore.extractor_cancel(self._api_key, guid)

            # If the HTTP result code is not 200 then throw our hands up and
            # raise an exception
            if response.status_code == requests.codes.ok:
                crawl_run = json.loads(response.text)
                crawl_run_id = crawl_run['crawlRunId']
            else:
                raise Exception()

            return crawl_run_guid
        except Exception as e:
            logger.exception(e)
            return None

    def csv(self, guid):
        """
        Returns the contents of the CSV file as list of lists from the most recent crawl run.
        The header appears in the first row

        :param guid:
        :param guid: Identifier of the extractor
        :return: List of lists containing the contents of the CSV
        """
        results = None
        try:
            response = apicore.extractor_csv(self._api_key, guid)
            if response.status_code == requests.codes.ok:
                lines = response.text.split('\n')
                results = []
                for l in lines:
                    results.append(l.replace('\r', '').replace('"', '').split(','))
                results = results[:-1]
        except Exception as e:
            logger.exception(e)
        return results

    def json(self, guid):
        """
        Return a list of JSON documents from an Extractor by converting JSON into dictionaries
        and adding to a python list
        :param guid: Identifier of the extractor
        :return: List of JSON documents
        """
        results = None
        try:
            for i in range(1, 6):
                response = apicore.extractor_json(self._api_key, guid)
                if response.status_code == requests.codes.ok:
                    results = []
                    lines = response.text.split('\n')
                    for l in lines:
                        if len(l) > 0:
                            results.append(json.loads(l))
                    break
                else:
                    logger.error("Getting JSON attachment from: {0}, return {1}, retrying".format(
                        guid, response.status_code))
        except Exception as e:
            logger.exception(e)
        return results

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
            logger.exception(e)

    def get_crawl_runs(self, guid):
        """
        Returns a list of crawl runs associated with an extractor

        :param guid: Identifier of the extractor
        :return: List containing extractor dictionaries
        """
        crawl_runs = []
        try:
            response = apicore.extractor_get_crawl_runs(self._api_key, guid, 1, 30)
            # If the HTTP result code is not 200 then throw our hands up and
            # raise an exception
            if response.status_code == requests.codes.ok:
                runs = json.loads(response.text)
                for run in runs['hits']['hits']:
                    crawl_runs.append(run)
            else:
                raise Exception()
            return crawl_runs

        except Exception as e:
            logger.exception(e)

    def get_by_name(self, name):
        # Todo: Exception if you cannot find the Extractor in the account then throw an exception
        return {}

    def log(self, guid):
        """
        Returns a list of log dictionaries
        :param guid: 
        :return: List containing log records
        """
        log_records = []
        try:
            response = apicore.extractor_log(self._api_key, guid)
            # If the HTTP result code is not 200 then throw our hands up and
            # raise an exception
            logger.debug(response.status_code)
            if response.status_code == requests.codes.ok:
                log_records = response.text.split('\n')
            else:
                raise Exception()
        except Exception as e:
            logger.exception(e)
        return log_records[:-1]

    def get_url_list(self, guid):
        """
        Returns the URLs associated with an Extractor

        :param guid: Identifier of the extractor
        :return: List of URL strings
        """
        extractor = self.get(guid)
        url_list_guid = extractor['urlList']
        response = apicore.extractor_url_list_get(self._api_key, guid, url_list_guid)
        url_list = response.text.split('\n')
        return url_list

    def list(self):
        """
        Returns a list of Extractor GUIDs in an account

        :return: List of GUIDs
        """
        return []

    def put_url_list(self, guid, urls):
        """
        Replaces the URL list on an Extractor
        :param guid: Identifier of the extractor
        :param url_list: List of string containing URLs
        :return: None
        """
        url_list_id = None
        try:
            url_list = '\n'.join(urls)
            response = apicore.extractor_url_list_put(self._api_key, guid, url_list)
            if response.status_code == requests.codes.ok:
                result = json.loads(response.text)
                url_list_id = result['guid']
            else:
                logger.error("Unable set url list for extractor: {0}".format(guid))
                raise Exception()
        except Exception as e:
            logger.exception(e)
        return url_list_id

    def query(self, guid, url):
        """
        Runs a live query with the Extractor

        :param guid: Identifier of the extractor
        :param url: URL to run the Extractor against
        :return: A dictionary of the results of the query
        """
        result = None
        try:
            # Make 5 attempts
            response = None
            success = True
            for i in range(1, 6):
                response = apicore.extractor_query(self._api_key, guid, url)
                if response.status_code == requests.codes.ok:
                    result = json.loads(response.text)
                    success = True
                    break
                else:
                    logger.error('Query failed for extractor: \"{0}\" with url: \"{1}\", http code:\"{2}\"'.format(
                        guid, url, response.status_code))
            if not success:
                logger.error("Unable to run query: {0} extractor: {1}, HTTP Code".format(url, guid, response.status_code))
                raise Exception()
        except Exception as e:
            logger.exception(e)
        return result

    def start(self, guid):
        """
        Starts a crawl run of an extractor

        :param guid: Extractor identifier
        :return: Crawl run identifier
        """
        crawl_run_id = None
        try:
            # TODO: What are the failure conditions we need to handle
            # TODO: What exceptions should we throw based on Network available, etc
            # TODO: What if a crawl run is already underway?
            response = apicore.extractor_start(self._api_key, guid)

            # If the HTTP result code is not 200 then throw our hands up and
            # raise an exception
            if response.status_code == requests.codes.ok:
                crawl_run = json.loads(response.text)
                crawl_run_id = crawl_run['crawlRunId']
            else:
                logger.error("Unable to start crawl run for extractor: {0}".format(guid))
                raise Exception()
            return crawl_run_id
        except Exception as e:
            logger.exception(e)
        return crawl_run_id


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
        api = ExtractorAPI()
        return api.get_url_list(self._guid)

    @property
    def status(self):
        pass

    def refresh(self):
        """
        Fetch the fields from the data store for this extractor given the name or guid
        :return:
        """
        api = ExtractorAPI()
        if self._name is not None:
            self.extractor = api.get_by_name(self._name)
        else:
            self.extractor = api.get(self._guid)

    def cancel(self):
        """
        Cancel a running extractor crawl run

        :return:
        """
        api = ExtractorAPI()
        api.cancel(self._guid)

    def start(self):
        """
        Start an Extractor crawl run

        :return: GUID of the crawl run
        """
        api = ExtractorAPI()
        api.start(self._guid)

    def csv(self):
        """
        Returns the CSV output from the most recent crawl run

        :return:
        """
        api = ExtractorAPI()
        result = api.csv(self._guid)
        csv = CSVData(header=result[0], data=result[1:])
        return csv



