from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS
import numpy as np
import os
from traffic import traffic_sign

from utils import removeFiles

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')

app = Flask(__name__)
app.secret_key = "WERWERW$%WERW@#%(WWERTYTUU"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/traffic', methods=['POST'])
def trafficSignRecognition():
    try:
        # check if the post request has the file part
        if 'imageFile' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
        # Get File
        file = request.files['imageFile']
        
        if file.filename == '':
            resp = jsonify({'message' : 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        
        if file:
            filename = secure_filename(file.filename)
            status = removeFiles(UPLOAD_FOLDER)

            if status:
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(img_path)
                
                sign = traffic_sign(img_path)

                if sign and sign is not None and sign != '':
                    response = jsonify({
                        'status': 200, 
                        'message': 'Successfully Detected!',
                        'sign': sign
                        })
                    response.status_code = 200
                    return response
                else:
                    resp = jsonify({'message' : 'No Traffic Sign Predicted!', 'error': f'{err}'})
                    resp.status_code = 400
                    return resp

    except Exception as err:
        resp = jsonify({'message' : 'Error in file upload!', 'error': f'{err}'})
        resp.status_code = 500
        return resp





