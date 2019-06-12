from flask import request, redirect, url_for, render_template, abort
from flask_login import login_required, current_user
from apps.forms.shop_forms import SellerShopForm, MenuCategoryForm, MenuFoodForm
from apps.libs.uid_helper import generate_shop_uuid
from apps.models.shop_model import SellerShop, db, MenuCategory, MenuFood
from apps.cms import cms_bp


# 验证店铺ID是否正确
def check_shop_pid(shop_pid):
    s1 = SellerShop.query.filter(
        SellerShop.pub_id == shop_pid,
        SellerShop.seller == current_user
    ).first()
    return s1 or abort(404)


# 获得店铺对应的分类对象
def check_shop_cate(shop, cate_id):
    for cate in shop.categories:
        if cate.id == cate_id:
            return cate
    abort(404)


# 获取菜品对应的对象
def check_shop_food(shop, food_id):
    food = MenuFood.query.filter(MenuFood.shop_id == shop.pub_id, MenuFood.id == food_id).first()
    if not food:
        abort(404)
    return food


# 店铺管理
@cms_bp.route('/add_shop/', endpoint='add_shop', methods=['GET', 'POST'])
@login_required
def seller_add_shop():
    form = SellerShopForm(request.form)
    if request.method == 'POST' and form.validate():
        s1 = SellerShop()
        s1.set_attrs(form.data)
        s1.seller = current_user
        s1.pub_id = generate_shop_uuid()
        db.session.add(s1)
        db.session.commit()
        return redirect(url_for('cms.index'))
    return render_template('CU_form.html', flags="店铺添加", form=form, img=True)


@cms_bp.route('/update_shop/<shop_pid>/', endpoint='update_shop', methods=['GET', 'POST'])
@login_required
def seller_update_shop(shop_pid):
    shop = check_shop_pid(shop_pid)
    form = None
    if request.method == 'GET':
        form = SellerShopForm(data=dict(shop))
    elif request.method == 'POST':
        form = SellerShopForm(request.form)
        if form.validate():
            shop.set_attrs(form.data)
            db.session.commit()
            return redirect(url_for('cms.index'))
    return render_template('CU_form.html', flags="店铺更新", form=form, img=True)


# 分类管理
@cms_bp.route('/add_cate/<shop_pid>/', endpoint='add_cate', methods=['GET', 'POST'])
@login_required
def seller_add_cate(shop_pid):
    s1 = check_shop_pid(shop_pid)
    form = MenuCategoryForm(s1, request.form)
    if request.method == 'POST' and form.validate():
        m1 = MenuCategory()
        m1.set_attrs(form.data)
        m1.shop = s1
        db.session.add(m1)
        db.session.commit()
        return redirect(url_for('cms.index'))
    return render_template('CU_form.html', flags="分类添加", form=form)


@cms_bp.route('/update_cate/<shop_pid>/<int:cate_id>/', endpoint='update_cate', methods=['GET', 'POST'])
@login_required
def seller_update_cate(shop_pid, cate_id):
    s1 = check_shop_pid(shop_pid)
    cate = check_shop_cate(s1, cate_id)
    form = None
    if request.method == 'GET':
        form = MenuCategoryForm(s1, data=dict(cate))
    elif request.method == 'POST':
        form = MenuCategoryForm(s1, request.form)
        if form.validate():
            cate.set_attrs(form.data)
            db.session.commit()
            return redirect(url_for('cms.index'))
    return render_template('CU_form.html', flags="分类更新", form=form)


@cms_bp.route('/show_cate/<shop_pid>/', endpoint='show_cate', methods=['GET', 'POST'])
@login_required
def seller_show_cate(shop_pid):
    s1 = check_shop_pid(shop_pid)
    result = [{
        'name': cate.name,
        'id': cate.id,
        'total': len(cate.foods),
        'average': '%.2f' % (
                sum([food.goods_price for food in cate.foods]) /
                (len(cate.foods) if len(cate.foods) > 0 else 1)
        ),
    } for cate in s1.categories]
    return render_template('cate_show.html', shop=s1, cates=result)


# 菜品管理
@cms_bp.route('/add_food/<shop_pid>/', endpoint='add_food', methods=['GET', 'POST'])
@login_required
def seller_add_food(shop_pid):
    s1 = check_shop_pid(shop_pid)
    form = MenuFoodForm(s1, request.form)
    if request.method == 'POST' and form.validate():
        m1 = MenuFood()
        m1.set_attrs(form.data)
        m1.shop_id = s1.pub_id
        db.session.add(m1)
        db.session.commit()
        return redirect(url_for('cms.index', shop_pid=shop_pid))
    return render_template('CU_form.html', flags='菜品添加', form=form, img=True)


@cms_bp.route('/update_food/<shop_pid>/<food_id>/', endpoint='update_food', methods=['GET', 'POST'])
@login_required
def seller_show_food(shop_pid, food_id):
    s1 = check_shop_pid(shop_pid)
    food = check_shop_food(s1, food_id)
    form = None
    if request.method == 'GET':
        form = MenuFoodForm(s1, data=dict(food))
        form.category_id.data = food.category_id
    elif request.method == 'POST':
        form = MenuFoodForm(s1, request.form)
        if form.validate():
            food.set_attrs(form.data)
            db.session.commit()
            return redirect(url_for('cms.index', shop_pid=shop_pid))
    return render_template('CU_form.html', shop=s1, flags="菜品更新", form=form, img=True)


@cms_bp.route('/show_food/<shop_pid>/', endpoint='show_food', methods=['GET', 'POST'])
@login_required
def seller_show_food(shop_pid):
    s1 = check_shop_pid(shop_pid)
    items = [(x.name, x.foods) for x in s1.categories]
    return render_template('food_show.html', shop=s1, items=items)
