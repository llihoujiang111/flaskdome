from apps import create_cms_app

cms_app = create_cms_app('apps.settings.CMSDevConfig')


if __name__ == '__main__':
    from apps.models import db
    with cms_app.app_context():
        # 在app上下文中，使用db对象进行数据表的新建
        db.create_all()
    # 运行flask自带测试web服务器
    cms_app.run(host="0.0.0.0",port=9999)
