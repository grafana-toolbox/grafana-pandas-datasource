"""
Copyright 2017 Linar <linar@jether-energy.com>
Copyright 2020 Andreas Motl <andreas.motl@panodata.org>

License: GNU Affero General Public License, Version 3
"""
from typing import Dict, Callable
from dataclasses import dataclass, field


@dataclass
class DataGenerators:
    """
    Store references to data generator functions
    yielding pandas data frames.
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
