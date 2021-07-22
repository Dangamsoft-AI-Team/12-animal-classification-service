import os
from flask import Flask,request, render_template,jsonify
from flask_cors import CORS
from utils import inference
from model import pretrained_resnet152
import torch
from math import exp
import random
import numpy as np

import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Api, Resource

import py_eureka_client.netint_utils as netint_utils
import py_eureka_client.eureka_client as eureka_client
from werkzeug.datastructures import FileStorage

import argparse, configparser


random_seed = 42

torch.manual_seed(random_seed)
torch.cuda.manual_seed(random_seed)
torch.cuda.manual_seed_all(random_seed) # if use multi-GPU
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
np.random.seed(random_seed)
random.seed(random_seed)

device =  torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = pretrained_resnet152(freeze=True, n_classes=12, pretrained=False)
model.load_state_dict(torch.load('../models/face_classification_v2.pt', map_location=device))
decoder = {0: 'chicken', 1: 'cow', 2: 'dog', 3: 'dragon', 4: 'horse', 5: 'monkey', 6: 'mouse', 7: 'pig',
                       8: 'rabbit', 9: 'sheep', 10: 'snake', 11: 'tiger'}

app = Flask(__name__)
CORS(app)
app.config.SWAGGER_UI_DOC_EXPANSION = 'full'

api = Api(app, version='1.0', title='12-animal-classification-service',
          description='return simmilar animal')
ns = api.namespace('face-clf')

upload_parser = ns.parser()
upload_parser.add_argument('image',
                           location='files',
                           type=FileStorage)

@api.route('/12-animal-classification/predict')
@api.expect(upload_parser)
class face_cls(Resource):
    def post(self):
        args = upload_parser.parse_args()
        img_bytes = args.get('image').read()
        
        output = inference(model,img_bytes)
        animal = decoder[output.argmax()]

        return jsonify({decoder[idx]: round(exp(output[idx])*100, 2) for idx in range(len(decoder))})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='which server?')
    parser.add_argument('--server_name', '-s', type=str, default='test', help='service, test, prod')
    parser.add_argument('--port_number', '-p', type=int, default=30001, help='port number default id 30001')
    args = parser.parse_args()

    config = configparser.ConfigParser()

    config.read('../server_data.ini')

    ip = config[args.server_name]['ip']
    port_number = args.port_number
    if ip == 'None':
        ip = netint_utils.get_first_non_loopback_ip()

    eureka_host = os.environ.get('EUREKA_HOST', config[args.server_name]['server'])
    server_host = os.environ.get('SERVER_HOST', ip)

    eureka_client.init(eureka_server=f"{eureka_host}:38761/eureka/",
                       app_name="12-animal-classification-service",
                       instance_ip=server_host,
                       instance_host=server_host,
                       instance_port=port_number)

    app.run(host='0.0.0.0', port=port_number)
