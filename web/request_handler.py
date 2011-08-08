#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   request_handler.py - the web framework 
#
#   PURPOSE: Serve web pages, handle javascript requests, and pass them on to
#   the serial deriver via RPC.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 8th August 2011
#
#   LICENSE: GNU GPL
#
#################################################

from flask import Flask, render_template, request, flash
from flaskext.wtf import Form, TextField
from flaskext.wtf import validators as v

import sys
sys.path.append('../serial')
from serial_client import set_states

app = Flask(__name__)
# TODO make secret key more secret
app.secret_key = '''\xf9\xae!\xca\xae\x1a\xd6k\xf3\xd1\xc3\xb18~\xe2V"\x89=`q\xde\x91\xe4'''

class ControlForm(Form):
    a_state = TextField('State of port A', 
            validators=[v.Required(), v.Length(min=8, max=8)])
    b_state = TextField('State of port B',
            validators=[v.Required(), v.Length(min=8, max=8)])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ControlForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        ret_a, ret_b = set_states(form.a_state.data, form.b_state.data)
        flash(ret_a)
        flash(ret_b)
    return render_template("index.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)