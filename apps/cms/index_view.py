from flask import render_template, jsonify, request, current_app
from flask_login import login_required, current_user
from qiniu import Auth
from apps.cms import cms_bp


@cms_bp.route('/', endpoint='index')
def cms_index():
    if current_user.is_authenticated:
        stores = current_user.stores
        return render_template('index.html', stores=stores)
    return render_template('index.html')


@cms_bp.route('/uptoken/', endpoint='uptoken')
@login_required
def qiniu_token():
    access_key = 'mmTxxgnkPLW5E-aId-EJA7-PNeK5xygrsN2QryOT'
    secret_key = current_app.config.get('QINIU_SECRET_KEY')
    space = request.args.get('space', '')

    token = ''
    if space and secret_key:
        q = Auth(access_key=access_key, secret_key=secret_key)
        token = q.upload_token(space)

    return jsonify({"uptoken": token})
