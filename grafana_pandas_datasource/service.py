"""
A REST API based on Flask for serving Pandas Dataframes to Grafana.

The idea is to use ``flask_restful`` and create a Blueprint to be
used by a parent project (i.e. a larger API project where ``/grafana/``
endpoints are used by Grafana's SimpleJson plugin).

----

Copyright 2017 Linar <linar@jether-energy.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin
import pandas as pd

from grafana_pandas_datasource.util import dataframe_to_response, dataframe_to_json_table, annotations_to_response


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

methods = ('GET', 'POST')

metric_finders = {}
metric_readers = {}
annotation_readers = {}
panel_readers = {}


def add_reader(name, reader):
    metric_readers[name] = reader


def add_finder(name, finder):
    metric_finders[name] = finder


def add_annotation_reader(name, reader):
    annotation_readers[name] = reader


def add_panel_reader(name, reader):
    panel_readers[name] = reader


@app.route('/', methods=methods)
@cross_origin()
def hello_world():
    print(request.headers, request.get_json())
    return 'Jether\'s Grafana Pandas Datasource, used for rendering HTML panels and timeseries data.'


@app.route('/search', methods=methods)
@cross_origin()
def find_metrics():
    print(request.headers, request.get_json())
    req = request.get_json()

    target = req.get('target', '*')

    if ':' in target:
        finder, target = target.split(':', 1)
    else:
        finder = target

    if not target or finder not in metric_finders:
        metrics = []
        if target == '*':
            metrics += metric_finders.keys() + metric_readers.keys()
        else:
            metrics.append(target)

        return jsonify(metrics)
    else:
        return jsonify(list(metric_finders[finder](target)))


@app.route('/query', methods=methods)
@cross_origin(max_age=600)
def query_metrics():
    print(request.headers, request.get_json())
    req = request.get_json()

    results = []

    ts_range = {'$gt': pd.Timestamp(req['range']['from']).to_pydatetime(),
                '$lte': pd.Timestamp(req['range']['to']).to_pydatetime()}

    if 'intervalMs' in req:
        freq = str(req.get('intervalMs')) + 'ms'
    else:
        freq = None

    for target in req['targets']:
        if ':' not in target.get('target', ''):
            abort(404, Exception('Target must be of type: <finder>:<metric_query>, got instead: ' + target['target']))

        req_type = target.get('type', 'timeserie')

        finder, target = target['target'].split(':', 1)
        query_results = metric_readers[finder](target, ts_range)

        if req_type == 'table':
            results.extend(dataframe_to_json_table(target, query_results))
        else:
            results.extend(dataframe_to_response(target, query_results, freq=freq))

    return jsonify(results)


@app.route('/annotations', methods=methods)
@cross_origin(max_age=600)
def query_annotations():
    print(request.headers, request.get_json())
    req = request.get_json()

    results = []

    ts_range = {'$gt': pd.Timestamp(req['range']['from']).to_pydatetime(),
                '$lte': pd.Timestamp(req['range']['to']).to_pydatetime()}

    query = req['annotation']['query']

    if ':' not in query:
        abort(404, Exception('Target must be of type: <finder>:<metric_query>, got instead: ' + query))

    finder, target = query.split(':', 1)
    results.extend(annotations_to_response(query, annotation_readers[finder](target, ts_range)))

    return jsonify(results)


@app.route('/panels', methods=methods)
@cross_origin()
def get_panel():
    print(request.headers, request.get_json())
    req = request.args

    ts_range = {'$gt': pd.Timestamp(int(req['from']), unit='ms').to_pydatetime(),
                '$lte': pd.Timestamp(int(req['to']), unit='ms').to_pydatetime()}

    query = req['query']

    if ':' not in query:
        abort(404, Exception('Target must be of type: <finder>:<metric_query>, got instead: ' + query))

    finder, target = query.split(':', 1)
    return panel_readers[finder](target, ts_range)


def get_application():
    return app
