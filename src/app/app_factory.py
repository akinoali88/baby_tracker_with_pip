'''
Generated Dash application factory module.
Includes functions to create Plotly figures and initialize the Dash app.
'''

from dash import Dash, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd


from .dashboard_logic import get_slider_params
from .components import (
    render_home_tab,
    render_individual_feeds_tab,
    render_night_vs_day_feeding,
)


def create_dash_app(df: pd.DataFrame,
                    daily_df: pd.DataFrame,
                    weekly_df: pd.DataFrame) -> Dash:
    '''
    Create and configure a Dash application for baby feeding schedule visualization.

    Parameters:    
        df : pd.DataFrame
            DataFrame containing aggregated or processed feeding data with 'age_in_weeks' column.
            Used for generating statistical visualizations.
        daily_df : pd.DataFrame
            DataFrame containing daily feeding data with columns 
                including 'age_in_weeks' and 'name'.
            Each row represents a single feeding event.
        weekly_df : pd.DataFrame
            DataFrame containing weekly aggregated feeding data, setting out
            the weekly volume of night versus day feeds per child. 
            See data_pipeline for definitions of night vs day feed.


    Returns:
        Dash
            Configured Dash application instance with interactive layout, callbacks, and graphs.
            The app includes a range slider for filtering data by age (in weeks) and dynamically
            updates two feed volume charts and a text display based on slider selection.

    Notes:
        - The range slider automatically calculates its range from the maximum age in daily_df.
        - Default slider range is set from 0 weeks to the lowest maximum age across all children.
        - Slider marks are displayed at 2-week intervals with descriptive labels.
        - The app includes a callback that updates both figures and a text display when the
        slider range is modified by the user.
    '''

    # load bootstrap figure templates
    load_figure_template('minty')
    dbc_css = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css'

    app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc_css, dbc.icons.BOOTSTRAP])

    # get slider params
    slider_parameters = get_slider_params(daily_df)
    default_child = slider_parameters['children']['value']

    # Define the app layout
    app.layout = dbc.Container([

            # Store the data as JSON in the browser/app state
            dcc.Store(id='stored-main-data', data=df.to_json(orient='records')),
            dcc.Store(id='stored-daily-data', data=daily_df.to_json(orient='records')),
            dcc.Store(id='stored-weekly-data', data=weekly_df.to_json(orient='records')),

            dbc.Tabs([

                # --- Home page tab ---
                dbc.Tab([
                    render_home_tab(daily_df, slider_parameters, default_child)],
                    label='Home: daily feed summary',
                    label_class_name='bg-primary-subtle text-grey',
                    ),

                # --- Individual feeding tabs ---
                dbc.Tab([
                    render_individual_feeds_tab(
                        df, slider_parameters, default_child)],
                    label='Individual feed summary',
                    label_class_name='bg-primary-subtle text-grey',
                    ),

                # --- Night vs day feeding tab ---
                dbc.Tab([
                    render_night_vs_day_feeding(
                        weekly_df, default_child)],
                    label='Night vs Day feeding',
                    label_class_name='bg-primary-subtle text-grey',
                    ),
                    ]) # Close dcc.Tabs
        ],
        fluid=True,
        className='bg-success',
        style={'minHeight': '100vh'}) # Close dbc.Container

    return app
