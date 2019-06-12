from datetime import datetime
import time
import json
from flask import jsonify, request, current_app, g, redirect, make_response
from apps.apis import api_bp
from apps.apis.buyer_api import sess
from apps.models.shop_model import MenuCategory, MenuFood, SellerShop, db
from apps.models.cart_model import OrderGoods, OrderInfo
from apps.models.buyer_model import BuyerUser, AddressUser
from apps.libs.uid_helper import showcreate_order, generate_shop_uuid
from alipay import AliPay


def claer_car(uid):
    api_redis = current_app.config.get("API_REDIS")
    res = api_redis.hgetall(uid)
    if res:
        api_redis.delete(uid)


def get_car(uid):
    api_redis = current_app.config.get("API_REDIS")
    goods = api_redis.hgetall(uid)
    return goods


# 添加购物车
@api_bp.route('/cart/', methods=['POST'])
@sess
def add_cart():
    goodslist = request.form.getlist("goodsList[]")
    goodscount = request.form.getlist("goodsCount[]")
    api_redis = current_app.config.get("API_REDIS")
    if len(goodslist) and len(goodscount):
        uid = g.uid
        claer_car(uid)
        for v, k in zip(goodslist, goodscount):
            f = MenuFood.query.get(v)
            gl = {
                "goods_name": f.goods_name,
                "goods_img": f.goods_img,
                "amount": k,
                "goods_price": f.goods_price,
                "shop_pid": f.shop_id
            }
            api_redis.hset(uid, v, json.dumps(gl))
            api_redis.expire(uid, current_app.config.get("CART_LIFETIME", 4000))
        data = {
            "status": "true",
            "message": "添加成功"
        }
        return jsonify(data)
    else:
        return jsonify({"status": "false",
                        "message": "添加失败"})


# 获取购物车
@api_bp.route('/cart/', methods=['GET'])
@sess
def get_cart_goods():
    uid = g.uid
    goods = get_car(uid)
    totalcost = 0
    res = []
    for v, gl in goods.items():
        gsl = json.loads(gl)
        gsl['goods_id'] = int(v)
        totalcost += (int(gsl['amount']) * gsl['goods_price'])
        res.append(gsl)
    data = {
        "goods_list": res,
        "totalCost": totalcost
    }
    return jsonify(data)


# 添加订单
@api_bp.route('/order/', methods=['POST'])
@sess
def add_order():
    uid = g.uid
    orderi = OrderInfo(user_id=uid)
    # 构造地址
    addressid = request.form.get("address_id")
    addr = AddressUser.query.get(int(addressid))
    res = [addr.provence, addr.city, addr.area, addr.detail_address]
    # 构造价格
    goods = get_car(uid)
    totalcost = 0
    # 构造订单编号
    orcode = showcreate_order(uid)
    for v, gl in goods.items():
        gsl = json.loads(gl)
        pid = gsl["shop_pid"]
        totalcost += (int(gsl['amount']) * gsl['goods_price'])
        orderi.goods.append(
            OrderGoods(
                goods_id=int(v),
                goods_name=gsl['goods_name'],
                goods_img=gsl['goods_img'],
                goods_price=gsl['goods_price'],
                amount=int(gsl['amount'])))
    # 添加
    orderi.order_code = orcode
    orderi.order_address = "".join(res)
    orderi.order_price = totalcost
    orderi.created_time = datetime.now()
    orderi.trade_sn = generate_shop_uuid()
    orderi.shop_pid = pid
    db.session.add(orderi)
    db.session.commit()
    claer_car(uid)
    data = {
        "status": "true",
        "message": "添加成功",
        "order_id": orderi.id
    }
    return jsonify(data)


# 得到指定订单
@api_bp.route('/order/', methods=['GET'])
@sess
def get_order():
    ordercode = request.args.get('id')
    order = OrderInfo.query.filter_by(id=ordercode).first()
    shop = order.shop
    orderg = order.goods
    data = {
        **dict(order),
        "id": order.id,
        "order_birth_time": order.created_time.strftime("%Y-%m-%d %H:%M"),
        "order_status": order.get_status(),
        "shop_id": shop.id,
        "shop_name": shop.shop_name,
        "shop_img": shop.shop_img,
        "goods_list": [dict(v) for v in orderg],
        "trade_sn": order.trade_sn
    }
    return jsonify(data)


