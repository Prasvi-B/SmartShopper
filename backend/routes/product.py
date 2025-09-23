from flask import Blueprint, request, jsonify
from services.scraper import get_prices

product_bp = Blueprint('product', __name__)

@product_bp.route('/api/product')
def product_search():
    query = request.args.get('query')
    prices = get_prices(query)
    return jsonify({'id': query, 'prices': prices})
