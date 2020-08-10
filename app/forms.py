from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Regexp, NumberRange, ValidationError
import re
import os
from dotenv import load_dotenv

import berserk
from requests_oauthlib import OAuth2Session

load_dotenv(".env")
client_id = os.environ.get("CLIENT_ID")

session = OAuth2Session(client_id)
client = berserk.Client(session)

def validate_username(form, field):
    if client.users.get_by_id(field.data) == []:
        raise ValidationError("Invalid input syntax")

class UsernameForm(FlaskForm):
    white = StringField('White Username', validators=[DataRequired(), validate_username])
    black = StringField('Black Username', validators=[DataRequired(), validate_username])
    evaluation = StringField('Stockfish Evaluation', validators=[DataRequired(),
                    Regexp("(^#-?[0-9]+$)|(^-?[0-9.]+$)", message="Please.")])
    white_clock = IntegerField('White Clock', validators=[DataRequired(),
    NumberRange(min=0)])
    black_clock = IntegerField('Black Clock', validators=[DataRequired(),
    NumberRange(min=0)])
    perf = SelectField('Time Control', choices=[('UltraBullet', 'UltraBullet'),
                                                ('Bullet', 'Bullet'),
                                                ('Blitz', 'Blitz'),
                                                ('Rapid', 'Rapid') ])
    submit = SubmitField('Go')
