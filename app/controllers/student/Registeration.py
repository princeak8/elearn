from flask import Flask, render_template, url_for, request, session, redirect, json, jsonify
from models.models import mongo, Student, Instructor, Interest, Student_interest, Course_interest, Course, Lesson, Student_subscription
from forms import SignupForm, LoginForm
import bcrypt
import locale
from bson import ObjectId
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import json

class RegisterationController():

	def signup():
		form = SignupForm()

		if request.method == 'POST':
			if form.validate() == False:
				return render_template('signup.html', form=form)
			else:
				session['student'] = {}
				newStudent = Student()
				id = newStudent.add(form.name.data, form.email.data, form.password.data, form.phone.data)
				session['student']['id'] = id
				session['student']['name'] = form.name.data
				session['student']['email'] = form.email.data
				return redirect(url_for('select_interests'))

		return render_template('signup.html', form=form)