import pymysql
import os

DB_USER = os.getenv('DB_USER')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')


class DbTestUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def file_to_str(path):

        """
        Reads the contents of a file an returns as a string
        :param path: Path to file contents to load
        :return: Str containing the contents of the file specified by path
        """
        contents = None
        with open(path) as f:
            contents = f.read()

        return contents

    @staticmethod
    def execute_sql(sql, commit=False):

        # Connect to the database
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     db=DB_DATABASE,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                if commit:
                    connection.commit()
        finally:
            connection.close()
