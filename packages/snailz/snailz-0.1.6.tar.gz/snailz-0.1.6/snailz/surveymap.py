'''Create map of survey points.'''

import plotly.graph_objects as go
import polars as pl


def surveymap(options):
    '''Main driver.'''
    samples = pl.read_csv(options.samples)['survey_id', 'lon', 'lat']
    fig = go.Figure(go.Scattermapbox(
        lon=samples['lon'],
        lat=samples['lat'],
        marker=go.scattermapbox.Marker(color=samples['survey_id']),
    ))
    fig.update_layout(
        mapbox={
            'style': 'open-street-map',
            'center': {'lon': -124.2, 'lat': 48.85},
            'zoom': 11,
        },
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
    )
    if options.outfile:
        fig.write_image(options.outfile)
    else:
        fig.show()
