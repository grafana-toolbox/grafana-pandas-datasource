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
from typing import Dict, Callable
from dataclasses import dataclass, field


@dataclass
class DataGenerators:
    """
    Store references to data generator functions
    yielding Pandas data frames.
    """

    metric_readers: Dict[str, Callable] = field(default_factory=dict)
    metric_finders: Dict[str, Callable] = field(default_factory=dict)
    annotation_readers: Dict[str, Callable] = field(default_factory=dict)
    panel_readers: Dict[str, Callable] = field(default_factory=dict)

    def add_metric_reader(self, name, reader):
        self.metric_readers[name] = reader

    def add_metric_finder(self, name, finder):
        self.metric_finders[name] = finder

    def add_annotation_reader(self, name, reader):
        self.annotation_readers[name] = reader

    def add_panel_reader(self, name, reader):
        self.panel_readers[name] = reader


"""
@dataclass
class DataGeneratorRegistry:
    generators: Dict[str, DataGenerators] = field(default_factory=dict)
"""


# Global reference to instance of DataGenerators.
data_generators: DataGenerators = DataGenerators()
