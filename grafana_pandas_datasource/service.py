"""
Copyright 2017 Linar <linar@jether-energy.com>
Copyright 2020-2022 Andreas Motl <andreas.motl@panodata.org>

License: GNU Affero General Public License, Version 3
"""
import pandas as pd
from flask import Blueprint, abort, current_app, jsonify, request
from flask_cors import cross_origin

from grafana_pandas_datasource.registry import data_generators as dg
from grafana_pandas_datasource.core import (
    annotations_to_response,
    dataframe_to_json_table,
    dataframe_to_response,
)

pandas_component = Blueprint("pandas-component", __name__)
methods = ("GET", "POST")


@pandas_component.route("/", methods=methods)
@cross_origin()
def test_datasource():
    current_app.logger.info('Request to "test_datasource" endpoint at /')
    return (
        "Grafana pandas datasource: Serve NumPy data via pandas data frames to Grafana. "
        'For documentation, see <a href="https://github.com/panodata/grafana-pandas-datasource">https://github.com/panodata/grafana-pandas-datasource</a>.'
    )


@pandas_component.route("/search", methods=methods)
@cross_origin()
def find_metrics():
    current_app.logger.info('Request to "find_metrics" endpoint at /search')
    req = request.get_json()

    target = req.get("target", "*")

    if ":" in target:
        finder, target = target.split(":", 1)
    else:
        finder = target

    if not target or finder not in dg.metric_finders:
        metrics = []
        if target == "*":
            metrics += dg.metric_finders.keys()
            metrics += dg.metric_readers.keys()
        else:
            metrics.append(target)

        return jsonify(metrics)
    else:
        return jsonify(list(dg.metric_finders[finder](target)))


@pandas_component.route("/query", methods=methods)
@cross_origin(max_age=600)
def query_metrics():
    current_app.logger.info('Request to "query_metrics" endpoint at /query')
    req = request.get_json()

    results = []

    ts_range = {
        "$gt": pd.Timestamp(req["range"]["from"]).to_pydatetime(),
        "$lte": pd.Timestamp(req["range"]["to"]).to_pydatetime(),
    }

    if "intervalMs" in req:
        freq = str(req.get("intervalMs")) + "ms"
    else:
        freq = None

    for target in req["targets"]:
        if ":" not in target.get("target", ""):
            abort(404, Exception("Target must be of type: <finder>:<metric_query>, got instead: " + target["target"]))

        req_type = target.get("type", "timeserie")

        finder, target = target["target"].split(":", 1)
        query_results = dg.metric_readers[finder](target, ts_range)

        if req_type == "table":
            results.extend(dataframe_to_json_table(target, query_results))
        else:
            results.extend(dataframe_to_response(target, query_results, freq=freq))

    return jsonify(results)


@pandas_component.route("/annotations", methods=methods)
@cross_origin(max_age=600)
def query_annotations():
    current_app.logger.info('Request to "query_annotations" endpoint at /annotations')
    req = request.get_json()

    results = []

    ts_range = {
        "$gt": pd.Timestamp(req["range"]["from"]).to_pydatetime(),
        "$lte": pd.Timestamp(req["range"]["to"]).to_pydatetime(),
    }

    query = req["annotation"]["query"]

    if ":" not in query:
        abort(404, Exception("Target must be of type: <finder>:<metric_query>, got instead: " + query))

    finder, target = query.split(":", 1)
    results.extend(annotations_to_response(query, dg.annotation_readers[finder](target, ts_range)))

    return jsonify(results)


@pandas_component.route("/panels", methods=methods)
@cross_origin()
def get_panel():
    current_app.logger.info('Request to "get_panel" endpoint at /panels')
    req = request.args

    ts_range = {
        "$gt": pd.Timestamp(int(req["from"]), unit="ms").to_pydatetime(),
        "$lte": pd.Timestamp(int(req["to"]), unit="ms").to_pydatetime(),
    }

    query = req["query"]

    if ":" not in query:
        abort(404, Exception("Target must be of type: <finder>:<metric_query>, got instead: " + query))

    finder, target = query.split(":", 1)
    return dg.panel_readers[finder](target, ts_range)
