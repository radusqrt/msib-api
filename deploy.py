from flask import Flask, flash, request, redirect, url_for
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

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


class FileUpload(Resource):
    def post(self):
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'fileName': filename}, 200


api.add_resource(FileUpload, '/upload')

if __name__ == '__main__':
    app.run(debug=True)
