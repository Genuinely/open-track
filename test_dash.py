import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from airtable import AirtableInterface
from dotenv import load_dotenv
from os import environ

load_dotenv()

airt = AirtableInterface(environ["AIRTABLE_API_KEY"], environ['AIRTABLE_BASE_ID'], environ['AIRTABLE_TABLE_KEY'])
df = airt.get_pd_dataframe()

df['time'] = pd.to_datetime(df['time'])

def extract_website_name(website):
    if '/' in website:
        return website.split('/')[0]
    if "main.google.com" in website:
        return "gmail.com"
    return website

def clean_program_name(program_name):
    cleaned_name = program_name.strip()

    if cleaned_name.startswith('[') and cleaned_name.endswith(']'):
        cleaned_name = cleaned_name[1:-1]
    
    cleaned_name = cleaned_name.replace("'", "")

    return cleaned_name

# Apply the function to the 'program_name' column
df['program_name'] = df['program_name'].astype(str)
df['program_name'] = df['program_name'].apply(clean_program_name)

# Apply the function to the website column, and use program name where website is NaN
df['website_or_program'] = df['website'].apply(lambda x: extract_website_name(x) if pd.notna(x) else x)
df['website_or_program'].fillna(df['program_name'], inplace=True)
df['project'] = df['project'].astype(str)
df['website_or_program'] = df['website_or_program'].astype(str)

# Start Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Dropdown(
        id='selection-dropdown',
        options=[
            {'label': i, 'value': i} for i in df['project'].unique()
        ] + [
            {'label': i, 'value': i} for i in df['category'].unique()
        ],
        value=df['project'].unique()[0]  # default value
    ),
    dcc.Graph(id='pie-chart')
])

# Callback to update pie-chart based on dropdown selection
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('selection-dropdown', 'value')]
)
def update_pie_chart(selected_value):
    if selected_value in df['project'].unique():
        filtered_df = df[df['project'] == selected_value]
    else:
        filtered_df = df[df['category'] == selected_value]

    fig = px.pie(filtered_df, names='website_or_program', 
                 title=f'Time Spent Breakdown for {selected_value}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)