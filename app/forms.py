from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, IntegerField, HiddenField, FileField
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

class LessonForm(Form):
	title = StringField('Title:', validators=[DataRequired("Enter the Title")])
	video_url = StringField('Video URL:', validators=[DataRequired("Enter the Lesson Video Url")])
	description = TextAreaField('Description:', validators=[DataRequired("Enter the description of the lesson")])
	duration = IntegerField('Duration:', validators=[DataRequired("Enter the Duration of Lesson in Minutes")])
	course_id = HiddenField()
	lesson_id = HiddenField()
	submit = SubmitField('SUBMIT')

class CourseForm(Form):
	title = StringField('Title:', validators=[DataRequired("Enter the Title")])
	cover_photo = FileField('Cover Photo:', validators=[DataRequired("Upload Cover Photo")])
	description = TextAreaField('Description:', validators=[DataRequired("Enter the description of the course")])
	instructor_id = HiddenField()
	submit = SubmitField('SUBMIT')

class EditCourseForm(Form):
	title = StringField('Title:', validators=[DataRequired("Enter the Title")])
	cover_photo = FileField('Cover Photo:')
	description = TextAreaField('Description:', validators=[DataRequired("Enter the description of the course")])
	course_id = HiddenField()
	instructor_id = HiddenField()
	submit = SubmitField('SUBMIT')
