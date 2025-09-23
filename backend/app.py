from flask import Flask
from routes.product import product_bp
from routes.reviews import reviews_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(product_bp)
app.register_blueprint(reviews_bp)

if __name__ == '__main__':
    app.run(debug=True)
