import sys
sys.path.append("./Web")

from app import db

class Products(db.Model):
    asin = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    deal = db.Column(db.Integer)
    cat = db.Column(db.String())
    subcat = db.Column(db.String())
    rating = db.Column(db.Float)
    nVotes = db.Column(db.Integer)
    availability = db.Column(db.String())
    imageURL = db.Column(db.String())
    url = db.Column(db.String(), nullable=False)

    prices = db.relationship("Prices", backref="product", lazy=True)
    emails = db.relationship("Emails", backref="product", lazy=True)

    def __repr__(self):
        # how object print when printing it out
        return f"Product: {self.name}"

class Prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(), db.ForeignKey("products.asin"), nullable=False)
    price = db.Column(db.Float)
    datetime = db.Column(db.DateTime)

class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(), db.ForeignKey("products.asin"), nullable=False)
    userEmail = db.Column(db.String(), nullable=False)