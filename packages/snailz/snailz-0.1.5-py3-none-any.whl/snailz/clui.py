'''Interface for command-line script.'''

import argparse
import importlib.metadata
from pathlib import Path

from .assays import assays
from .db import db
from .genomes import genomes
from .grid import grid
from .mangle import mangle
from .plates import plates
from .samples import samples
from .survey import survey

from .params import export_params


TOUCH = '.touch'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='store_true', help='show version')
    subparsers = parser.add_subparsers()
    for sub in (
            _assays_parser,
            _db_parser,
            _everything_parser,
            _genomes_parser,
            _grid_parser,
            _mangle_parser,
            _params_parser,
            _plates_parser,
            _samples_parser,
            _survey_parser,
    ):
        sub(subparsers)
    options = parser.parse_args()
    if options.version:
        print(importlib.metadata.version('snailz'))
    else:
        options.func(options)


def everything(options):
    '''Build everything using default values.'''
    # Common values
    assays_data = Path(options.datadir, 'assays.json')
    assays_params = Path(options.paramsdir, 'assays.json')
    db_file = Path(options.datadir, 'lab.db')
    designs_data_dir = Path(options.datadir, 'designs')
    genomes_data = Path(options.datadir, 'genomes.json')
    genomes_params = Path(options.paramsdir, 'genomes.json')
    grids_data_dir = Path(options.datadir, 'grids')
    grids_params = Path(options.paramsdir, 'grids.json')
    mangled_data_dir = Path(options.datadir, 'mangled')
    readings_data_dir = Path(options.datadir, 'readings')
    samples_data = Path(options.datadir, 'samples.csv')
    samples_params = Path(options.paramsdir, 'samples.json')
    sites_params = Path(options.paramsdir, 'sites.csv')
    surveys_params = Path(options.paramsdir, 'surveys.csv')
    survey_map_file = Path(options.datadir, 'survey.png')

    # Grids
    _verbose(options, 'grids')
    grids_data_dir.mkdir(exist_ok=True)
    grid(_make_options(
        outdir=grids_data_dir,
        params=grids_params,
        sites=sites_params,
    ))
    Path(grids_data_dir, TOUCH).touch()

    # Genomes
    _verbose(options, 'genomes')
    genomes(_make_options(
        params=genomes_params,
        outfile=genomes_data,
    ))

    # Samples
    _verbose(options, 'samples')
    samples(_make_options(
        genomes=genomes_data,
        grids=grids_data_dir,
        outfile=samples_data,
        params=samples_params,
        sites=sites_params,
        surveys=surveys_params,
    ))

    # Assays
    _verbose(options, 'assays')
    assays(_make_options(
        genomes=genomes_data,
        outfile=assays_data,
        params=assays_params,
        samples=samples_data,
    ))

    # Plates
    _verbose(options, 'plates')
    designs_data_dir.mkdir(exist_ok=True)
    readings_data_dir.mkdir(exist_ok=True)
    plates(_make_options(
        designs=designs_data_dir,
        readings=readings_data_dir,
        assays=assays_data,
        params=assays_params,
    ))
    Path(designs_data_dir, TOUCH).touch()
    Path(readings_data_dir, TOUCH).touch()

    # Database
    _verbose(options, 'db')
    db(_make_options(
        dbfile=db_file,
        assays=assays_data,
        samples=samples_data,
        sites=sites_params,
        surveys=surveys_params,
    ))

    # Mangled plate files
    _verbose(options, 'mangled')
    mangled_data_dir.mkdir(exist_ok=True)
    mangle(_make_options(
        dbfile=db_file,
        tidy=readings_data_dir,
        outdir=mangled_data_dir,
    ))
    Path(mangled_data_dir, TOUCH).touch()

    # Survey map
    _verbose(options, 'survey')
    survey(_make_options(
        outfile=survey_map_file,
        samples=samples_data,
    ))


