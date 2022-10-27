from markupsafe import escape
from flask import jsonify, request, Blueprint
from Models.model import Product

products_Blueprint = Blueprint('products', __name__, url_prefix='/products')

@products_Blueprint.route("/", methods=['GET'])
def get_products():
    try:
        category_id = request.args.get('categoryID') or None
        if category_id:
            result = [x.as_dict() for x in Product.get_products_by_category_id(category_id)]
            return jsonify({"success": True, "results": result}), 200
        result = [x.as_dict() for x in Product.get_all_products()]
        return jsonify({"success": True, "results": result}), 200
    except Exception as ex:
        return jsonify({"success": False, "message": ex}), 500
    

@products_Blueprint.route("/", methods=['POST'])
def post_product():
    try:
        body = request.get_json()
        product_keys = ['name', 'price', 'quantity', 'category_id', 'img_url']
        for key in product_keys:
            if key not in body:
                return jsonify({"success": False, "message": f'{key} missing from body'}), 400
        if 'id' in body:
            del body['id']
        
        old_product = Product.get_product_by_name(body['name'])
        if old_product:
            return jsonify({"success": False, "results": old_product.as_dict(), "message": "Product already exists"}), 200
        
        new_product = Product.add_product(_name=body['name'], _price=body['price'], _quantity=body['quantity'], _img_url=body['img_url'], _category_id=body['category_id'])
        return jsonify({"success": True, "results": new_product.as_dict(), "message": "Product added successfully"}), 200
    except Exception as ex:
        return jsonify({"success": False, "message": ex}), 500
    

@products_Blueprint.route("/<int:id>", methods=['PATCH'])
def patch_product(id):
    try:
        old_product = Product.get_product_by_id(escape(id))
        if old_product:
            body = request.get_json()       
            if 'id' in body:
                del body['id']
            Product.update_product(old_product, body)
            return jsonify({"success": True, "results": old_product.as_dict(), "message": "Product updated successfully"}), 200
        
        return jsonify({"success": False, "message": "Product Not Found"}), 200
    except Exception as ex:
        return jsonify({"success": False, "message": ex}), 500
    

@products_Blueprint.route("/<int:id>", methods=['PUT'])
def put_product(id):
    try:
        body = request.get_json()  
             
        product_keys = ['name', 'price', 'quantity', 'category_id', 'img_url']
        for key in product_keys:
            if key not in body:
                return jsonify({"success": False, "message": f'{key} missing from body'}), 400
            
        if 'id' in body:
            del body['id']
            
        result = Product.replace_product(escape(id), body['name'], body['price'], body['quantity'], body['img_url'], body['category_id'])
        if result:
            return jsonify({"success": True, "results": result.as_dict(), "message": "Product updated successfully"}), 200
        return jsonify({"success": False, "message": "Product Not Found"}), 200
    except Exception as ex:
        return jsonify({"success": False, "message": ex}), 500


@products_Blueprint.route("/<int:id>", methods=['GET'])
def get_product_byId(id):
    try:
        result = Product.get_product_by_id(escape(id))
        if result:
            result = result.as_dict()
            return jsonify({"success": True, "result": result}), 200
        return jsonify({"success": False, "message": "Product Not Found"}), 200
    except Exception as ex:
        return jsonify({"success": False, "message": ex}), 500
    

@products_Blueprint.route("/<int:id>", methods=['DELETE'])
def delete_product(id):
    try:
        Product.delete_product(escape(id))
        return jsonify({"success": True, "result": {}, "message": "Product deleted successfully"}), 200
    except Exception as ex:
        return jsonify({"success": False, "message": ex}), 500