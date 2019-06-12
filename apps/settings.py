
def get_redis_address():
    from redis import Redis
    return Redis(host="127.0.0.1", port=6545)
    # return Redis(host="47.97.199.234", port=6545)


class DevConfig:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:root123@127.0.0.1:3306/flaskpro?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class CMSDevConfig(DevConfig):
    # CSRF值加密的秘钥
    WTF_CSRF_SECRET_KEY = 'a1b1c'
    # session加密的秘钥
    SECRET_KEY = 'bba'

    SESSION_TYPE = 'redis'
    SESSION_REDIS = get_redis_address()


class APIDevConfig(DevConfig):
    SMS_LIFETIME = 300

    API_REDIS = get_redis_address()

    SECRET_KEY = 'elm-api'

    TOKEN_EXPIRES = 3600
    CART_LIFETIME=4000
