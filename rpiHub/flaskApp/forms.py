from wtforms import Form, TextField, TextAreaField,validators
from wtforms import StringField,SubmitField

class ExperimentForm(Form):
    name = TextField('Name: ', validators=[validators.required()])
    description = TextField('Description: ', validators=[validators.required()])
