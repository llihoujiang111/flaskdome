from flask import request, jsonify, current_app, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from functools import wraps

from apps.models.buyer_model import BuyerUser


# token认证装饰器
def token_require(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        # 判断cookie中是否有token信息
        token = request.cookies.get('token')
        if not token:
            return jsonify({'status': "false", 'message': '没有token'})
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return jsonify({'status': "false", 'message': '无效的token'})
        user_id = data.get('user_id')
        # 判断用户信息
        user = BuyerUser.query.get(user_id)
        if not user:
            return jsonify({'status': "false", 'message': '非法用户'})
        g.current_user = user
        return fn(*args, **kwargs)
    return decorated
