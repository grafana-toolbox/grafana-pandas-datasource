"""
Copyright 2020 Andreas Motl <andreas@hiveeyes.org>

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
import urllib.parse
from datetime import datetime, timedelta

import pandas as pd
from cachetools import cached, TTLCache
from phenodata.dwd.cdc import DwdCdcClient
from phenodata.dwd.pheno import DwdPhenoDataHumanizer, DwdPhenoData
from phenodata.ftp import FTPSession
from phenodata.util import read_list

from grafana_pandas_datasource import create_app
from grafana_pandas_datasource.registry import data_generators as dg
from grafana_pandas_datasource.service import pandas_component

"""
Demo for grafana-pandas-datasource.

This is a demo program which generates flowering events for
phenology species suitable as fruits for bees (Apis mellifera)
as Grafana annotations.

Setup::

    pip install grafana-pandas-datasource phenodata>=0.10.0 cachetools

To query the annotations, use ``<reader_name>:<query_string>``, e.g.
- ``flowering:station=müncheberg``
"""


def define_and_register_data():

    # Sample annotation reader.
    def get_mellifera_flowering(query_string, ts_range):
        query = dict(urllib.parse.parse_qsl(query_string))
        series = phenodata_mellifera(
            dataset="immediate", years=tuple([2019, 2020, 2021]), phases=tuple([5, 7]),
            options=tuple(query.items())
        )
        return series

    # Register data generators.
    dg.add_annotation_reader("flowering", get_mellifera_flowering)


@cached(cache=TTLCache(maxsize=65536, ttl=24 * 60 * 60))
def phenodata_mellifera(dataset: str, years: tuple[int], phases: tuple[str], options: tuple[tuple[str, str]]):

    options = dict(options)
    options["type"] = read_list(options.get("type")) or ["observations"]

    cdc_client = DwdCdcClient(ftp=FTPSession())
    humanizer = DwdPhenoDataHumanizer(language="german", long_station=False, show_ids=False)
    client = DwdPhenoData(cdc=cdc_client, humanizer=humanizer, dataset=dataset)

    # Rewrite options.
    phenodata_options = {
        "partition": "recent",
        "year": years,
        "species": DwdPhenoData.load_preset("options", "species", "mellifera-de-primary"),
        "phase-id": phases,
        "station": read_list(options.get("station", [])),
        "humanize": True,
    }

    data_total = []

    # Get observations
    if "observations" in options["type"]:
        data_past = client.get_observations(phenodata_options, humanize=phenodata_options['humanize'])
        data_total.append(data_past)

    if "forecast" in options["type"]:
        next_year = (datetime.today() + timedelta(days=365)).year
        data_future = client.get_forecast(phenodata_options, forecast_year=next_year, humanize=phenodata_options['humanize'])
        data_total.append(data_future)

    data = pd.concat(data_total)

    # Create Pandas Series from Dataframe.
    index = data.Datum.astype('datetime64')
    values = data.Spezies.str.cat(data.Phase, sep=" - ").str.cat(data.Station, sep=" - ")
    series = pd.Series(data=values.tolist(), index=index)
    series = series.sort_index(ascending=True)

    return series


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
