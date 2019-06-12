from apps import create_api_app

api_app = create_api_app('apps.settings.APIDevConfig')


if __name__ == '__main__':
    from apps.models import db
    with api_app.app_context():
        db.create_all()
    api_app.run(port=8080)
