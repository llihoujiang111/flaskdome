from flask import request, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user
from apps.cms import cms_bp
from apps.forms.seller_forms import RegisterSellerForm, LoginSellerForm
from apps.models.seller_model import SellerUser, db


@cms_bp.route('/register/', endpoint='register', methods=['GET', 'POST'])
def seller_register():
    form = RegisterSellerForm(request.form)
    if request.method == 'POST' and form.validate():
        s1 = SellerUser()
        s1.set_attrs(form.data)
        db.session.add(s1)
        db.session.commit()
        return redirect(url_for('cms.login'))
    return render_template('CU_form.html', flags="商家注册", form=form)


@cms_bp.route('/login/', endpoint='login', methods=['GET', 'POST'])
def seller_login():
    form = LoginSellerForm(request.form)
    if request.method == 'POST' and form.validate():
        u1 = SellerUser.query.filter_by(username=form.username.data).first()
        if u1 and u1.check_password(form.password.data):
            login_user(u1)
            next_url = request.args.get('next', '')
            if not next_url.startswith('/'):
                next_url = url_for('cms.index')
            return redirect(next_url)
        form.password.errors = ['用户名或密码出错']
    return render_template('CU_form.html', flags="商家登陆", form=form)


@cms_bp.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('cms.index'))
