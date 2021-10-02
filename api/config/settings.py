import os

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.environ.get('EMAIL')
SMTP_PASSWORD = os.environ.get('EMAIL_PWD')
EMAILS_FROM_NAME = "BookSpot"
EMAILS_FROM_EMAIL = os.environ.get('EMAIL')
EMAIL_TEMPLATES_DIR = "/usr/src/api/static/emails"

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

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_TEST_TOKEN = os.environ.get('GOOGLE_TEST_TOKEN')
