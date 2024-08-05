'''Generate random plates.'''

import csv
import json
from pathlib import Path
import random
import sys

from .params import AssayParams, load_params


MODEL = 'Weyland-Yutani 470'
PLATE_HEIGHT = 4
PLATE_WIDTH = 4


def plates(options):
    '''Main driver.'''
    options.params = load_params(AssayParams, options.params)
    random.seed(options.params.seed)
    _create_files(options)


def _create_files(options):
    '''Create randomized plate files.'''
    for filename, sample_id, kind in _join_assay_data(options):
        _make_plate(
            options.params,
            sample_id,
            kind,
            Path(options.designs, filename),
            Path(options.readings, filename),
        )


def _generate(params, func):
    '''Make body of plate design or results.'''
    title_row = ['', *[chr(ord('A') + col) for col in range(PLATE_WIDTH)]]
    values = [
        [func(params, _make_placement) for col in range(PLATE_WIDTH)]
        for row in range(PLATE_HEIGHT)
    ]
    labeled = [[str(i + 1), *r] for (i, r) in enumerate(values)]
    return [title_row, *labeled]


def _join_assay_data(options):
    '''Get experiment type and plate filename from data.'''
    assays = json.load(open(options.assays, 'r'))
    experiments = {x['sample_id']: x['kind'] for x in assays['experiment']}
    plates = {p['filename']: p['sample_id'] for p in assays['plate']}
    return ((f, plates[f], experiments[plates[f]]) for f in plates)


def _make_head(kind, sample_id):
    '''Make head of plate.'''
    return [
        [MODEL, kind, sample_id],
        [],
    ]


def _make_placement(kind):
    '''Generate random placement of samples.'''
    placement = [[False for col in range(PLATE_WIDTH)] for row in range(PLATE_HEIGHT)]
    if kind == 'calibration':
        return placement, []
    columns = list(c for c in range(PLATE_WIDTH))
    random.shuffle(columns)
    columns = columns[:PLATE_HEIGHT]
    for r, row in enumerate(placement):
        row[columns[r]] = True
    return placement, columns


def _make_plate(params, sample_id, kind, design_file, readings_file):
    '''Generate an entire plate.'''
    placement, sample_locs = _make_placement(kind)

    design = [*_make_head('design', sample_id), *_generate(params, _make_treatment)]
    _save(design_file, _normalize_csv(design))

    readings = [*_make_head('readings', sample_id), *_generate(params, _make_reading)]
    _save(readings_file, _normalize_csv(readings))


def _make_reading(params, treated):
    '''Generate a single plate reading.'''
    mean = params.treated_val if treated else params.control_val
    value = max(0.0, random.gauss(mean, params.stdev))
    return f'{value:.02f}'


def _make_treatment(params, treated):
    '''Generate a single plate treatment.'''
    return params.treatment if treated else random.choice(params.controls)


def _normalize_csv(rows):
    required = max(len(r) for r in rows)
    for row in rows:
        row.extend([''] * (required - len(row)))
    return rows


def _save(filename, rows):
    '''Save as CSV.'''
    if not filename:
        csv.writer(sys.stdout).writerows(rows)
    else:
        csv.writer(open(filename, 'w'), lineterminator='\n').writerows(rows)
