from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from apps.models import db, BaseModel


# 商家用户信息表
class SellerUser(BaseModel, UserMixin):
    username = db.Column(db.String(16), unique=True)
    _password = db.Column('password', db.String(128))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd_value):
        self._password = generate_password_hash(pwd_value)

    def check_password(self, val):
        return check_password_hash(self.password, val)

