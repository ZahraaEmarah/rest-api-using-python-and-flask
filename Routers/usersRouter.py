from flask import jsonify, request, Blueprint
from Models.model import User

users_Blueprint = Blueprint('users', __name__, url_prefix='/user')

@users_Blueprint.route("/login", methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify({"success": False, "message": 'Missing arguments'}), 400
    user = User.get_user_by_username(username)
    verified = user.verify_password(password)
    if verified:
        return jsonify({"success": True, "message": 'Login successful'}), 200
    return jsonify({"success": False, "message": 'Wrong Credentials'}), 200


@users_Blueprint.route("/register", methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify({"success": False, "message": 'Missing arguments'}), 400
    if User.query.filter_by(username = username).first() is not None:
        return jsonify({"success": False, "message": 'User already exists'}), 400
    user = User.add_user(username, password)
    return jsonify({"success": True, "message": 'Registeration successful', "username": user.as_dict()}), 201