# 获取订单列表
@api_bp.route('/orders/', methods=['GET'])
@sess
def get_order_list():
    uid = g.uid
    orderi = OrderInfo.query.filter_by(user_id=uid).all()
    data = [{**dict(v),
             "id": v.id,
             "order_birth_time": v.created_time.strftime("%Y-%m-%d %H:%M"),
             "order_status": v.get_status(),
             "shop_id": v.shop.id,
             "shop_name": v.shop.shop_name,
             "shop_img": v.shop.shop_img,
             "goods_list": [dict(i) for i in v.goods]}
            for v in orderi]
    return jsonify(data)

#
# @api_bp.route('/pay.php/', methods=['POST'])
# @sess
# def pay_aa():
#     uid = g.uid
#     u = BuyerUser.query.get(uid)
#     orders = u.orders
#     for v in orders:
#         # 查询订单信息
#         # 订单总金额
#         total = v.order_price
#         brief = "李爸爸商城支付"
#
#         app_private_key_string = "-----BEGIN RSA PRIVATE KEY-----MIIEogIBAAKCAQEAuTMTdZA8XIrss16bJkp0Twd2ohBjxiZjg8l90hoH2WKpF2+Eh1fiUEka6gKIvfCFD1lHm0A5O7XrdghrxmB/mzG6iO2GiNw4h9bw7VMMO8S/vnyfz2W4S+F+U5rJkTAUGKkIFp79lPgFgHyoGqlNgNZOdqUAj3EygYVOjt89RnpHWoxsnMSRIt+RINJNJgvlGOEFalh21GYNQpBHKY84RLVTKCY/OqWtezSGsfXCCNZKYLBFS09/P7a73gNH0BbpPFlO4+URvBGwgUDpYQbVxrWuaU/uRySAlZmWzme3u0KZnwUpFhOXm0IMTzbIcio783IlUzC8QM0Ldx/JuZu6xQIDAQABAoIBAAfZrGd9V7GsieAIkJcM7OU0scio3THXCrzZW6X+SHrkfbpqlbmO9h7lGmj09ormmR1PcYOZM1PeoD5+mOLt0Drp3rhTKTK/8v1/FPNaY9hcvKv8aGHINAmzY0Fz/DtVSGTLNXaQAru/z6vknNOUfZ6KdwT8dYufBr8KwYu41sYX8kuyuRSg3TH7iYgr0WhDtGVYlLm5X9XKuRpGJP82y0phhbe8FTy2GkDzmUz7jseRPaJzPn+bICzlqSyAUd+oUj5gUQzUVAvFIjWQZ5VE7+2YNxinlIa42Q6VEio4g3QB00fr06PzmVArVtCY/mK+W09tewhi4p9pRS7zSP7idAECgYEA7QI2xOLp8ZWwjpU/6cGc4l7Tp3N23tPPwLSNGfwxos8/MOGSp6aICf3aU5+eVKdIxaKluSds8439lF6mZ6F47F1HzL8nHOc0qG/L7hen/wAbbNkQW40wP2WFKH/tqXuYkMB5v2yf00vFmS1CDPmIIkZPwWHIN6rTDRYvrrBzkIECgYEAyAoYZOIJoyjapJOOjoMcMl1w4qLULhqF0D25hYS+2bpRFFZCxt8wWU1DI1okNlq7TL310VxRJiPSxCRc11Zou5AiVUBx8SLmbtiiZja1KvRMDAjn61lvk0GTt4p/bjlHrmYXV0B346nrfr/sWROQxUjMpWI17OATvdn7uMkRyEUCgYAm8BktaZZDwXL7SdvxPITYz/l35klePHBCWadg4IULGX9pOXYNoxdwhMsst+mcQMt85MbTT33f2bESgiZWmjmyo3SbV8BGSFnnXk6jtDE+fLcEv/inAeAuWjBxQes6z/p1tZmK8H6liSpSixPx68EI2IJb5AOv2ZnI6Z811Pl3gQKBgFogKkNxj7QCGRgjHwxYR+DtNon1oLEw4+8hkC920mHYTuVhw+5D6k2hwMjxuPUARfjacSElfa44X6JdW7LtTHyNANr2ER/6gGWalviEV3WF4alebdccUWfAGOSNssIfbotFleiKtDlPejl+EOdFKGmqVgGBURhrEJnt1zq25JsdAoGAHivgMsy2WCIspS9FVkXnteCkiFdfd1UFyeFCtFn/80kLOCxMlpJUzvaodrLpMV230kTvZpX7d9JSHDNjoBS9m1hEwxw2Yywk/+q5RzzvDlYMAxQnXLjT3jOCv2Nn0WLBcJf/+akNLq/RrMwyaWrtRZMC0CiLBXtB41AmTCH1zpY=-----END RSA PRIVATE KEY-----"
#         # app_private_key_string = open("private_key.text").read()
#         # alipay_public_key_string = open("all_public_key.text").read()
#         alipay_public_key_string = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy7THDM1+M5DXEdhi4cZoCSrwZDje81ZYTirX1qUS6NN6IB+zuAKpQNsIwDh3yksj2enEHP9Vdmth6+rfuBLbJfWtpBdAvYXaI6Ss3ABJqzwvPzIYy0JuvAC2lCTCgnm/7MrNcJKAStvqMX1SmvWVBSD2MJXMVuAgE6Dw0flkUKE45wkPy85v5LvStBwQI2WJlxyDvhiaVreVWMf2aKQMXKnHxPnr/HhYOx/avVs9XRSGxxY8snJPS9iHGULDkz5t99oCBZ7SOO/+X6kMYAjuqrZnlpeKANNEPUpm2b08CBszlO6Zg/OW+ZJKzvwTNXL3t81PopVFq+Ds3NgY9tx2IwIDAQAB-----END PUBLIC KEY-----"
#         # 创建对象
#
#         alipay = AliPay(
#             appid="2016092300577098",
#             app_notify_url=None,  # 默认回调url
#             app_private_key_string=app_private_key_string,
#             # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#             alipay_public_key_string=alipay_public_key_string,
#             sign_type="RSA2",  # RSA 或者 RSA2
#             debug=False  # 默认False
#         )
#         order_string = alipay.api_alipay_trade_wap_pay(
#             out_trade_no=v.order_code,
#             total_amount=str(total),
#             subject=brief,
#             return_url="http://127.0.0.1:8080/pay.php",
#             notify_url=None  # 可选, 不填则使用默认notify url
#         )
#         return redirect("https://openapi.alipaydev.com/gateway.do?{}".format(order_string))
#
#
# # 支付
# @api_bp.route('/pay.php/', methods=['GET'])
# @sess
# def pay():
#     uid = g.uid
#     u = BuyerUser.query.get(uid)
#     orders = u.orders
#     # 发起一次支付查询,查看是否支付成功
#     # 发起支付, 生成了一个地址, 跳转到支付宝地址上
#     app_private_key_string = open("private_key.text").read()
#     alipay_public_key_string = open("all_public_key.text").read()
#
#     # 创建对象
#     alipay = AliPay(
#         appid="2016092300577098",
#         app_notify_url=None,  # 默认回调url
#         app_private_key_string=app_private_key_string,
#         # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#         alipay_public_key_string=alipay_public_key_string,
#         sign_type="RSA2",  # RSA 或者 RSA2
#         debug=True  # 默认False
#     )
#
#     # 获取参数
#     out_trade_no = orders.order_code
#
#     # check order status
#     paid = False
#     for i in range(3):
#         result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
#         if result.get("trade_status", "") == "TRADE_SUCCESS":
#             paid = True
#             break
#         else:
#             time.sleep(3)
#
#     if paid is False:
#         data = {
#             "message": "支付失败"
#         }
#     else:
#         # 支付成功
#         # 修改状态
#         orders.order_status = 1
#         db.session.add(orders)
#         db.session.commit()
#         # 渲染数据
#         data = {
#             "message": "支付成功"
#         }
#
#     # 支付成功之后返回的页面
#     return jsonify(data)
