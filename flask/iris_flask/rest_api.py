import os

from flask import Flask, jsonify, abort, make_response, request
import requests
import json
import time
import sys
import pandas as pd
import model as M
import copy
import logging
logging.basicConfig(filename='logs/logs.log',level=logging.DEBUG)

from rq import Queue, get_current_job
from redis import Redis
redis_conn = Redis(host='app-redis', port=6379)
queue = Queue('rest_api', connection=redis_conn, default_timeout=1200)

app = Flask(__name__)

model = M.load_model()
targets = ['setosa', 'versicolor', 'virginica']

def get_pred(sepal_length, sepal_width, petal_length, petal_width):

    logging.info('Prediction ...')
    
    all_columns = ['sepal length', 'sepal width', 'petal length', 'petal width']
    lst = [sepal_length, sepal_width, petal_length, petal_width]
    df = pd.DataFrame([lst], columns = all_columns)
    
    df = df.astype(float)
    result = model.predict_proba(df)
    predx = ['%.3f' % elem for elem in result[0]]
    preds_concat = pd.concat([pd.Series(targets), pd.Series(predx)], axis=1)
    preds = pd.DataFrame(data=preds_concat)
    preds.columns = ["class", "probability"]
    return preds.reset_index(drop=True)

def launch_task(sepal_length, sepal_width, petal_length, petal_width, api, job_id):
    job = get_current_job()
    
    pred_model = get_pred(sepal_length, sepal_width, petal_length, petal_width)

    if api == 'v1.0':
        logging.info('Launch Task')
        res_dict = {'result':  json.loads( pd.DataFrame(pred_model).to_json(orient='records'))}
        return res_dict
    else:
        res_dict = {'error': 'API doesnt exist'}
        logging.warning('API doesnt exist')
        return res_dict

def get_response(dict, status=200):
    return make_response(jsonify(dict), status)

def get_job_response(job_id):
    return get_response({'job_id': job_id})

@app.route('/iris/api/v1.0/getpred', methods=['GET'])
def get_task():

    job_id = request.args.get('job_id')
    job = queue.enqueue('rest_api.launch_task', request.args.get('sepal_length'), request.args.get('sepal_width'), \
                         request.args.get('petal_length'), request.args.get('petal_width'), 'v1.0', job_id, result_ttl=60 * 60 * 24, \
                        job_id=job_id)

    return get_job_response(job.get_id())

def get_process_response(code, process_status, status=200):
    return get_response({
        'code': code,
        'status': process_status
    }, status)

@app.route('/iris/api/status/<id>')
def status(id):
    job = queue.fetch_job(id)

    if (job is None):
        return get_process_response('NOT_FOUND', 'error', 404)

    if (job.is_failed):
        return get_process_response('INTERNAL_SERVER_ERROR', 'error', 500)

    if (job.is_finished):
        return get_process_response('READY', 'success')

    return get_process_response('NOT_READY', 'running', 202)

@app.route('/iris/api/result/<id>')
def result(id):
    job = queue.fetch_job(id)
    
    if job is None:
        return get_process_response('NOT_FOUND', 'error', 404)

    if job.is_failed:
        return get_process_response('INTERNAL_SERVER_ERROR', 'error', 500)

    if job.is_finished:
        job_result = copy.deepcopy(job.result)
        result = {
            'result': job_result['result']
        }

        return get_response(result)

    return get_process_response('NOT_FOUND', 'error', 404)

@app.errorhandler(404)
def not_found(error):
    logging.warning('PAGE NOT FOUND')
    return make_response(jsonify({'code': 'PAGE_NOT_FOUND'}), 404)

@app.errorhandler(500)
def server_error(error):
    logging.warning('INTERNAL SERVER ERROR')
    return make_response(jsonify({'code': 'INTERNAL_SERVER_ERROR'}), 500)

if __name__ == '__main__':
    app.run(port=5000, debug=True)