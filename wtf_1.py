from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lkuahsef.m aeflkuhc'

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

app.app_context().push()
f = MyForm()

