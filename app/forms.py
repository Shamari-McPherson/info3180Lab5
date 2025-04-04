# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length

class MovieForm(FlaskForm):
    title = StringField('Movie Title', 
        validators=[
            DataRequired(message='Movie title is required'),
            Length(min=2, max=100, message='Title must be between 2 and 100 characters')
        ]
    )
    
    description = TextAreaField('Movie Description', 
        validators=[
            DataRequired(message='Movie description is required'),
            Length(min=10, max=500, message='Description must be between 10 and 500 characters')
        ]
    )
    
    poster = FileField('Movie Poster', 
        validators=[
            FileRequired(message='Movie poster is required'),
            FileAllowed(['jpg', 'png', 'jpeg'], message='Only image files are allowed')
        ]
    )