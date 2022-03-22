#!/usr/bin/env python3

import spacy
import os
import sys
import logging

from util.preprocessing import addCharInformation, createMatrices, addCasingInformation
from neuralnets.BiLSTM import BiLSTM

from model import detect_events

from flask import Flask, jsonify, request

port = os.getenv("ANALYTIC_PORT")
if not port:
    port = 45000

model_path = os.getenv('MODEL_PATH')
if not model_path:
    model_path = './models/EN_Events.h5'

lstmModel = None
try:
    lstmModel = BiLSTM.loadModel(model_path)
    logging.debug("model loaded OK")
except IOError:
    print("failed to load model; set $MODEL_PATH to valid model file")
    sys.exit(1)

nlp = spacy.load('en_core_web_sm', disable=["parser", "tagger"])
nlp.add_pipe(nlp.create_pipe('sentencizer'))

max_length = os.getenv("MAX_DOCUMENT_LENGTH")
if max_length:
    nlp.max_length = int(max_length)

# shape of output data
ota = {}
ota['class'] = 'derived'
ota['type'] = 'tags'
ota['label'] = "Qntfy Event detection"
ota['version'] = "0.2.1"


######################################
## flask-related
######################################


def prefix_route(route_function, prefix='', mask='{0}{1}'):
    def newroute(route, *args, **kwargs):
        return route_function(mask.format(prefix, route), *args, **kwargs)
    return newroute


STATUS_OK = "ok"
STATUS_ERROR = "error"

app = Flask(__name__)


@app.route('/api/v1/health', methods=['GET'])
def health():
    out = {}
    out['status'] = STATUS_OK
    return jsonify(out)


@app.route('/api/v1/cdr/predict', methods=['POST'])
def predict():
    request_json = request.get_json(force=True)
    txt = request_json['extracted_text']
    events = detect_events(txt, nlp, lstmModel)
    # each event is a dict with tag, offset_end, offset_start,
    # so it's good to go schema wise
    # filter out 'O' tags
    ota['content'] = [event for event in events if event['tag'] is not 'O']
    annos = []
    if 'annotations' in request_json:
        annos = request_json['annotations']
    annos.append(ota)
    request_json['annotations'] = annos
    return jsonify(request_json)


@app.route('/api/v1/annotate/cdr', methods=['POST'])
def annotate():
    request_json = request.get_json(force=True)
    txt = request_json['extracted_text']
    events = detect_events(txt, nlp, lstmModel)
    # each event is a dict with tag, offset_end, offset_start,
    # so it's good to go schema wise
    # filter out 'O' tags
    output_sans_zeros = [event for event in events if event['model_output'] is not 'O']
    for d in output_sans_zeros:
        del d['model_output']
        del d['text']
    ota['content'] = output_sans_zeros
    return jsonify(ota)


if __name__ == '__main__':
    app.run(debug=False,
            host='0.0.0.0',
            port=port,
            use_reloader=False,
            threaded=False,
            )
