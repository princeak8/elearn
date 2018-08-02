from flask import Flask, render_template, url_for, request, session, redirect, json, jsonify
from models.models import mongo, Student, Instructor, Interest, Student_interest, Course_interest, Course, Lesson, Student_subscription
from forms import SignupForm, LoginForm
import bcrypt
import locale
from bson import ObjectId
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import json

class LoginController():

	def student_login(self):
		form = LoginForm()
		if request.method == 'POST':
			students = mongo.db.students
			login_student = students.find_one({'email' : request.form['email']})

			if form.validate() == False:
				errors = ''
				if form.email.errors:
					for error in form.email.errors:
						errors += ' '+error
					#return json.dumps({'message':errors});

				if form.password.errors:
					for error in form.password.errors:
						errors += ' '+error
					return json.dumps({'status':'ERROR','message':errors});

			if login_student:
				if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_student['password'].encode('utf-8')) == login_student['password'].encode('utf-8'):
					session['student'] = {}
					#session['cart'] = {}
					#session['mylist'] = {}
					#session['cart']['key'] = 'val'
					#session['mylist']['key'] = 'val'
					#session['student']['id'] = login_student['_id']
					if isinstance(login_student['_id'], ObjectId):
						session['student']['id'] = str(login_student['_id'])
					else:
						session['student']['id'] = login_student['_id']

					session['student']['email'] = login_student['email']
					session['student']['name'] = login_student['name']
					return json.dumps({'status':'OK','message':'Login Successfull'});

			return json.dumps({'status':'ERROR','message':'Invalid email/password Combination'});


	def instructor_login(self):
		session['instructor_login_error'] = {}

		form = LoginForm()

		if request.method == 'POST':
			instructors = mongo.db.instructors
			login_instructor = instructors.find_one({'email' : request.form['email']})

			if form.validate() == False:
				errors = ''
				if form.email.errors:
					for error in form.email.errors:
						errors += ' '+error
					#return json.dumps({'message':errors});

				if form.password.errors:
					for error in form.password.errors:
						errors += ' '+error
					return render_template('instructor_login.html', form=form)

			if login_instructor:
				if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_instructor['password'].encode('utf-8')) == login_instructor['password'].encode('utf-8'):
					session['instructor'] = {}
					if isinstance(login_instructor['_id'], ObjectId):
						session['instructor']['id'] = str(login_instructor['_id'])
					else:
						session['instructor']['id'] = login_instructor['_id']

					session['instructor']['email'] = login_instructor['email']
					session['instructor']['name'] = login_instructor['name']
					return redirect(url_for('instructor_dashboard'))

			session['instructor_login_error'] = 'Incorrect Email/Password'
			return render_template('instructor_login.html', form=form)

		return render_template('instructor/login.html', form=form)