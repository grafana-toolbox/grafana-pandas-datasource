################################
Apis mellifera flowering example
################################


*****
About
*****

This is a demo program which generates flowering events for
phenology species suitable as fruits for bees (Apis mellifera)
as Grafana annotations.

.. figure:: https://user-images.githubusercontent.com/453543/103260962-fd1b8900-499f-11eb-8459-9ecaa6c55ac7.png

    Image: Flowering events for some species around Müncheberg, Brandenburg, Germany.


*****
Setup
*****

For general installation instructions, see `setup sandbox environment`_.

::

    pip install grafana-pandas-datasource phenodata>=0.10.0 cachetools


**************
Start services
**************

::

    # Run Grafana.
    docker run --rm -it \
        --publish=3000:3000 --volume="$(pwd)/var/lib/grafana":/var/lib/grafana \
        --env='GF_SECURITY_ADMIN_PASSWORD=admin' --env='GF_INSTALL_PLUGINS=grafana-simple-json-datasource' \
        grafana/grafana:8.3.4

    # Run Grafana pandas datasource demo.
    python examples/phenodata-mellifera/demo.py


*****************
Configure Grafana
*****************


Command line
============

You can have a quickstart by putting those two JSON definition files into
Grafana::

    # Login to Grafana.
    export GRAFANA_URL=http://localhost:3000
    http --session=grafana ${GRAFANA_URL} --auth=admin:admin

    # Create datasource.
    cat examples/phenodata-mellifera/datasource.json | \
        http --session=grafana POST ${GRAFANA_URL}/api/datasources

    # Create dashboard.
    cat examples/phenodata-mellifera/dashboard.json | \
        http --session=grafana POST ${GRAFANA_URL}/api/dashboards/db

Then, visit the dashboard at::

    open ${GRAFANA_URL}


.. note::

    The host where the datasource service is running can be accessed from the
    Grafana Docker container using the hostname ``host.docker.internal``.


.. _setup sandbox environment: https://github.com/panodata/grafana-pandas-datasource/blob/main/docs/setup.rst
