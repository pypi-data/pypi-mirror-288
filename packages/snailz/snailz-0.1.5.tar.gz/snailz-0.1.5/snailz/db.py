'''Generate database from data files.'''

import json
import polars as pl


def db(options):
    '''Main driver.'''
    url = f'sqlite:///{options.dbfile}'

    _csv_to_db(url, 'sample', options.samples)
    _csv_to_db(url, 'site', options.sites)
    _csv_to_db(url, 'survey', options.surveys, 'survey_id', 'site_id', 'date')

    assays = json.load(open(options.assays, 'r'))
    _json_to_db(url, assays, 'staff')
    _json_to_db(url, assays, 'experiment')
    _json_to_db(url, assays, 'performed')
    _json_to_db(url, assays, 'plate')
    _json_to_db(url, assays, 'invalidated')


def _csv_to_db(url, name, source, *columns):
    '''Create table from CSV.'''
    df = pl.read_csv(source)
    if columns:
        df = df[list(columns)]
    df.write_database(name, url, if_table_exists='replace')


def _json_to_db(url, data, name):
    '''Create table from JSON.'''
    df = pl.DataFrame(data[name])
    df.write_database(name, url, if_table_exists='replace')
