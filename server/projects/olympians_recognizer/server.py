from flask import Blueprint, render_template, session,abort, jsonify
from projects.olympians_recognizer import util
app = Blueprint('app_olympians_recognizer', __name__)

@app.route("/olympians_recognizer_olympians_name", methods=["POST"])
def olympians_recognizer_olympians_name():
    response = jsonify(util._olympians_recognizer_index)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

