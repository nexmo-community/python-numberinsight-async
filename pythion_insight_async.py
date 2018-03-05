import requests
import os
from flask import Flask, request, Response, jsonify 
import json

import datetime
import pickle
import dateutil.parser

app = Flask(__name__)
app.debug = True

def getInsight(number, url_root):
    params = {
        'api_key' : os.environ['NEXMO_API_KEY'],
        'api_secret' : os.environ['NEXMO_SECRET'],
        'number' : number,
        'callback' : url_root+'response'
    }
    url = 'https://api.nexmo.com/ni/advanced/async/json'
    res = requests.get(url, params=params)
    return res.json()


@app.route('/get/<number>', methods=['GET', 'POST'])
def lookup(number):
    fname = "files/{}.pkl".format(number)
    try:
        data = pickle.load(open(fname, "rb" ))
    except:
        req = getInsight(number, request.url_root)
        resp = {'status':'processing', 'request_id' : req['request_id'] }
        return Response(json.dumps(resp), status=202, mimetype='application/json')
    timestamp = dateutil.parser.parse(data['timestamp'])
    now = datetime.datetime.utcnow()
    delta = datetime.datetime.utcnow() - timestamp
    if (delta.seconds > 180):
        req = getInsight(number, request.url_root)
        resp = {'status':'processing', 'request_id' : req['request_id'] }
        return Response(json.dumps(resp), status=202, mimetype='application/json')
    else:
        return jsonify(data)
        


@app.route('/response', methods=['GET', 'POST'])
def response():
    data = request.get_json()
    data['timestamp'] = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    fname = "files/{}.pkl".format(data['international_format_number'])
    pickle.dump(data, open( fname, "wb" ))
    return "ok"



if __name__ == '__main__':
    app.run()