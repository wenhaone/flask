from DBUtils.PooledDB import PooledDB, SharedDBConnection
import pymysql

class Config():
    SALT=b'dsafs'
    SECRET_KEY = 'asdf123sdfsdfsdf'
    MAX_CONTENT_LENGTH = 1024 * 1024 * 7


