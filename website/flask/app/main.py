from flask import Flask
from flask import request
from flask import jsonify
# from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os
import sys
import uuid
import json

from app.InowasFlopyAdapter.InowasFlopyImportAdapter import InowasFlopyImportAdapter

app = Flask(__name__)
CORS(app)
# api = Api(app)
UPLOAD_FOLDER = '/app/uploads'

@app.route('/model-upload', methods=['POST'])
def upload():

    if request.method == 'POST':
        files = request.files.getlist("file[]")
       
        model_ws = os.path.join(UPLOAD_FOLDER, str(uuid.uuid4()))
        json_file_name = os.path.join(model_ws, 'config.json')

        os.mkdir(model_ws)

        try:
            for f in files:
                f.save(os.path.join(model_ws, f.filename))
            
            import_adapter = InowasFlopyImportAdapter(
                model_ws=model_ws,
                json_file=json_file_name,
                mf_namfile='mf.nam',
                mt_namfile='mt.nam'
            )
            import_adapter.serialize()

            response_message, model_data = import_adapter.response

            return json.dumps(
                {
                    'data':'',
                    'message': response_message,
                    'model_data': model_data,
                    'status':'success'
                },
                default=InowasFlopyImportAdapter.np_type_translate
            )

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            return json.dumps(
                {
                    'data':'',
                    'message': str(e)+str(exc_type)+str(fname)+str(exc_tb.tb_lineno),
                    'status':'error'
                },
                default=InowasFlopyImportAdapter.np_type_translate
            )


# class ModelUpload(Resource):

#     def post(self):
#         files = request.files.getlist("file[]")
#         model_ws = os.path.join(UPLOAD_FOLDER, str(uuid.uuid4()))
#         json_file_name = os.path.join(model_ws, 'config.json')

#         os.mkdir(model_ws)
#         print(model_ws)
#         # try:
#         for f in files:
#             f.save(os.path.join(model_ws, f.filename))
        
#         import_adapter = InowasFlopyImportAdapter(
#             model_ws=model_ws,
#             json_file=json_file_name,
#             mf_namfile='mf.nam',
#             mt_namfile='mt.nam'
#         )
#         import_adapter.serialize()

#         return {
#             'data':'',
#             'message': str(import_adapter.response_message),
#             'status':'success'
#         }

        # except Exception as e:
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print(exc_type, fname, exc_tb.tb_lineno)
        #     return {
        #         'data':'',
        #         'message': str(e)+str(exc_type)+str(fname)+str(exc_tb.tb_lineno),
        #         'status':'error'
        #     }

# api.add_resource(ModelUpload,'/model-upload')

if __name__ == '__main__':
    app.run(debug=True)