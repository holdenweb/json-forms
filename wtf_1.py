from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "lkuahsef.m aeflkuhc"


class MyForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])


import flask.ctx

ctx = flask.ctx.AppContext(app)
ctx = flask.ctx.RequestContext(app, {})
ctx.push()
f = MyForm()
