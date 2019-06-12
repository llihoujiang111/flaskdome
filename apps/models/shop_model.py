from apps.models import db, BaseModel


# 商家店铺信息表
class SellerShop(BaseModel):
    # 店铺对外ID号
    pub_id = db.Column(db.String(255), unique=True, index=True)
    # 店铺名称
    shop_name = db.Column(db.String(32), nullable=False, unique=True)
    # 店铺评分
    shop_rating = db.Column(db.Float, default=5.0)
    # 是否是品牌
    brand = db.Column(db.Boolean, default=False)
    # 是否准时送达
    on_time = db.Column(db.Boolean, default=False)
    # 是否蜂鸟配送
    fengniao = db.Column(db.Boolean, default=False)
    # 是否保险
    bao = db.Column(db.Boolean, default=False)
    # 是否有发票
    piao = db.Column(db.Boolean, default=False)
    # 是否准标识
    zhun = db.Column(db.Boolean, default=False)
    # 起送价格
    start_send = db.Column(db.Float, default=0.0)
    # 配送费
    send_cost = db.Column(db.Float, default=0.0)
    # 店铺logo图片
    shop_img = db.Column(db.String(128), default='')
    # 店铺公告
    notice = db.Column(db.String(128), default='')
    # 优惠信息
    discount = db.Column(db.String(128), default='')
    # 店铺和商家的关系
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_user.id'))
    # 建立反向查询关系
    seller = db.relationship("SellerUser", backref="stores")

    def __repr__(self):
        return '<shop {}>'.format(self.shop_name)

    def keys(self):
        return "shop_name", "shop_img", "brand", "on_time", "fengniao", "bao", \
               "piao", "zhun", "start_send", "send_cost", "notice", "discount"


# 菜品分类
class MenuCategory(BaseModel):
    # 分类名称
    name = db.Column(db.String(32))
    # 分类描述
    description = db.Column(db.String(128), default='')
    # 分类编号
    type_accumulation = db.Column(db.String(16))
    # 是否默认
    is_default = db.Column(db.Boolean, default=False)
    # 归属店铺
    shop_pid = db.Column(db.String(16), db.ForeignKey('seller_shop.pub_id'))

    shop = db.relationship('SellerShop', backref='categories')

    def keys(self):
        return "name", "description", "type_accumulation", "is_default"

    def __repr__(self):
        return "<MenuCate {}>".format(self.name)


# 菜品信息
class MenuFood(BaseModel):
    # 菜品名称
    goods_name = db.Column(db.String(64))
    # 菜品评分
    rating = db.Column(db.Float, default=5.0)
    # 归属店铺
    shop_id = db.Column(db.String(16), db.ForeignKey('seller_shop.pub_id'))
    # 归属分类
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'))
    cates = db.relationship('MenuCategory', backref='foods')    # 添加一条关系
    # 菜品价格
    goods_price = db.Column(db.Float, default=0.0)
    # 月销售额
    month_sales = db.Column(db.Integer, default=0)
    # 评分数量
    rating_count = db.Column(db.Integer, default=0)
    # 菜品提示信息
    tips = db.Column(db.String(128), default='')
    # 菜品图片
    goods_img = db.Column(db.String(128), default='')

    def keys(self):
        return "goods_id", "goods_name", "rating", "goods_price", "description", "tips", "month_sales", "goods_img"

    def __repr__(self):
        return "<Food: {} ￥{}>".format(self.food_name, self.food_price)