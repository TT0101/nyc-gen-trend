# -*- coding: utf-8 -*-
"""
See here: https://dash.plot.ly/urls
"""

import dash
from flask import Flask

#app = dash.Dash()
#server = app.server
#comment the above and uncomment below and Flask to work on server
fServer = Flask(__name__)
app = dash.Dash(__name__, server=fServer, static_folder='static', url_base_pathname='/')
app.config.suppress_callback_exceptions = True



