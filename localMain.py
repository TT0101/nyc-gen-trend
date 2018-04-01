# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 10:55:46 2018

@author: theresa
"""
import dash
import nycgenheatmap as home

#run (for local only...if you want to see the app run on your machine, use this not main.py (that's for pythonanywhere to work))
if __name__ == '__main__':
    app = dash.Dash()
    app = home.runMapPage(app)
    app.run_server(debug=True)
    