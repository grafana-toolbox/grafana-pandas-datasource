################################
Apis mellifera flowering example
################################
This is a demo program which generates flowering events for
phenology species suitable as fruits for bees (Apis mellifera)
as Grafana annotations.

.. figure:: https://user-images.githubusercontent.com/453543/103260962-fd1b8900-499f-11eb-8459-9ecaa6c55ac7.png

    Image: Flowering events for some species around Müncheberg, Brandenburg, Germany.


Setup
=====
::

    pip install grafana-pandas-datasource phenodata>=0.10.0 cachetools


Acquire example files
=====================
::

    export EXAMPLES_BASEURL=https://raw.githubusercontent.com/panodata/grafana-pandas-datasource/0.1.0/examples

    wget ${EXAMPLES_BASEURL}/phenodata-mellifera/demo.py \
        --output-document=phenodata-mellifera-demo.py

    wget ${EXAMPLES_BASEURL}/phenodata-mellifera/datasource.json \
        --output-document=phenodata-mellifera-datasource.json

    wget ${EXAMPLES_BASEURL}/phenodata-mellifera/dashboard.json \
        --output-document=phenodata-mellifera-dashboard.json


Invoke
======
::

    # Run Grafana.
    docker run --rm -it \
        --publish=3000:3000 --volume="$(pwd)/var/lib/grafana":/var/lib/grafana \
        --env='GF_SECURITY_ADMIN_PASSWORD=admin' --env='GF_INSTALL_PLUGINS=grafana-simple-json-datasource' \
        grafana/grafana:7.3.6

    # Run Grafana Pandas Datasource demo.
    python phenodata-mellifera-demo.py


Configure
=========
.. note::

    The host where the datasource service is running can be accessed from the
    Grafana Docker container using the hostname ``host.docker.internal``.

You can have a quickstart by putting ``examples/phenodata-mellifera/datasource.json``
and ``examples/phenodata-mellifera/dashboard.json`` into Grafana::

    # Login to Grafana.
    export GRAFANA_URL=http://localhost:3000
    http --session=grafana ${GRAFANA_URL} --auth=admin:admin

    # Create datasource.
    cat phenodata-mellifera-datasource.json | \
        http --session=grafana POST ${GRAFANA_URL}/api/datasources

    # Create dashboard.
    cat phenodata-mellifera-dashboard.json | \
        http --session=grafana POST ${GRAFANA_URL}/api/dashboards/db

    open ${GRAFANA_URL}
