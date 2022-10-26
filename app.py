from flask import Flask, jsonify, request
from Routers.productsRouter import products_Blueprint
from Routers.categoriesRouter import categories_Blueprint
from settings import *

app.register_blueprint(products_Blueprint)
app.register_blueprint(categories_Blueprint)

@app.route("/", methods=['GET'])
def status():
    return jsonify({"message": "OK"})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)