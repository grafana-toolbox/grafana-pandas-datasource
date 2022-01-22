"""
Copyright 2017 Linar <linar@jether-energy.com>
Copyright 2020 Andreas Motl <andreas.motl@panodata.org>

License: GNU Affero General Public License, Version 3
"""
import pandas as pd
import numpy as np
from grafana_pandas_datasource import create_app
from grafana_pandas_datasource.registry import data_generators as dg
from grafana_pandas_datasource.service import pandas_component

"""
Demo for grafana-pandas-datasource.

This is a demo program which generates data using NumPy and Pandas.
It creates
- a sine wave for data and
- midnight times for annotations

Setup::

    pip install grafana-pandas-datasource

To query the reader, use ``<reader_name>:<query_string>``, e.g.
- ``sine_wave:24``
- ``midnights:xx``
"""


def define_and_register_data():

    # Sample timeseries reader.
    def get_sine(freq, ts_range):
        freq = int(freq)
        ts = pd.date_range(ts_range['$gt'], ts_range['$lte'], freq='H')
        return pd.Series(np.sin(np.arange(len(ts)) * np.pi * freq * 2 / float(len(ts))), index=ts).to_frame('value')

    # Sample annotation reader.
    def get_midnights(query_string, ts_range):
        return pd.Series(index=pd.date_range(ts_range['$gt'], ts_range['$lte'], freq='D', normalize=True), dtype='float64').fillna('Text for annotation - midnight')

    # Register data generators.
    dg.add_metric_reader("sine_wave", get_sine)
    dg.add_annotation_reader("midnights", get_midnights)


def main():

    # Define and register data generators.
    define_and_register_data()

    # Create Flask application.
    app = create_app()

    # Register Pandas component.
    app.register_blueprint(pandas_component, url_prefix="/")

    # Invoke Flask application.
    app.run(host='127.0.0.1', port=3003, debug=True)


if __name__ == '__main__':
    main()
