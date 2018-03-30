import dash
import dash_html_components as html

from flask import Flask

#app files
import basicMapWithPolygonsWorking as test

fServer = Flask(__name__)
initLayout = html.Div(id='page-content', children="init")
app = dash.Dash(__name__, server=fServer, static_folder='static', url_base_pathname='/')
app.layout = initLayout

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app = test.run(app)