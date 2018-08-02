from flask import Flask, render_template, url_for, request, session, redirect, json, jsonify
from models.models import mongo, Student, Instructor, Interest, Student_interest, Course_interest, Course, Lesson, Student_subscription, Student_question
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

		self.newInstructor = Instructor()
		self.newStudent_interest = Student_interest()
		self.newCourse_interest = Course_interest()
		self.newInterest = Interest()
		self.newCourse = Course()
		self.newStudent_subscription = Student_subscription()
		self.newStudent_question = Student_question()

	def dashboard(self):
		if self.loggedIn != True:
			return redirect(url_for('instructor_login'))

		data = {}
		data['logged_in'] = True 
		data['courses'] = []
		data['instructor'] = self.newInstructor.get_instructor_by_name(session['instructor']['name'])
		fields = {"instructor_id":data['instructor']['_id']}
		courses = self.newCourse.get_courses(fields)
		if courses:
			for course in courses:
				course_subscription = self.newStudent_subscription.get_course_subscriptions(course['_id'])
				course['subscribed'] = course_subscription.count()
				questions = self.newStudent_question.get_course_questions(str(course['_id']))
				course['questions'] = questions.count()
				data['courses'].append(course)

		return render_template("instructor/dashboard.html", data=data)


	def select_interests():
		data = {}
		data['loggedIn'] = False

		if 'student' in session:
			student_interests = self.newStudent_interest.get_student_interests(session['student']['name'])
			data['selected_interests'] = []
			if student_interests:
				for interest in student_interests:
					#print(interest)
					data['selected_interests'].append(interest['interest_id']) 

			data['loggedIn'] = True
			data['student'] = session['student']
			data['interests'] = self.newInterest.interests()

			return render_template("fields.html", data=data)
		else:
			return redirect(url_for('index'))


	def toggle_interests():
		if request.method == 'POST':
			newStudent_interest = Student_interest()
			interest = request.form['interest']
			student_name = session['student']['name']
			action = request.form['action']
			if action == 'add':
				data = newStudent_interest.add(student_name, interest)

			if action == 'remove':
				data = newStudent_interest.remove(student_name, interest)
			
			return json.dumps({'status':data});