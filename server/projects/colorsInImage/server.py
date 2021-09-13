from flask import Blueprint, jsonify, request
from projects.colorsInImage import util
app = Blueprint('app_colorsInImage', __name__)

@app.route("/colorsInImage_getColors", methods=["POST"])
def colorsInImage_getColors():
    image_data = request.form['image_data']
    response = jsonify(util.getColors(image_data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
