
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddNALFcompetitionForm(FlaskForm):
    name = StringField('Nazwa rozgrywek', validators=[DataRequired()])
    schedule_link = StringField('Link do terminarza', validators=[DataRequired()])
    table_link = StringField('Link do tabeli (opcjonalnie)')
    strikers_link = StringField('Link do strzelców', validators=[DataRequired()])
    assistants_link = StringField('Link do asystentów', validators=[DataRequired()])
    canadians_link = StringField('Link do kanadyjskiej', validators=[DataRequired()])
    submit = SubmitField('Zapisz')

