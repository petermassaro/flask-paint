from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length


class QuoteRequestForm(FlaskForm):
	customer = StringField('Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	street = StringField('Street Address', validators=[DataRequired()])
	city = StringField('City', validators=[DataRequired()])
	state = StringField('State', validators=[DataRequired()])
	zip_code = StringField('Zip Code', validators=[DataRequired()])
	phone = StringField('Phone', validators=[DataRequired()])
	time = StringField('Time')
	description = TextAreaField('Description (Optional)')
	submit = SubmitField('Submit')


class JobDataForm(FlaskForm):
	customer = StringField("Customer", validators=[DataRequired()])
	room_volume = IntegerField("Room Volume", validators=[DataRequired()])
	wall_area = IntegerField("Wall Area", validators=[DataRequired()])
	window_area = IntegerField("Window Area", validators=[DataRequired()])
	door_area = IntegerField("Door Area", validators=[DataRequired()])
	patchwork = BooleanField("Patchwork Required")
	damages = BooleanField("Damages (Y/N)")
	trim = BooleanField("Trim Required (Y/N)")
	current_sheen = StringField("Current Sheen")
	current_color = StringField("Current Color")
	previous_paint = SelectField("Previous Paint", choices=[('oil','Oil'),('latex', 'Latex')])
	other = TextAreaField("Other")
	submit = SubmitField("Submit Job")