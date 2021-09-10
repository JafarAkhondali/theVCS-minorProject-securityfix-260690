from flask import Flask, jsonify
from werkzeug.utils import import_string
import util


app = Flask(__name__)

# add all ml projects here
ml_box = {
    "Olympians Recognizer": "/clients/common/olympians_recognizer/app.html",
}

# add all tool box projects here
tool_box = {
}






########################## DON'T CHANGE CODE BELOW #####################################

@app.route('/', methods=['GET', 'POST'])
def home():
    response = jsonify({
        "title": "ML-TOOLBOX",
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/all_ml_projects", methods=["GET", "POST"])
def all_ml_projects():
    response = jsonify(ml_box)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/all_tool_projects", methods=["GET", "POST"])
def all_tool_projects():
    response = jsonify(tool_box)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

########################## DON'T CHANGE CODE ABOVE #####################################







############################## importing other servers below #############################

from projects.olympians_recognizer import server as olympians_recognizer # By Prince Mishra

############################## importing other servers above #############################



############################### All projects Below #############################

app.register_blueprint(olympians_recognizer.app) # By Prince Mishra

############################### All projects Above #############################








if __name__ == "__main__":
    print("Starting Python Flask Server For Sports Celebrity Image Classification")
    util.load_saved_artifacts()
    app.run(port=5000, debug=True)
