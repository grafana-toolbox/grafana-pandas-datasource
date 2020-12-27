#########################
Grafana Pandas Datasource
#########################


*****
About
*****
A REST API based on Flask for serving Pandas Dataframes to Grafana.

This way, a native Python application can be used to directly supply
data to Grafana both easily and powerfully.

It was inspired by and is compatible with the simple json datasource.

https://gist.github.com/linar-jether/95ff412f9d19fdf5e51293eb0c09b850

Setup
=====
::

    pip install grafana-pandas-datasource

Resources
=========
- https://github.com/grafana/grafana
- https://grafana.com/grafana/plugins/grafana-simple-json-datasource


*******
Example
*******
This is a demo program which generates a sine wave for data and
annotations for designating midnight times. For both, we are using NumPy.

.. figure:: https://user-images.githubusercontent.com/453543/103137119-78dab480-46c6-11eb-829f-6aa957239804.png

    Image: Sinewave data and midnights annotations, both generated using NumPy.


Acquire example files
=====================
::

    export EXAMPLES_BASEURL=https://raw.githubusercontent.com/panodata/grafana-pandas-datasource/0.1.0/examples

    wget ${EXAMPLES_BASEURL}/sinewave-midnights/demo.py \
        --output-document=sinewave-midnights-demo.py

    wget ${EXAMPLES_BASEURL}/sinewave-midnights/datasource.json \
        --output-document=sinewave-midnights-datasource.json

    wget ${EXAMPLES_BASEURL}/sinewave-midnights/dashboard.json \
        --output-document=sinewave-midnights-dashboard.json


Invoke
======
::

    # Run Grafana.
    docker run --rm -it \
        --publish=3000:3000 --volume="$(pwd)/var/lib/grafana":/var/lib/grafana \
        --env='GF_SECURITY_ADMIN_PASSWORD=admin' --env='GF_INSTALL_PLUGINS=grafana-simple-json-datasource' \
        grafana/grafana:7.3.6

    # Run Grafana Pandas Datasource demo.
    python sinewave-midnights-demo.py


Configure
=========
.. note::

    The host where the datasource service is running can be accessed from the
    Grafana Docker container using the hostname ``host.docker.internal``.

You can have a quickstart by putting ``examples/sinewave-midnights/datasource.json``
and ``examples/sinewave-midnights/dashboard.json`` into Grafana::

    # Login to Grafana.
    export GRAFANA_URL=http://localhost:3000
    http --session=grafana ${GRAFANA_URL} --auth=admin:admin

    # Create datasource.
    cat sinewave-midnights-datasource.json | \
        http --session=grafana POST ${GRAFANA_URL}/api/datasources

    # Create dashboard.
    cat sinewave-midnights-dashboard.json | \
        http --session=grafana POST ${GRAFANA_URL}/api/dashboards/db

    open ${GRAFANA_URL}
