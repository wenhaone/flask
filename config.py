#codeing : utf-8
import redis
class Config(object):
    #配置信息

    SECRET_KEY = "XHSOI*Y9dasf"

    #数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/ihome"

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    #redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    #flask-session配置
    SESSION_TYPE = "redis"

    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER =True #对cookie中session_id进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 60*60*24#session数据的有效期

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

config_map = {
    "develop":DevelopmentConfig,
    "product":ProductionConfig

}