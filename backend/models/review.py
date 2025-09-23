# Review model
class Review:
    def __init__(self, id, product_id, text, sentiment):
        self.id = id
        self.product_id = product_id
        self.text = text
        self.sentiment = sentiment
