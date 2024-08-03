'''Parameter dataclasses and utilities.'''

from dataclasses import dataclass, field
from datetime import date, datetime
from importlib.resources import files
import json
from pathlib import Path
from typing import List


DATE_FORMAT = '%Y-%m-%d'
DEFAULT_START_DATE = datetime.strptime('2023-11-01', DATE_FORMAT)
DEFAULT_END_DATE = datetime.strptime('2023-11-10', DATE_FORMAT)
RADIUS = 200.0
PARAMETER_FILES = (
    'Makefile',
    'params/assays.json',
    'params/genomes.json',
    'params/grids.json',
    'params/samples.json',
    'params/sites.csv',
    'params/surveys.csv',
)


@dataclass
class AssayParams:
    '''Parameters for assay data generation.'''

    assay_types: list
    assay_staff: list
    assay_duration: list
    assay_plates: list
    control_val: float = 5.0
    controls: List[str] = field(default_factory=list)
    enddate: date = None
    experiments: int = 1
    filename_length: int = 8
    invalid: float = 0.1
    locale: str = 'en_IN'
    seed: int = None
    staff: int = 1
    startdate: date = None
    stdev: float = 3.0
    treated_val: float = 8.0
    treatment: str = None

    def __post_init__(self):
        '''Convert dates if provided.'''
        if self.startdate is None:
            self.startdate = DEFAULT_START_DATE
        else:
            self.startdate = datetime.strptime(self.startdate, DATE_FORMAT)

        if self.enddate is None:
            self.enddate = DEFAULT_END_DATE
        else:
            self.enddate = datetime.strptime(self.enddate, DATE_FORMAT)


@dataclass
class GenomeParams:
    '''Gene sequence parameters.'''
    snp_probs: list
    length: int
    num_genomes: int
    num_snp: int
    prob_other: float
    seed: int = None


@dataclass
class GridParams:
    '''Invasion percolation parameters.'''
    depth: int
    height: int
    seed: int
    width: int


@dataclass
class SampleParams:
    '''Sampled snail parameters.'''
    min_snail_size: float = None
    max_snail_size: float = None
    mutant: float = None
    normal: float = None
    seed: int = None


def export_params(options):
    '''Export parameter files.'''
    outdir = Path(options.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    root = files(__name__.split('.')[0])
    for filename in PARAMETER_FILES:
        src = root.joinpath(filename)
        dst = outdir.joinpath(Path(filename).name)
        dst.write_bytes(src.read_bytes())


def load_params(cls, filename):
    '''Load parameters from file.'''
    return cls(**json.loads(Path(filename).read_text()))
