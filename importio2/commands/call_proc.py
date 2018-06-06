#
# Copyright 2018 Import.io
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
import pymysql

logger = logging.getLogger(__name__)


class CallProc(object):

    def __init__(self):
        pass

    def call_proc(self, user, password, database, host, proc, args):
        """
        Entry point to execute this command programmatically
        :param user: User to use to authentication against the database
        :param password: Password to use to authentication against the database
        :param database: Which database to make current for the query
        :param host: Location of the database either hostname or IP address
        :param proc: Ether a bare SQL statement or path to file containing SQL if the path exists
        :return: None
        """
        cnx = pymysql.connect(user=user,
                              password=password,
                              database=database,
                              host=host)
        cursor = cnx.cursor()
        logger.info("Call procedure: {0} query with args: {1}".format(proc, args))
        cursor.callproc(proc, args)
        for row in cursor:
            logger.info(row)
        cursor.close()
        cnx.close()

