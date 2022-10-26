from flask import jsonify, Blueprint
from Models.model import Category

categories_Blueprint = Blueprint('categories', __name__, url_prefix='/categories')

@categories_Blueprint.route("/", methods=['GET'])
def get_categories():
    try:
        result = [x.as_dict() for x in Category.get_all_categories()]
        return jsonify({"success": True, "results": result, "message": "OK"}), 200
    except Exception as ex:
        return jsonify({"success": False, "results": [], "message": ex}), 500