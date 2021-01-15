import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID')
    RESOURCE_GROUP = os.getenv('RESOURCE_GROUP')
    ACCOUNT_ID = os.getenv('ACCOUNT_ID')
    AAD_TENANT_ID = os.getenv('AAD_TENANT_ID')
    AAD_CLIENT_ID = os.getenv('AAD_CLIENT_ID')
    AAD_SECRET = os.getenv('AAD_SECRET')
    SECRET_KEY = os.getenv('SECRET_KEY')
