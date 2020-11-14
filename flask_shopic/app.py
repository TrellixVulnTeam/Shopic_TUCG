import os
from flask import Flask,flash, request, redirect, url_for, jsonify
from flask import render_template
from werkzeug.utils import secure_filename
import base64

from google.cloud import vision
import google_api as g

app = Flask(__name__)

project_id='shopic'
location='us-east1'
product_set_id='product_set0'

UPLOAD_FOLDER = os.path.join(os.getcwd(),'img')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    # image = g.get_reference_image(project_id,location,'product_id94','image94')
    # uri = image.uri.replace('gs://','https://storage.googleapis.com/')
    # print(f'the uri is: {uri}')
    # hello="no"
    # g.list_products(project_id,location)
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #above is normal file upload saving to img directory

            # Under is calling google API
            results = g.get_similar_products_file(project_id,
            location, 
            product_set_id,
            'apparel-v2',
            (os.path.join(app.config['UPLOAD_FOLDER'], filename)), 
            'style = women')

            return jsonify({'called':'true'})
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))

def encode_image(image):
  image_content = image.read()
  return base64.b64encode(image_content)