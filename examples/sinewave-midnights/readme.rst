##########################
Sinewave/Midnights example
##########################


*****
About
*****

This is a demo program which generates a sine wave for data and
annotations for designating midnight times.

.. figure:: https://user-images.githubusercontent.com/453543/103137119-78dab480-46c6-11eb-829f-6aa957239804.png

    Image: Sinewave data and midnights annotations, both generated using NumPy_.


*****
Setup
*****

For general installation instructions, see `setup sandbox environment`_.


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
    python examples/sinewave-midnights/demo.py


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
    cat examples/sinewave-midnights/datasource.json | \
        http --session=grafana POST ${GRAFANA_URL}/api/datasources

    # Create dashboard.
    cat examples/sinewave-midnights/dashboard.json | \
        http --session=grafana POST ${GRAFANA_URL}/api/dashboards/db

Then, visit the dashboard at::

    open http://localhost:3000/d/xNbUrobGz/sine-24

GUI
===

This section walks you through setting up a data source and dashboard in
Grafana manually, step by step with screenshots. Please follow the guidelines
carefully.

.. figure:: https://user-images.githubusercontent.com/453543/150621604-f9b4664c-493a-4a9d-bd46-cf59da175438.png

    Install "SimpleJson" plugin at http://localhost:3000/plugins/grafana-simple-json-datasource.

.. figure:: https://user-images.githubusercontent.com/453543/150621516-cb8b24fa-46ee-4515-b66e-81f79a046912.png

    Add new data source of "SimpleJson" type at http://localhost:3000/datasources/new.
    Configure the URL to the Flask service serving pandas data frames.
    When running Grafana in Docker, use ``host.docker.internal`` to address the
    Docker host.

.. figure:: https://user-images.githubusercontent.com/453543/150621520-f0eeb740-2c12-4a8b-908c-50893a8bd583.png

    Create dashboard with Timeseries or Graph panel at http://localhost:3000/dashboard/new,
    adjust "Data source" and "metric" values.

.. figure:: https://user-images.githubusercontent.com/453543/150621869-5d226582-886c-41c4-a446-d8d75685f9d2.png

    At the time picker, choose an interval of "Last 2 days".

.. figure:: https://user-images.githubusercontent.com/453543/150621970-3d20f11c-007a-4e6e-ad8f-abf1f3e02ed0.png

    Save your dashboard.


.. _NumPy: https://numpy.org/
.. _setup sandbox environment: https://github.com/panodata/grafana-pandas-datasource/blob/main/docs/setup.rst
