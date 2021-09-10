from flask import Blueprint, jsonify, request
from projects.olympians_recognizer import util
app = Blueprint('app_olympians_recognizer', __name__)

@app.route("/olympians_recognizer_olympians_name", methods=["POST"])
def olympians_recognizer_olympians_name():
    response = jsonify(util._names)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/olympians_recognizer_classify_image', methods=['GET', 'POST'])
def olympians_recognizer_classify_image():
    image_data = request.form['image_data']

    response = jsonify(util.classify_image(image_data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
