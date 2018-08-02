from flask import Flask, render_template, url_for, request, session, redirect, json, jsonify
from models.models import mongo, Student, Instructor, Interest, Student_interest, Course_interest, Course, Lesson, Student_subscription
import bcrypt
import locale
from bson import ObjectId
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import json

class StudentController():

	def  __init__(self):
		self.newStudent_interest = Student_interest()
		self.newCourse_interest = Course_interest()
		self.newInterest = Interest()
		self.newCourse = Course()
		self.newStudent_subscription = Student_subscription()

	def dashboard(self):
		data = {}
		data['loggedIn'] = False

		if 'student' in session:
			student_id = ObjectId(session['student']['id'])
			student_subscriptions = self.newStudent_subscription.get_student_subscriptions(student_id)
			student_interests = self.newStudent_interest.get_student_interests(session['student']['name'])
			data['selected_interests'] = []
			data['interest_courses'] = []
			data['subscribed'] = []
			if student_interests:
				for interest in student_interests:
					#print(interest)
					myInterest = self.newInterest.get_interest_by_id(interest['interest_id'])
					data['selected_interests'].append(myInterest['name'])
					interest_courses = self.newCourse_interest.get_interest_courses(interest['interest_id'])
					if interest_courses:
						for interest_course in interest_courses:
							course = self.newCourse.get_course_by_id(interest_course['course_id'])
							if course not in data['interest_courses']:
								course_subscription = self.newStudent_subscription.get_course_subscriptions(interest_course['course_id'])
								course['subscribed'] = course_subscription.count()
								data['interest_courses'].append(course)
					 
			if student_subscriptions:
				for subscribed in student_subscriptions:
					course = self.newCourse.get_course_by_id(subscribed['course_id'])
					course_subscription = self.newStudent_subscription.get_course_subscriptions(subscribed['course_id'])
					course['subscribed'] = course_subscription.count()
					data['subscribed'].append(course)

			data['loggedIn'] = True
			data['student'] = session['student']
			data['interests'] = self.newInterest.interests()

			return render_template("dashboard.html", data=data)
		else:
			return redirect(url_for('index'))


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