from flask import Flask, flash, request, redirect, url_for
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import csv
import uuid
from handle_sheets import handle_csv, handle_xlsx

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
cors = CORS(app)


class Home(Resource):
    def get(self):
        return 'I am just an API'


class FileUpload(Resource):
    def post(self):
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return "Niciun fișier ales", 400
        if file and allowed_file(file.filename):
            real_filename = secure_filename(file.filename)
            # TODO: handle extensions
            filename = str(uuid.uuid4())
            file.save(filename)
            response, code = handle_xlsx(
                filename) if real_filename[-4:] == 'xlsx' else handle_csv(filename)
            os.remove(filename)
            print(response, code)
            return response, code
        return "Fișierele trebuie să fie .csv sau .xlsx.", 400


api.add_resource(FileUpload, '/upload')
api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(debug=True)
