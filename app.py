# -*- coding: utf-8 -*-
"""
See here: https://dash.plot.ly/urls
"""

import dash
from flask import Flask

fServer = Flask(__name__)
app = dash.Dash(__name__, server=fServer, static_folder='static', url_base_pathname='/')
app.config.suppress_callback_exceptions = True



