"""
Demo for grafana-pandas-datasource.

To query the reader, use ``<reader_name>:<query_string>``, e.g.
- ``sine_wave:24``
- ``midnights:xx``
"""
import pandas as pd
import numpy as np
from grafana_pandas_datasource.service import get_application, add_reader, add_annotation_reader


def main():

    # Sample timeseries reader.
    def get_sine(freq, ts_range):
        freq = int(freq)
        ts = pd.date_range(ts_range['$gt'], ts_range['$lte'], freq='H')
        return pd.Series(np.sin(np.arange(len(ts)) * np.pi * freq * 2 / float(len(ts))), index=ts).to_frame('value')

    # Sample annotation reader.
    def get_midnights(query_string, ts_range):
        return pd.Series(index=pd.date_range(ts_range['$gt'], ts_range['$lte'], freq='D', normalize=True), dtype='float64').fillna('Text for annotation - midnight')

    # Register data generation functions.
    add_reader('sine_wave', get_sine)
    add_annotation_reader('midnights', get_midnights)

    # Get Flask application and invoke it.
    app = get_application()
    app.run(host='127.0.0.1', port=3003, debug=True)


if __name__ == '__main__':
    main()
