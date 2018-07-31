from flask import Flask
from flask import request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import werkzeug, os

app = Flask(__name__)
CORS(app)
api = Api(app)
UPLOAD_FOLDER = './uploads'
parser = reqparse.RequestParser()
parser.add_argument('file[]', type=werkzeug.datastructures.FileStorage, location='files')


class ModelUpload(Resource):

    def post(self):
        files = request.files.getlist("file[]")
        data = parser.parse_args()
        # if data['file'] == "":
        #     return {
        #         'data':'',
        #         'message':'No file found',
        #         'status':'error'
            # }

        print(files)
        # try:
        for f in files:
            f.save(os.path.join(UPLOAD_FOLDER))
    
        return {
            'data':'',
            'message':'{} files uploaded'.format(len(files)),
            'status':'success'
        }
        # except Exception:
        #     return {
        #         'data':'',
        #         'message':str(Exception),
        #         'status':'error'
        #     }

api.add_resource(ModelUpload,'/model-upload')

if __name__ == '__main__':
    app.run(debug=True)