import os

DEBUG = True

DATABASE = {
    'HOST': os.environ.get('PSQL_HOST'),
    'DB': os.environ.get('PSQL_DATABASE'),
    'USER': os.environ.get('PSQL_USER'),
    'PASSWORD': os.environ.get('PSQL_PWD'),
}

DATABASE_URI = "postgresql://{}:{}@{}/{}".format(DATABASE["USER"],
                                                                  DATABASE["PASSWORD"],
                                                                  DATABASE["HOST"],
                                                                  DATABASE["DB"])

TEST_DATABASE_URI = "postgresql://{}:{}@{}/tests".format(DATABASE["USER"],
                                                                  DATABASE["PASSWORD"],
                                                                  DATABASE["HOST"],
                                                                  DATABASE["DB"])
