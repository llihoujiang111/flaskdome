from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import validators

from apps.models.seller_model import SellerUser

# 用户登录
class LoginSellerForm(FlaskForm):
    # 商家注册用户名
    username = StringField(
        label="用户名",
        validators=(
            validators.InputRequired(message='请填写用户名'),
            validators.Length(min=3, message='用户名不能少于3个字符'),
            validators.Length(max=32, message='用户名不能多于32个字符'),
        ),
        render_kw={'class': 'form-control', 'placeholder': '请输入用户名'},
    )

    # 商家登录密码
    password = PasswordField(
        label='登录密码',
        validators=(
            validators.InputRequired(message='请填写登录密码'),
            validators.Length(min=3, message='密码不能少于3个字符'),
            validators.Length(max=16, message='密码字符多于16个字符'),
        ),
        render_kw={'class': 'form-control', 'placeholder': '请输入登录密码'},
    )

# 用户注册
class RegisterSellerForm(LoginSellerForm):
    USER_ERROR = '该用户名已经被注册了'

    # 确认密码
    password1 = PasswordField(
        label='确认密码',
        validators=(
            validators.InputRequired(message='请填写确认密码'),
            validators.EqualTo('password', message="请输入相同的密码"),
        ),
        render_kw={'class': 'form-control', 'placeholder': '请输入确认密码'},
    )

    # 校验用户名是否唯一
    def validate_username(self, obj):
        u = SellerUser.query.filter_by(username=obj.data).first()
        if u:
            raise validators.ValidationError(message=self.USER_ERROR)
