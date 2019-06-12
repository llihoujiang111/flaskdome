from flask import request, current_app, jsonify, g, make_response
from werkzeug.security import gen_salt
from apps.apis import api_bp
from apps.forms.buyer_forms import BuyerRegisterForm, BuyerLoginForm, AddressFrom
from apps.models.buyer_model import BuyerUser, db, AddressUser
from itsdangerous import TimedJSONWebSignatureSerializer as Tjws, SignatureExpired, BadSignature
from functools import wraps


# 注册
@api_bp.route('/register/', endpoint='register', methods=['POST'])
def register():
    b = BuyerRegisterForm(request.form)
    if b.validate():
        name = request.form.get('username')
        pwd = request.form.get('password')
        tel = request.form.get('tel')
        u = BuyerUser(username=name, password=pwd, tel=tel)
        db.session.add(u)
        db.session.commit()
        return jsonify({"status": "true", "message": "注册成功"})
    else:
        return jsonify({"status": "false",
                        "message": f"请填写正确数据{b.errors.get('username')}{b.errors.get('tel')}{b.errors.get('pwd')}{b.errors.get('sms')}"})


# 验证码
@api_bp.route('/sms/', methods=['GET'])
def get_cms():
    tel = request.args.get("tel")
    if tel:
        cms = gen_salt(4)
        api_redis = current_app.config.get('API_REDIS')
        api_redis.setex(tel, current_app.config.get('SMS_LIFETIME'), cms)
        return jsonify({"status": True, "message": f"获取短信验证码成功 : {cms}"})
    else:
        return jsonify({"status": False, "message": "获取验证码失败"})


# 登录
@api_bp.route('/login/', endpoint='login', methods=['POST'])
def login():
    if request.form:
        name = request.form.get('name')
        pwd = request.form.get('password')
        u = BuyerUser.query.filter_by(username=name).first()
        if u and u.check_password(pwd):
            s = Tjws('lhj545', expires_in=1000)
            res = s.dumps({'uid': u.id})
            data = {
                "status": "true",
                "message": "登录成功",
                "user_id": u.id,
                "username": name,
            }
            t = make_response(jsonify(data))
            t.set_cookie("lhjcook", res.decode('ascii'), max_age=3600)
            return t
    else:
        return jsonify({"status": False, "message": "失败"})


# 装饰器
def sess(old):
    @wraps(old)
    def new(*args, **kwargs):
        if 'cookie' in request.headers:
            tokens = request.cookies.get("lhjcook")
            s = Tjws('lhj545')
            try:
                data = s.loads(tokens)
            except SignatureExpired:
                return jsonify({"success": 2, "message": "时间过期"})
            except BadSignature:
                return jsonify({"success": 3, "message": "数据不合法"})
            uid = data.get('uid')
            g.uid = uid
            res = old(*args, **kwargs)
            return res
        else:
            return jsonify({"success": 5, "message": "数据不存在"})

    return new


# 展示地址
@api_bp.route('/address/', endpoint='address', methods=['GET'])
@sess
def get_address_list():
    uid = g.uid
    # print(uid)
    if request.args.get('id'):
        a = int(request.args.get('id'))
        # print(type(a))
        u = AddressUser.query.get(a)
        # print(u)
        data = {**dict(u), "id": a}
        return jsonify(data)
    u1 = AddressUser.query.filter_by(user_id=uid).all()
    if u1:
        data = [{**dict(k), "id": i + 1} for i, k in enumerate(u1)]
        return jsonify(data)
    else:
        return jsonify({"success": 4, "message": "数据不存在"})


# 添加地址
@api_bp.route('/address/', methods=['POST'])
@sess
def add_address():
    addresfrom = AddressFrom(request.form)
    if addresfrom.validate():
        uid = g.uid
        print(uid)
        if addresfrom.id.data:
            a = int(addresfrom.id.data)
            address = AddressUser.query.get(a)
            address.set_attrs(addresfrom.data)
            address.user_id = uid
            db.session.add(address)
            db.session.commit()
            data = {
                "status": "true",
                "message": "修改成功"
            }
            return jsonify(data)
        elif not addresfrom.id.data:
            address = AddressUser()
            address.set_attrs(addresfrom.data)
            address.user_id = uid
            db.session.add(address)
            db.session.commit()
        data = {
            "status": "true",
            "message": "添加成功"
        }
        return jsonify(data)
    else:
        return jsonify({"status": "false", "message": "数据不合法"})


# 修改密码
@api_bp.route('/password/', methods=['POST'])
@sess
def change_password():
    id = g.uid
    b = BuyerUser.query.get(id)
    if b.password == request.form.get('oldPassword'):
        b.password = request.form.get('newPassword')
        db.session.add(b)
        db.session.commit()
        return jsonify({
            "status": "true",
            "message": "修改成功"
        })
    else:
        return jsonify({
            "status": "false",
            "message": "修改失败"
        })


# 忘记密码
@api_bp.route('/new_password/', methods=['POST'])
def forget_password():
    tel = request.form.get('tel')
    b = BuyerUser.query.filter_by(tel=tel).first()
    if b:
        b.password = request.form.get('password')
        db.session.add(b)
        db.session.commit()
        return jsonify({
            "status": "true",
            "message": "修改成功"
        })
    else:
        return jsonify({
            "status": "false",
            "message": "修改失败"
        })
