from flask import jsonify, request
from apps.apis import api_bp
from apps.models.shop_model import SellerShop


@api_bp.route('/shop_list/', endpoint='shop_showall', methods=['GET'])
def shop_showall():
    s = SellerShop.query.all()
    data = [{**dict(v), 'id': v.pub_id} for v in s]
    return jsonify(data)


@api_bp.route('/shop/', endpoint='shop_show', methods=['GET'])
def shop_show():
    pid = request.args.get('id')
    s = SellerShop.query.filter_by(pub_id=pid).first()
    shop = s.categories
    con = [{**dict(v), 'goods_list':[{**dict(i), 'goods_id': i.id} for i in v.foods]} for v in shop]
    data= {**dict(s),'pid': s.pub_id, 'commodity': con, 'evaluate': []}
    return jsonify(data)
