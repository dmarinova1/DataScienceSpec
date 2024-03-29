#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Statistics Dashboard",
            style={'textAlign': 'center', 'color': 'red'}),
    html.Div([
        html.Div(
            html.Label("Select Statistics:",
                   style={ 'color': 'white','font-weight': 'bold','font': '18px Arial, Helvetica, sans-serif'}
                   ),
            style={'width': '60%','height':'30px','margin-left':'50px','padding':'15px'}

        ),

        dcc.Dropdown(
            id='select-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',
            placeholder='Select Statistics',
            style={
    'font-weight': 'bold',
    'font': '18px Arial, Helvetica, sans-serif'}
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=1980
        )),
    html.Div([
        html.Div(id='output-container', className='output-container', style={'width': '100%','margin':'auto', 'display': 'inline-block'}),
    ])
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='select-statistics', component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-statistics', component_property='value'),
    Input(component_id='select-year', component_property='value')])

def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

#TASK 2.5: Create and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(recession_data, x='Year', y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))

#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        # use groupby to create relevant data for plotting

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
            title="Average Number of Vehicles Sold by Vehicle Type during Recession Period")
        )
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
        figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
            title="Total Expenditure Share by Vehicle Type during Recession Period")
        )

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        unemployment_effect = recession_data.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemployment_effect, x='Unemployment_Rate', y='Automobile_Sales', color='Vehicle_Type',
            title="Effect of Unemployment Rate on Vehicle Type and Sales during Recession Period")
        )

        
        # Return the charts as a list
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1)],style={'margin-bottom': '20px'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart2)],style={'margin-bottom': '20px'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3)],style={'margin-bottom': '20px'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart4)],style={'margin-bottom': '20px'})
            ]

# TASK 2.6: Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots                             
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]
                              
#TASK 2.5: Creating Graphs Yearly data
                           
#plot 1 Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title=f'Yearly Automobile Sales'))
        
# Plot 2 Total Monthly Automobile sales using line chart.
        Y_chart2 = dcc.Graph(figure=px.bar(yearly_data, x='Month', y='Automobile_Sales', title=f'Monthly Automobile Sales in {input_year}'))

            # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                      title=f'Average Vehicles Sold by Vehicle Type in the year {input_year}')
        )
            # Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                      title=f'Total Advertisement Expenditure by Vehicle Type in the year {input_year}')
        )

#TASK 2.6: Returning the graphs for displaying Yearly data

        return [
                html.Div(className='chart-item', children=[html.Div(children=Y_chart1)],style={'margin-bottom': '20px'}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart2)],style={'margin-bottom': '20px'}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart3)],style={'margin-bottom': '20px'}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart4)],style={'margin-bottom': '20px'})
                ]
        
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

