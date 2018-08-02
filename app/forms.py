from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
	name = StringField('Name:', validators=[DataRequired("Please enter your Fullname")])
	email = StringField('Email:', validators=[DataRequired("Please enter your Email"), Email("Enter a valid Email")])
	password = PasswordField('Password:', validators=[DataRequired("Please enter your Password"), Length(min=6, message="Passwords must be 6 characters or more.")])
	phone = StringField('Phone Number:', validators=[DataRequired("Please enter your Phone Number")])
	submit = SubmitField('Sign Up')

class LoginForm(Form):
	email = StringField('Email:', validators=[DataRequired("Please enter your Email"), Email("Enter a valid Email")])
	password = PasswordField('Password:', validators=[DataRequired("Please enter your Password")])
	submit = SubmitField('Login')

class QuestionForm(Form):
	question = TextAreaField('Question:', validators=[DataRequired("Please enter your Question Here")])
	submit = SubmitField('ASK')