from flask import Flask, flash, request, redirect, url_for
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import csv

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
cors = CORS(app)


# class HelloWorld(Resource):
#     def get(self):
#         return {}

#     def post(self):
#         some_json = request.get_json()
#         return {'you sent': some_json}, 201


class Home(Resource):
    def get(self):
        return 'I am just an API'


class FileUpload(Resource):
    def post(self):
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return "No file chosen", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    print(row)
            return {'fileName': filename}, 200
        return "Files should be only .csv, .xls or .xlsx.", 400


api.add_resource(FileUpload, '/upload')
api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(debug=True)
