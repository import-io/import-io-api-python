#!/usr/bin/env python
from importio2 import ExtractorAPI
from pprint import pprint


# Given the contents in the file urls.txt

extractor_id = '7d9122f6-f293-49e4-8035-1961dac6f049'

url_list = list()
url_list.append("http://www1.example.com")
url_list.append("http://www2.example.com")
url_list.append("http://www3.example.com")
url_list.append("http://www4.example.com")
url_list.append("http://www5.example.com")
url_list.append("http://www6.example.com")
url_list.append("http://www7.example.com")
url_list.append("http://www8.example.com")
url_list.append("http://www9.example.com")

api = ExtractorAPI()

# Upload a list of URLs to an extractor
api.put_url_list(extractor_id, url_list)


# Download a list of URLs to an extractor

url_list = api.get_url_list(extractor_id)
pprint(url_list)
