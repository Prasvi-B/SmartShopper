from flask import Blueprint, request, jsonify
from services.sentiment import analyze_sentiment
from services.recommender import recommend_site

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/api/reviews')
def review_analysis():
    product_id = request.args.get('productId')
    sentiments = analyze_sentiment(product_id)
    recommendation = recommend_site(product_id)
    return jsonify({'sentiments': sentiments, 'recommendation': recommendation})
