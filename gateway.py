# from fileinput import filename
import json
# from unittest import result
# from grpc import Status
# from matplotlib.font_manager import json_dump
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
# from requests import session
from werkzeug.wrappers import Response
import os
# from flask import Flask, flash, request, redirect, url_for, send_from_directory, current_app
from flask import Flask
from werkzeug.utils import secure_filename
# import datetime


UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
EXTENSION_HEADER = {
    'txt': 'text/plain',
    'pdf': 'application/pdf',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif'
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class CloudStorageGatewayService:
    name = 'cloud_storage_gateway'
    cloud_storage_rpc = RpcProxy('cloud_storage_service')
    
    @http('POST', '/api/files')
    def upload_files(self, request):
        if 'file' not in request.files:
            return 400, json.dumps({
                "status": "error",
                "message": "No file part"
            })
        
        files = request.files.getlist('file')
        for file in files:
            if file.filename == '':
                return 400, json.dumps({
                    "status": "error",
                    "message": "No selected file"
                })
        
        arrFilename = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                arrFilename.append(filename)
            else:
                return 415, json.dumps({
                    "status": "error",
                    "message": "Unsupported Media Type"
                })
        
        upload_files = self.cloud_storage_rpc.upload_files(arrFilename)
        
        return int(upload_files['response_code']), json.dumps(upload_files['response_data'])
    
    
    @http('GET', '/api/files/<int:file_id>')
    def download_files(self, request, file_id):
        download_files = self.cloud_storage_rpc.download_files(file_id)
        
        if int(download_files['response_code']) != 200:
            return int(download_files['response_code']), json.dumps(download_files['response_data'])
        
        filename = download_files['response_data']['data']['filename']
        response = Response(open(UPLOAD_FOLDER + '/' + filename, 'rb').read())
        file_type = filename.split('.')[-1]
        
        response.headers['Content-Type'] = EXTENSION_HEADER[file_type]
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        
        return response
    
    
    @http('GET', '/api/files')
    def get_all_files(self, request):
        get_all_files = self.cloud_storage_rpc.get_all_files()
        
        return int(get_all_files['response_code']), json.dumps(get_all_files['response_data'])
