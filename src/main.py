'''
Baby Feeding Schedules Main Application Module

This module serves as the entry point for the Baby Feeding Schedules application.
It orchestrates the data processing pipeline for multiple children, exports processed
data to Excel files, and creates an interactive Dash dashboard for visualization.

Workflow:
1. Initializes DataPipeline objects for each child defined in settings
2. Processes raw feeding schedule data for each child
3. Exports processed data and validation errors to Excel
4. Combines data from all children across different time periods (raw, daily, weekly)
5. Launches a Dash web application with interactive charts and visualizations

Dependencies:
    - pandas: Data manipulation and concatenation
    - src.pipeline.data_pipeline: DataPipeline class for data processing
    - src.app.app_factory: Dash app creation factory
    - src.models.children: Child settings and configuration

Global Variables:
    child_pipelines (list): Stores DataPipeline objects for each child
    Amelia_data (DataPipeline): Processed pipeline for Amelia
    Ayla_data (DataPipeline): Processed pipeline for Ayla
    combined_data (pd.DataFrame): Concatenated transformed data from all children
    combined_daily_data (pd.DataFrame): Concatenated daily aggregated data from all children
    combined__weekly_data (pd.DataFrame): Concatenated weekly aggregated data from all children
    app (Dash): Dash application instance

Note:
    The application runs on localhost:8051 in debug mode with reloader disabled.
'''

import pandas as pd

from pipeline.data_pipeline import DataPipeline
from app.app_factory import create_dash_app
from models.children import settings

# Run data pipelines for each child
# hold your processed DataPipeline objects
child_pipelines = []

for child in settings.children:
    pipeline = DataPipeline(
        name=child.name,
        file_name=child.file_name,
        dob=child.dob
    )
    child_pipelines.append(pipeline)

# Get individual child data pipelines
Amelia_data = child_pipelines[0]
Ayla_data = child_pipelines[1]

# Run data piepline
Ayla_data.process()
Amelia_data.process()

# Export processed data to Excel files
Amelia_data.export_data(
    output_file_name="Amelia_feeding_schedule.xlsx",
    export_errors=True,
    export_validated=True
)
# Create charts
combined_data = pd.concat(
    [Ayla_data.transformed_data, Amelia_data.transformed_data],
    )

combined_daily_data = pd.concat(
    [Ayla_data.daily_data, Amelia_data.daily_data],
    )

combined__weekly_data = pd.concat(
    [Ayla_data.weekly_data, Amelia_data.weekly_data],
    )

# Create Dash app
if __name__ == "__main__":
    app = create_dash_app(combined_data, combined_daily_data, combined__weekly_data )
    app.run(debug=True, use_reloader=False, port=8051)
    server = app.server
