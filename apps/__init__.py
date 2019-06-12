from flask import Flask


# 注册商家后台管理系统的蓝图业务
def register_cms_bp(app: Flask):
    from apps.cms import cms_bp
    app.register_blueprint(cms_bp)


# 绑定数据库服务对象
def register_db(app: Flask):
    from apps.models import db
    db.init_app(app)


# 绑定flask-login插件服务
def register_login_helper(app: Flask):
    from apps.libs.login_helper import login_manager
    login_manager.init_app(app)
    login_manager.login_view = 'cms.login'


# session的注册
def register_session(app: Flask):
    from flask_session import Session
    Session(app=app)


def create_cms_app(config_info: str):
    app = Flask(__name__)

    # app配置信息初始化，必须在所有绑定插件服务前调用
    app.config.from_object(config_info)
    # 加载私有配置信息
    app.config.from_object('apps.secret_config')

    # session存储位置修改
    register_session(app)

    # 数据库服务对象绑定
    register_db(app)

    # 用户登录管理工具对象绑定
    register_login_helper(app)

    # app加载需要的蓝图业务
    register_cms_bp(app)
    return app


# 注册API接口的蓝图
def register_api_bp(app: Flask):
    from apps.apis import api_bp
    app.register_blueprint(api_bp)


def create_api_app(config_object: str):
    app = Flask(__name__, static_folder='./web_client', static_url_path='')
    app.config.from_object(config_object)

    register_db(app)

    register_api_bp(app)

    return app
