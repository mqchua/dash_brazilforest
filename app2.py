import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('amazon.csv')
df

##### Data Preprocessing #####

# Forest Fires by Year

df_year = df.groupby(['year']).sum().reset_index()
year_list = df_year['year'].tolist()
numbers_list = df_year['number'].tolist()

# Scatter plot

df_scatter = df.groupby(['state', 'year']).agg('sum').reset_index()

# Horizontal Bar plot

df_bar = df.groupby(['state']).sum().reset_index()

# Create a plotly figure
fig1 = go.Figure(data=go.Scatter(x=df_year.year, y=df_year.number,
                                 mode='lines+markers',
                                 line=dict(width=2, color='rgb(66, 179, 245)'),
                                 marker={
                                     'size': 20,
                                     'opacity': 0.5,
                                     'line': {'width': 0.5, 'color': 'white'}}
                                 ),
                 layout=go.Layout(title="Total Fires / Year (All States)",
                                  xaxis_title="Year",
                                  yaxis_title="Numbers",
                                  paper_bgcolor='#F6F6F2',
                                  plot_bgcolor='rgba(0, 0, 0, 0)'))
##### Initialize app #####

app = dash.Dash(__name__, external_stylesheets=[
                'https://codepen.io/chriddyp/pen/bWLwgP.css'])

##### DASH APP #####

app.layout = html.Div([

    html.Div([
        html.H1('Brazil Forest Fires')
    ], className="title"),

    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(id='bar-dropdown',
                             options=[{'label': i, 'value': i}
                                      for i in df_bar.state.unique()],
                             multi=True,
                             value=['Acre', 'Rio', 'Ceara', 'Roraima']),
            ], className='showcase'),
            html.Div([
                dcc.Graph(id='fire-1')
            ], className='showcase'),

        ], className='top-box-a'),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='state-dropdown',
                    options=[{'label': i, 'value': i}
                             for i in df.state.unique()],
                    multi=True,
                    value=['Acre', 'Paraiba']),
            ], className='showcase'),
            html.Div([
                dcc.Graph(id='fire-2')], className='showcase'),
        ], className='top-box-b'),

        html.Div([dcc.Graph(id='plot', figure=fig1)], className='top-box-c'),

    ], className='top-container')

], className='wrapper')

##### CALLBACKS #####


@app.callback(Output('fire-1', 'figure'), [Input('bar-dropdown', 'value')])
def update_figure(state_values):

  dff = df_bar.loc[df_bar['state'].isin(state_values)]

  return {
      'data': [go.Bar(
          x=dff[dff['state'] == state]['number'],
          y=dff[dff['state'] == state]['state'],
          text="State: " +
          f"{dff[dff['state'] == state]['state'].unique()[0]}",
          name=state, orientation='h'
      ) for state in dff.state.unique()],  # For loop for state in data

      'layout': go.Layout(
          title="Total Forest Fires / State",
          xaxis={'title': 'Numbers'},
          yaxis={'title': ''},
          # margin={'l': 90, 'b': 50, 't': 80, 'r': 0},
          hovermode='closest',
          paper_bgcolor='#F6F6F2',
          plot_bgcolor='rgba(0, 0, 0, 0)')}


@app.callback(Output('fire-2', 'figure'), [Input('state-dropdown', 'value')])
def update_graph(state_values):
  dff = df_scatter.loc[df_scatter['state'].isin(state_values)]

  return {
      'data': [go.Scatter(
          x=dff[dff['state'] == state]['year'],
          y=dff[dff['state'] == state]['number'],
          text="State: " +
          f"{dff[dff['state'] == state]['state'].unique()[0]}",
          mode='lines+markers',
          name=state,
          marker={
              'size': 12,
              'opacity': 0.5,
              'line': {'width': 0.5, 'color': 'white'}
          }
      ) for state in dff.state.unique()],  # For loop for state in data

      'layout': go.Layout(
          title="State Fire Comparison / Year",
          xaxis={'title': 'Year'},
          yaxis={'title': ''},
          # margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
          hovermode='closest',
          paper_bgcolor='#F6F6F2',
          plot_bgcolor='rgba(0, 0, 0, 0)'
      )
  }


if __name__ == '__main__':
  app.run_server(debug=True)
