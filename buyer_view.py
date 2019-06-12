from flask import jsonify
from apps.demo_apis import api_bp


# 短信验证码api
@api_bp.route('/sms/', methods=['GET'])
def get_cms():
    data = {
        "status": True,
        "message": "获取短信验证码成功"
    }
    return jsonify(data)


# 买家用户注册api
@api_bp.route('/register/', endpoint='register', methods=['POST'])
def register():
    data = {
        "status": "true",
        "message": "注册成功"
    }
    return jsonify(data)


# 登陆api
@api_bp.route('/login/', endpoint='login', methods=['POST'])
def login():
    data = {
        "status": "true",
        "message": "登录成功",
        "user_id": "1",
        "username": "张三"
    }
    return jsonify(data)


# 收获地址api
@api_bp.route('/address/', endpoint='address', methods=['GET'])
def get_address_list():
    data = [
        {
            "id": "1",
            "provence": "四川省",
            "city": "成都市",
            "area": "武侯区",
            "detail_address": "四川省成都市武侯区天府大道56号",
            "name": "张三",
            "tel": "18584675789"
        },
        {
            "id": "2",
            "provence": "河北省",
            "city": "保定市",
            "area": "武侯区",
            "detail_address": "四川省成都市武侯区天府大道56号",
            "name": "张三",
            "tel": "18584675789"
        }
    ]
    return jsonify(data)


# 新增地址API
@api_bp.route('/address/', methods=['POST'])
def add_address():
    data = {
        "status": "true",
        "message": "添加成功"
    }
    return jsonify(data)


# 修改密码接口
@api_bp.route('/password/', methods=['POST'])
def change_password():
    data = {
      "status": "true",
      "message": "修改成功"
    }
    return jsonify(data)


# 忘记密码接口
@api_bp.route('/new_password/', methods=['POST'])
def forget_password():
    data = {
      "status": "true",
      "message": "添加成功"
    }
    return jsonify(data)
