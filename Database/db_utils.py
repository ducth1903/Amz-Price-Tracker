import email_msg_utils
import sys
sys.path.append("..")               # root directory

from Web_app import db

asin_length_limit = 10

class Products(db.Model):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}

    asin = db.Column(db.String(asin_length_limit), primary_key=True, nullable=False)
    name = db.Column(db.Text)
    deal = db.Column(db.Integer)
    cat = db.Column(db.Text)
    subcat = db.Column(db.Text)
    rating = db.Column(db.Float)
    nVotes = db.Column(db.Integer)
    availability = db.Column(db.Text)
    imageURL = db.Column(db.Text)
    url = db.Column(db.Text, nullable=False)

    # prices = db.relationship("Prices", backref="product", lazy=True)
    # emails = db.relationship("Emails", backref="product", lazy=True)

    def __repr__(self):
        # how object print when printing it out
        return f"<Product: {self.asin}, {self.name}>"

    def to_dict(self):
        return {"ASIN": self.asin, "name": self.name, "isDeal": self.deal, 
            "cat1": self.cat, "cat2": self.subcat, "rating": self.rating,
            "nVotes": self.nVotes, "availability": self.availability,
            "imageURL": self.imageURL, "url": self.url}

class Prices(db.Model):
    __tablename__ = "prices"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(asin_length_limit), db.ForeignKey("products.asin", ondelete="CASCADE"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Price: {self.asin}>"

    def datetime_to_str(self):
        return self.datetime.strftime("%d/%m/%Y %H:%M:%S")

class Emails(db.Model):
    __tablename__ = "emails"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(asin_length_limit), db.ForeignKey("products.asin", ondelete="CASCADE"), nullable=False)
    userEmail = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Email: {self.asin}>"

########################## PRODUCTS ##########################
def get_all_products():
    products = Products.query.with_entities(Products.url).all()
    return products

def get_product_from_asin(product_asin):
    query_product = Products.query.filter_by(asin=product_asin).first()
    if query_product:
        return query_product.to_dict()
    else:
        # Product does not exist in database
        return None

def insert_product(product_info):
    new_prod = Products(
        asin=product_info[0],
        name=product_info[1],
        deal=product_info[2],
        cat=product_info[3],
        subcat=product_info[4],
        rating=product_info[5],
        nVotes=product_info[6],
        availability=product_info[7],
        imageURL=product_info[8],
        url=product_info[9]
    )
    db.session.add(new_prod)
    db.session.commit()

def delete_product(product_asin):
    Products.query.filter_by(asin=product_asin).delete()
    db.session.commit()

########################## PRICES ##########################
def get_price_from_asin(product_asin):
    query_price = Prices.query.filter_by(asin=product_asin).all()
    result_dict = {"ASIN": query_price[0].asin, "price": [], "datetime": []}
    for q in query_price:
        result_dict["price"].append(q.price)
        result_dict["datetime"].append(q.datetime_to_str())
    return result_dict

def insert_price(price_info):
    new_price = Prices(
        asin=price_info[0],
        price=price_info[1],
        datetime=price_info[2]
    )
    db.session.add(new_price)
    db.session.commit()

########################## EMAILS ##########################
def add_user_email(product_asin, user_email):
    new_email = Emails(
        asin=product_asin,
        userEmail=user_email
    )
    db.session.add(new_email)
    db.session.commit()

def remove_user_email(product_asin, user_email):
    row_to_remove = Emails.query.filter_by(asin=product_asin, userEmail=user_email).first()
    if row_to_remove:
        db.session.delete(row_to_remove)
        db.session.commit()

def alert_user_email(product_asin, product_name, product_price):
    list_emails = Emails.query.filter_by(asin=product_asin).all()
    for email in list_emails:
        email_msg_utils.email_alert(email.userEmail, product_asin, product_name, product_price)