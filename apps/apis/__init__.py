from flask import Blueprint

api_bp = Blueprint('apis', __name__, url_prefix='/api/v1')

from apps.apis import shop_api
from apps.apis import buyer_api
from apps.apis import cart_api
