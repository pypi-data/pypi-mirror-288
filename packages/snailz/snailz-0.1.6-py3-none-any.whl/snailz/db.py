'''Generate database from data files.'''

import json
import polars as pl


ISO_DATE = "%Y-%m-%d"


def db(options):
    '''Main driver.'''
    url = f'sqlite:///{options.dbfile}'

    _csv_to_db(url, 'sample', options.samples)
    _csv_to_db(url, 'site', options.sites)
    _csv_to_db(url, 'survey', options.surveys, dates=['date'], columns=['survey_id', 'site_id', 'date'])

    assays = json.load(open(options.assays, 'r'))
    _json_to_db(url, assays, 'staff')
    _json_to_db(url, assays, 'experiment', dates=['start', 'end'])
    _json_to_db(url, assays, 'performed')
    _json_to_db(url, assays, 'plate', dates=['date'])
    _json_to_db(url, assays, 'invalidated', dates=['date'])


def _csv_to_db(url, name, source, dates=[], columns=[]):
    '''Create table from CSV.'''
    df = pl.read_csv(source)
    if columns:
        df = df[columns]
    df = _convert_dates(df, dates)
    df.write_database(name, url, if_table_exists='replace')


def _json_to_db(url, data, name, dates=[]):
    '''Create table from JSON.'''
    df = pl.DataFrame(data[name])
    df = _convert_dates(df, dates)
    df.write_database(name, url, if_table_exists='replace')


def _convert_dates(df, dates):
    '''Convert text columns to dates.'''
    for colname in dates:
        df = df.with_columns(pl.col(colname).str.to_date(ISO_DATE))
    return df
