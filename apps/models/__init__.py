from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 数据模型基类，所有表都支持id和status字段
class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, default=1)

    # 将form.data字典结构，循环赋值给数据模型对象的属性
    def set_attrs(self, attrs: dict):
        for k, v in attrs.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)


from apps.models import seller_model
from apps.models import shop_model
from apps.models import cart_model
from apps.models import buyer_model