from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,RadioField, FileField,TextAreaField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Required, Length, EqualTo
from ..models import User
# from wtforms import ValidationError



class FormCategory(FlaskForm):
    name = StringField('Category Name', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Submit')
    
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
   
    submit = SubmitField('Submit')


class FormPitch(FlaskForm):
    title = StringField('Pitch Title', validators=[Required(), Length(1, 64)])
    author = StringField('Author : ', validators=[Required()])
    category = RadioField('Pitch Category', choices = [('businesspitch', 'Business Pitch'),  ('lyricspitch', ' Lyrics Pitch'), ('advertisementpitch', 'Advertisement Pitch'),('relationshippitch' , 'Relationship Pitch')], validators = [Required()])
    content = TextAreaField('Pitch Content', validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm():
    content = TextAreaField('Pitch Content', validators=[Required()])
    submit = SubmitField('Submit')

