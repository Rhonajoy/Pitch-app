from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField,TextAreaField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import User
# from wtforms import ValidationError



class FormCategory(FlaskForm):
    name = StringField('Category Name', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Submit')
    
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
class AddPitch(FlaskForm):
    title = StringField('Pitch Title', validators=[Required(), Length(1, 64)])
    category = StringField('Pitch Title', validators=[Required(), Length(1, 64)])
    body = TextAreaField('Pitch Content', validators=[Required()])
    submit = SubmitField('Submit')
