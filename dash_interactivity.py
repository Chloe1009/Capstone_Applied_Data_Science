import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

data=pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')

max_payload=data['Payload Mass (kg)'].max()
min_payload=data['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout=html.Div([
     html.H1("SpaceX Launch Records Dashboard",style={'color': '#503D36', 'font-size': 24}),
     html.Div([
          dcc.Dropdown(id='site-dropdown',
                     options=[
                             {'label': 'All Sites', 'value': 'ALL'},
                             {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                             {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                             {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                             {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                     ],
                     value='ALL',
                     placeholder='Select a Launch Site here',
                     searchable=True
        ),

        html.Div([
         dcc.RangeSlider(
             id='payload-slider',
             min=0, max=10000,step=1000,
             marks={0: '0',
                    100: '100'},
             value=[min_payload, max_payload]
         )
        ]),

        html.Div(dcc.Graph(id='success-pie-chart')),
        
        html.Div(
         dcc.Graph(id='success-payload-scatter-chart')
        )
     ])
])
    
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = data
    if entered_site == 'ALL':
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Success Count for all launch sites')
        return fig
    else:
        filtered_df=data[data['Launch Site']== entered_site]
        filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(filtered_df,values='class count',names='class',title=f"Total Success Launches for site {entered_site}")
        return fig
        # return the outcomes piechart for a selected site

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider',component_property='value')]
)
def scatter(entered_site, payload):
    filtered_df=data[data['Payload Mass (kg)'].between(payload[0],payload[1])]
    
    if entered_site=='ALL':
        fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Success count on Payload mass for all sites')
        return fig
    else:
        fig=px.scatter(filtered_df[filtered_df['Launch Site']==entered_site],x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f"Success count on Payload mass for site {entered_site}")
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)