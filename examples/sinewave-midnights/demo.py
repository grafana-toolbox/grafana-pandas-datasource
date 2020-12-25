"""
Demo for grafana-pandas-datasource.

To query the reader, use ``<reader_name>:<query_string>``, e.g.
- ``sine_wave:24``
- ``midnights:xx``
"""
import pandas as pd
import numpy as np
from grafana_pandas_datasource.core import get_application, add_annotation_reader, add_reader


def main():

    # Sample annotation reader.
    add_annotation_reader(
        'midnights',
        lambda query_string, ts_range:
            pd.Series(index=pd.date_range(ts_range['$gt'], ts_range['$lte'], freq='D', normalize=True)).fillna('Text for annotation - midnight'))

    # Sample timeseries reader.
    def get_sine(freq, ts_range):
        freq = int(freq)
        ts = pd.date_range(ts_range['$gt'], ts_range['$lte'], freq='H')
        return pd.Series(np.sin(np.arange(len(ts)) * np.pi * freq * 2 / float(len(ts))), index=ts).to_frame('value')
    add_reader('sine_wave', get_sine)

    # Get Flask application and invoke it.
    app = get_application()
    app.run(host='127.0.0.1', port=3003, debug=True)


if __name__ == '__main__':
    main()
