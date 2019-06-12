from flask import Blueprint

cms_bp = Blueprint('cms', __name__)

from apps.cms import index_view
from apps.cms import seller_view
from apps.cms import shop_view
