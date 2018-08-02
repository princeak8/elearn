from flask import Flask, render_template, url_for, request, session, redirect, json, jsonify
from models.models import mongo, Student, Instructor, Interest, Student_interest, Course_interest, Course, Lesson, Student_subscription, Student_question

from forms import CourseForm
import bcrypt
import locale
from bson import ObjectId
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import json

class InstructorController():
	loggedIn = False

	def  __init__(self):
		if 'instructor' in session:
			self.loggedIn = True
		else:
			return redirect(url_for('instructor_login'))

		self.newInstructor = Instructor()
		self.newStudent_interest = Student_interest()
		self.newCourse_interest = Course_interest()
		self.newInterest = Interest()
		self.newCourse = Course()
		self.newStudent_subscription = Student_subscription()
		self.newStudent_question = Student_question()

	def dashboard_data(self):
		data = {}
		data['logged_in'] = True 
		data['courses'] = []
		data['instructor'] = self.newInstructor.get_instructor_by_name(session['instructor']['name'])
		fields = {"instructor_id":data['instructor']['_id']}
		courses = self.newCourse.get_courses(fields)
		data['new_course_form'] = CourseForm()
		data['new_course_form'].instructor_id.data = data['instructor']['_id']
		if courses:
			for course in courses:
				course_subscription = self.newStudent_subscription.get_course_subscriptions(course['_id'])
				course['subscribed'] = course_subscription.count()
				questions = self.newStudent_question.get_course_questions(str(course['_id']))
				course['questions'] = questions.count()
				data['courses'].append(course)

		return data


	def dashboard(self):

		data = self.dashboard_data()
		return render_template("instructor/dashboard.html", data=data)


	def courses(self):
		data = self.dashboard_data()

		data['view'] = 'courses'

		return render_template("instructor/dashboard.html", data=data)

	def new_course(self):
		data = self.dashboard_data()

		data['view'] = 'new'

		return render_template("instructor/dashboard.html", data=data)


