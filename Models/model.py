from settings import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
import json

db = SQLAlchemy(app)

class Category(db.Model):
    __tablename__ = 'category'
    id= db.Column(db.Integer, primary_key=True, nullable=False)
    name= db.Column(db.String(500), nullable=False)

    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self):
        category_obj = {
            'name': self.name 
        }
        return json.dumps(category_obj)
    
    def get_all_categories():
        return Category.query.all()
    
    def add_category(_id, _name):
        new_category = Category(id=_id, name=_name)
        db.session.add(new_category)
        db.session.commit()
        return new_category


class Product(db.Model):
    __tablename__ = 'products'
    id= db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name= db.Column(db.String(500), unique=True, nullable=False)
    price= db.Column(db.Float, nullable=False)
    quantity= db.Column(db.Float)
    img_url= db.Column(db.String(300))
    cateogry_id= db.Column(db.Integer, ForeignKey('category.id'), index=True,nullable=False)

    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self):
        product_obj = {
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'img_url': self.img_url,
            'category_id': self.cateogry_id 
        }
        return json.dumps(product_obj)
    
    def get_all_products():
        return Product.query.all()
    
    def get_product_by_id(_id):
        return Product.query.filter_by(id=_id).first()
    
    def get_product_by_name(_name):
        return Product.query.filter_by(name=_name).first()
    
    def get_products_by_category_id(_cat_id):
        return Product.query.filter_by(cateogry_id=_cat_id).all()
    
    def add_product(_name, _price, _quantity, _img_url, _category_id):
        new_product = Product(name=_name, price=_price, quantity=_quantity, img_url=_img_url, cateogry_id=_category_id)
        db.session.add(new_product)
        db.session.commit()
        return new_product
    
    def update_product(old_product, new_product_obj):
        for property in new_product_obj:
            if property in old_product.as_dict():
                setattr(old_product, property, new_product_obj[property])
        db.session.commit()
        
    def replace_product(_id, _name, _price, _quantity, _img_url, _category_id):
        product_to_replace = Product.query.filter_by(id=_id).first()
        product_to_replace.name = _name
        product_to_replace.price = _price
        product_to_replace.quantity = _quantity
        product_to_replace.img_url = _img_url
        product_to_replace.cateogry_id = _category_id
        db.session.commit()
        return product_to_replace
        
    def delete_product(_id):
        try:
            Product.query.filter_by(id=_id).delete()
            db.session.commit()
            return True
        except:
            return False