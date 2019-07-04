# coding: utf-8
import resume_parser
from flask import Flask, json
from flask_cors import CORS, cross_origin
from flask.globals import request
from shutil import rmtree
from tempfile import mkdtemp
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import sys, os
app = Flask(__name__)
CORS(app)
# print()
UPLOAD_FOLDER = 'UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'docx','doc'])
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

obj = resume_parser.ResumeParser()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/resumeParser', methods=['POST'])
@cross_origin()
def parse_resume():
    if request.method == 'POST':
        file = request.files.get('file',"")
        if not file:
            # flash('No selected file')
            return json.dumps({"status": 400, "reason": "No selected file"}), 400
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                val_data = obj.extract_block(filepath)
                # print ('==================>',val_data)
                os.remove(filepath)
                return json.dumps({"status": 200, "data": val_data})
            except Exception as e:
                return json.dumps({"status": 500, "reason":str(e)}), 500
        else:
            return json.dumps({"status": 400, "reason": "Invalid file extension"}), 400

def start_api():
    try:
        app.run('0.0.0.0', port=9000, threaded=True)
    except Exception as e:
        raise Exception('Exception occurred in initializing ' + str(e))


if __name__ == "__main__":
    start_api()

