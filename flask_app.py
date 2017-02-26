#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import request, Response, Flask

from string import ascii_letters
from random import choice
from pyprometheus.contrib.uwsgi_features import UWSGIStorage
from pyprometheus.registry import BaseRegistry
from pyprometheus.utils.exposition import registry_to_text
from pyprometheus.metrics import BaseMetric, Gauge, Counter, Histogram, Summary

storage = UWSGIStorage(0)
registry = BaseRegistry(storage=storage)


requests_total = Counter("app:requests_total", "Total count of requests", ["method", "url_rule"], registry=registry)
request_time_histogram = Histogram("app:request_time_histogram", "Request time", ["method", "url_rule"], registry=registry)
request_time_summary = Histogram("app:request_time_summary", "Request time", ["method", "url_rule"], registry=registry)



app = Flask(__name__)
app.debug = True


@app.route("/metrics")
def metrics():
    text = "# Process in {0}\n".format(os.getpid())
    return Response(text + registry_to_text(registry), mimetype="text/plain")


@app.route('/<path:path>')
@app.route('/')
def index(path='/'):
    requests_total.labels(method=request.method, url_rule="total").inc()

    rnd = ''.join([choice(ascii_letters) for x in xrange(10)])

    text = "# Process in {0} rnd={1}\n".format(os.getpid(), rnd)
    #with request_time_histogram.labels(method=request.method, url_rule=path).time(), request_time_summary.labels(method=request.method, url_rule=path).time():

    return Response(text, mimetype="text/plain")

application = app
print("Debug app init")
