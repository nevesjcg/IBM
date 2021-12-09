# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
#import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()



# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),

                                html.Div(dcc.Dropdown(id='site-dropdown',
                                                options=[{'value': x, 'label': x} 
                                                    for x in ['ALL', 'CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40']],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                )),
                                html.Br(),
                                html.Div(id='dd-output-container'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                dcc.Graph(id='success-pie-chart'),

                                
                                # TASK 3: Add a slider to select payload range
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                html.Br(),
                                dcc.RangeSlider(
                                        id='payload-slider',
                                        min=0, 
                                        max=10000, 
                                        step=1000,
                                        marks={
                                            0:      '0', 
                                            2500:   '2500',
                                            5000:   '5000',
                                            7500:   '7500',
                                            10000:  '10000'
                                            },
                                        value=[0, 10000]),
                                html.Br(),
                                #html.Div(id='output-container-range-slider'), 
                                #html.Br(),
                            

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 1:

@app.callback(
    Output('dd-output-container', 'children'),
    Input('site-dropdown', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')])
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, 
                        values='class', 
                        names='Launch Site', 
                        title='Total Success Launches By Site')
    else:
        data = filtered_df.loc[filtered_df['Launch Site'] == str(entered_site)]
        fig = px.pie(data, 
                        values='Payload Mass (kg)',
                        names='class', 
                        title='Total Success Launches for Site {}'.format(entered_site))
    return fig

 
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output("success-payload-scatter-chart", "figure"), 
    [Input("site-dropdown", "value")],
    [Input("payload-slider", "value")])
def update_bar_chart(entered_site, slider_range):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        low, high = slider_range
        mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            filtered_df[mask], 
            x="Payload Mass (kg)", 
            y="class", 
            color="Booster Version Category",
            title="Correlation between Payload and Success for all Sites"
             )
    else:
        data = filtered_df.loc[filtered_df['Launch Site'] == str(entered_site)]
        low, high = slider_range
        mask = (data['Payload Mass (kg)'] > low) & (data['Payload Mass (kg)'] < high)
        fig = px.scatter(
            data[mask], 
            x="Payload Mass (kg)", 
            y="class", 
            color="Booster Version Category",
            title="Correlation between Payload and Success for Site {}".format(entered_site),
            hover_data=['Payload Mass (kg)']
            )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# cd /Users/joseclaudioguedesdasneves/Cursos/IBM/Data\ Science\ and\ Machine\ Learning\ Capstone\ Project/Module\ 3\ -\ Interactive\ Visual\ Analytics\ and\ Dashboard/

""" options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                ], """