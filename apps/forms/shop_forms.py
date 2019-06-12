from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DecimalField, SelectField
from wtforms import validators


# 商家店铺验证类
from wtforms.widgets import HiddenInput

from apps.models.shop_model import MenuCategory


class SellerShopForm(FlaskForm):
    # 店铺名称
    shop_name = StringField(
        label="店铺名称",
        validators=[
            validators.DataRequired(message="请输入店铺名称"),
            validators.Length(max=32, message="店铺名称不能超过32个字符"),
        ],
        render_kw={'class': 'form-control', 'placeholder': '请输入店铺名称'},
    )

    brand = BooleanField(label="品 牌", default=False)
    on_time = BooleanField(label="准时送达", default=False)
    fengniao = BooleanField(label="蜂鸟快递", default=False)
    bao = BooleanField(label="提供保险", default=False)
    piao = BooleanField(label="提供发票", default=False)
    zhun = BooleanField(label="准标识", default=False)

    start_send = DecimalField(
        label="起送价格",
        validators=[validators.DataRequired(message="填写起送价格")],
        render_kw={'class': 'form-control', 'placeholder': '请输入起送价格'},
    )
    send_cost = DecimalField(
        label="配送费用",
        validators=[validators.DataRequired(message="填写配送费用")],
        render_kw={'class': 'form-control', 'placeholder': '请输入配送费用'},
    )

    notice = StringField(
        label="店铺公告",
        validators=[validators.Length(max=128, message="不能超过128个字符")],
        render_kw={'class': 'form-control', 'placeholder': '请输入店铺公告'},
    )

    discount = StringField(
        label="优惠信息",
        validators=[validators.Length(max=128, message="不能超过128个字符")],
        render_kw={'class': 'form-control', 'placeholder': '请输入优惠信息'},
    )

    shop_img = StringField(label="店铺图片", id='image-input', widget=HiddenInput())

    def validate_start_send(self, obj):
        obj.data = float('{:.2f}'.format(obj.data))

    def validate_send_cost(self, obj):
        obj.data = float('{:.2f}'.format(obj.data))


# 菜品分类验证层
class MenuCategoryForm(FlaskForm):
    # 分类名称
    name = StringField(
        label="菜品分类名",
        validators=[
            validators.DataRequired(message="请输入菜品分类名"),
            validators.Length(max=32, message="不能超过32字符"),
        ],
        render_kw={'class': 'form-control', 'placeholder': '请输入菜品分类名'},
    )
    # 分类描述
    description = StringField(
        label="菜品分类描述",
        validators=[
            validators.Length(max=128, message="不能超过128字符"),
        ],
        render_kw={'class': 'form-control', 'placeholder': '请输入菜品分类描述'},
    )

    # 分类编号
    type_accumulation = StringField(
        label="菜品分类编号",
        validators=[
            validators.DataRequired(message="请输入菜品分类标记"),
            validators.Length(max=16, message="不能超过16字符"),
        ],
        render_kw={'class': 'form-control', 'placeholder': '请输入菜品分类编号'},
    )
    # 是否默认
    is_default = BooleanField(label="是否默认", default=False)

    def __init__(self, shop, *args, **kwargs):
        super(MenuCategoryForm, self).__init__(*args, **kwargs)
        self.shop = shop

    def validate_is_default(self, obj):
        m1 = MenuCategory.query.filter(
            MenuCategory.shop == self.shop,
            MenuCategory.is_default == True,
        ).first()
        if m1:
            obj.data = False


# 菜品信息验证层
class MenuFoodForm(FlaskForm):
    # 菜品名称
    goods_name = StringField(
        label="菜品名称",
        validators=[
            validators.DataRequired(message="请输入菜品分类名"),
            validators.Length(max=64, message="不能超过32字符"),
        ],
        render_kw={'class': 'form-control', 'placeholder': '请输入菜品名称'},
    )
    # 归属分类
    category_id = SelectField(
        label="菜品分类", coerce=int,
        render_kw={'class': 'form-control'},
    )
    # 菜品价格
    goods_price = DecimalField(
        label="菜品价钱", places=2,
        validators=[
            validators.NumberRange(min=0, max=999, message="价钱超出范围"),
            validators.DataRequired(message="请输入菜品价格"),
        ],
        render_kw={'class': 'form-control', 'placeholder': '请输入菜品价格'},
    )
    # 菜品提示信息
    tips = StringField(
        label="菜品提示信息",
        validators=[
            validators.Length(max=128, message="不能超过128个字符"),
        ],
        render_kw={'class': 'form-control', 'placeholder': '请输入提示信息'},
    )
    # 菜品图片
    goods_img = StringField(label="菜品图片", id='image-input', widget=HiddenInput())

    def validate_goods_price(self, obj):
        obj.data = float('{:.2f}'.format(obj.data))

    def __init__(self, shop, *args, **kwargs):
        super(MenuFoodForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(cate.id, cate.name) for cate in shop.categories]
