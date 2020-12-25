"""
Copyright 2017 Linar <linar@jether-energy.com>
Copyright 2020 Andreas Motl <andreas.motl@panodata.org>

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
