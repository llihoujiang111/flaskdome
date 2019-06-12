from apps.models import db, BaseModel


class OrderInfo(BaseModel):
    # 订单编号
    order_code = db.Column(db.String(32), unique=True)
    shop_pid = db.Column(db.String(16), db.ForeignKey('seller_shop.pub_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('buyer_user.id'))
    # 订单送货地址
    order_address = db.Column(db.String(128))
    # 订单价钱
    order_price = db.Column(db.Float, default=0)
    # 订单状态
    order_status = db.Column(db.Integer, default=0)
    # 订单产生时间
    created_time = db.Column(db.DateTime, onupdate=True)
    # 第三方交易号
    trade_sn = db.Column(db.String(128), default='')

    user = db.relationship('BuyerUser', backref='orders')
    shop = db.relationship('SellerShop', backref='orders')

    def keys(self):
        return 'order_address', 'order_price', 'order_code'

    def get_status(self):
        if self.order_status == 0:
            return "代付款"
        else:
            return "以付款"


# 订单的商品
class OrderGoods(BaseModel):
    order_id = db.Column(db.Integer, db.ForeignKey('order_info.id'))
    # 商品ID号
    goods_id = db.Column(db.Integer)
    # 商品名称
    goods_name = db.Column(db.String(64))
    # 商品图片
    goods_img = db.Column(db.String(128), default='')
    # 商品价钱
    goods_price = db.Column(db.Float)
    # 商品数量
    amount = db.Column(db.Integer)

    order = db.relationship('OrderInfo', backref='goods')

    def keys(self):
        return 'goods_id', 'goods_name', 'goods_price', 'amount', 'goods_img'
