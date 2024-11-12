from flask import Flask, request, jsonify,render_template,send_from_directory
from werkzeug.utils import secure_filename

import util
app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def hello():

    response = jsonify('hello')

    response.headers.add('Access-Control-Allow-Origin', '*')

    return  render_template('index.html')

app.config['static'] = "static"

# Define a route to serve static files (e.g., CSS and JS) from the specified directory
@app.route('/static/<path:filename>')
def get_assets(filename):
    # Ensure the filename is secure to prevent potential security issues
    filename = secure_filename(filename)
    # Use send_from_directory to send the static file to the client
    # as_attachment=False means the file will be displayed rather than downloaded
    return send_from_directory(app.config['static'], filename, as_attachment=False)


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
  
    app.run(debug=True)
