from flask import Flask, jsonify
import pandas as pd
from airtable import AirtableInterface
from dotenv import load_dotenv
from os import environ
import plotly.express as px
import plotly
from json import dumps

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

load_dotenv()

airt = AirtableInterface(environ["AIRTABLE_API_KEY"], environ['AIRTABLE_BASE_ID'], environ['AIRTABLE_TABLE_KEY'])

df = airt.get_pd_dataframe()
df['time'] = pd.to_datetime(df['time'])

# Apply the function to the 'program_name' column
df['program_name'] = df['program_name'].astype(str)
df['program_name'] = df['program_name'].apply(clean_program_name)

# Apply the function to the website column, and use program name where website is NaN
df['website_or_program'] = df['website'].apply(lambda x: extract_website_name(x) if pd.notna(x) else x)
df['website_or_program'].fillna(df['program_name'], inplace=True)
df['project'] = df['project'].astype(str)
df['website_or_program'] = df['website_or_program'].astype(str)

app = Flask(__name__)

@app.route('/category_time', methods=['GET'])
def category_time():
    grouped_data = df.groupby(['category', 'website_or_program']).size().reset_index(name='time_spent')

    fig = px.bar(grouped_data, x='category', y='time_spent', color='website_or_program', 
             title='Time Spent on Different Categories by Website/Program',
             labels={'time_spent':'Time Spent', 'website_or_program':'Website/Program'})
    graphJSON = dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
    # return jsonify(grouped_data.to_dict(orient='records'))

@app.route('/proj_time', methods=['GET'])
def proj_time():
    grouped_data = df.groupby(['project', 'website_or_program']).size().reset_index(name='time_spent')
    return jsonify(grouped_data.to_dict(orient='records'))

@app.route('/usage', methods=['GET'])
def usage():
    # Aggregate data by website/program
    usage_data = df['website_or_program'].value_counts()
    return jsonify(usage_data.to_dict(orient='records'))

@app.route('/pie_proj', methods=['GET'])
def pie_proj():
    # Aggregate data for pie chart by project
    pie_project_data = df.groupby('project').size().reset_index(name='time_spent')
    return jsonify(pie_project_data.to_dict(orient='records'))

@app.route('/pie_cat', methods=['GET'])
def pie_cat():
    # Aggregate data for pie chart by category
    pie_category_data = df.groupby('category').size().reset_index(name='time_spent')
    return jsonify(pie_category_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)