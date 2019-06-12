from werkzeug.security import generate_password_hash, check_password_hash
from apps.models import db, BaseModel


class BuyerUser(BaseModel):
    # 买家用户名
    username = db.Column(db.String(32), unique=True)
    # 买家密码
    _password = db.Column("password", db.String(128))
    # 买家电话号码
    tel = db.Column(db.String(16), unique=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, raw_pwd):
        return check_password_hash(self._password, raw_pwd)

    def __repr__(self):
        return "<Buyer: {}>".format(self.username)


class AddressUser(BaseModel):
    # 收货人姓名
    name = db.Column(db.String(20))
    # 收货人电话
    tel = db.Column(db.String(16))
    # 省
    provence = db.Column(db.String(20))
    # 市
    city = db.Column(db.String(20))
    # 区
    area = db.Column(db.String(20))
    # 详细地址
    detail_address = db.Column(db.String(100))
    # 关联用户表
    user_id = db.Column(db.Integer, db.ForeignKey("buyer_user.id"))
    buyeruser = db.relationship('BuyerUser', backref='address')

    def keys(self):
        return "name", "tel", "provence", "city", "area", "detail_address"

    def __repr__(self):
        return self.provence