def _assays_parser(subparsers):
    parser = subparsers.add_parser('assays', help='construct assays')
    parser.add_argument('--genomes', type=str, required=True, help='genome file')
    parser.add_argument('--outfile', type=str, default=None, help='output file')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    parser.add_argument('--samples', type=str, required=True, help='samples file')
    parser.set_defaults(func=assays)


def _db_parser(subparsers):
    parser = subparsers.add_parser('db', help='construct database')
    parser.add_argument('--assays', type=str, required=True, help='assay data file')
    parser.add_argument('--dbfile', type=str, required=True, help='output database file')
    parser.add_argument('--samples', type=str, required=True, help='samples data file')
    parser.add_argument('--sites', type=str, required=True, help='sites parameter file')
    parser.add_argument('--surveys', type=str, required=True, help='surveys parameter file')
    parser.set_defaults(func=db)


def _everything_parser(subparsers):
    parser = subparsers.add_parser('everything', help='build everything with defaults')
    parser.add_argument('--datadir', type=str, required=True, help='output data directory')
    parser.add_argument('--paramsdir', type=str, required=True, help='input parameters directory')
    parser.add_argument('--verbose', action='store_true', help='report progress')
    parser.set_defaults(func=everything)


def _genomes_parser(subparsers):
    parser = subparsers.add_parser('genomes', help='construct genomes')
    parser.add_argument('--outfile', type=str, default=None, help='output file')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    parser.set_defaults(func=genomes)


def _grid_parser(subparsers):
    parser = subparsers.add_parser('grid', help='construct survey grid')
    parser.add_argument('--outdir', type=str, required=True, help='output directory')
    parser.add_argument('--params', type=str, required=True, help='grid parameter file')
    parser.add_argument('--sites', type=str, required=True, help='site parameter file')
    parser.set_defaults(func=grid)


def _mangle_parser(subparsers):
    parser = subparsers.add_parser('mangle', help='mangle readings files')
    parser.add_argument('--dbfile', type=str, required=True, help='database file')
    parser.add_argument('--outdir', type=str, required=True, help='output directory')
    parser.add_argument('--tidy', type=str, required=True, help='input directory')
    parser.set_defaults(func=mangle)


def _params_parser(subparsers):
    parser = subparsers.add_parser('params', help='export parameter files')
    parser.add_argument('--outdir', type=str, required=True, help='output directory')
    parser.set_defaults(func=export_params)


def _plates_parser(subparsers):
    parser = subparsers.add_parser('plates', help='construct plates')
    parser.add_argument('--assays', type=str, required=True, help='assays file')
    parser.add_argument('--designs', type=str, required=True, help='designs directory')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    parser.add_argument('--readings', type=str, required=True, help='readings directory')
    parser.set_defaults(func=plates)


def _samples_parser(subparsers):
    parser = subparsers.add_parser('samples', help='construct samples')
    parser.add_argument('--genomes', type=str, required=True, help='genome file')
    parser.add_argument('--grids', type=str, required=True, help='grids directory')
    parser.add_argument('--outfile', type=str, help='output file')
    parser.add_argument('--params', type=str, required=True, help='parameter file')
    parser.add_argument('--sites', type=str, required=True, help='sites parameter file')
    parser.add_argument('--surveys', type=str, required=True, help='surveys parameter file')
    parser.set_defaults(func=samples)


def _survey_parser(subparsers):
    parser = subparsers.add_parser('survey', help='construct survey locations')
    parser.add_argument('--outfile', type=str, required=True, help='output file name')
    parser.add_argument('--samples', type=str, required=True, help='samples data file')
    parser.set_defaults(func=survey)


def _make_options(**kwargs):
    '''Build an argparse options object.'''
    options = argparse.Namespace()
    for key, value in kwargs.items():
        setattr(options, key, value)
    return options


def _verbose(options, msg):
    '''Possibly report progress.'''
    if options.verbose:
        print(f'...{msg}')
