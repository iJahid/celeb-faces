from flask import Flask, request, jsonify
import util

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():

    response = jsonify('hello')

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/get_celeb_names')
def get_celeb_names():
    response = jsonify({'location': util.get_celeb_names()})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/classify_image', methods=['GET', 'POST'])
def classify_image():
    image_data = request.form['image_data']

    response = jsonify(util.classify_image(image_data))

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Sports Celebrity Image Classification")
    util.load_artifacts()
    app.run(port=5000)
