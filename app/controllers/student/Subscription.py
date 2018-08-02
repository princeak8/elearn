from flask import Flask, render_template, url_for, request, session, redirect, json, jsonify
from models.models import mongo, Student, Instructor, Interest, Student_interest, Course_interest, Course, Lesson, Student_subscription
import bcrypt
import locale
from bson import ObjectId
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import json

class SubscriptionController():

	def  __init__(self):
		if 'student' not in session:
			return redirect(url_for('index'))
			
		self.newStudent_interest = Student_interest()
		self.newCourse_interest = Course_interest()
		self.newInterest = Interest()
		self.newCourse = Course()
		self.newStudent_subscription = Student_subscription()
		self.newStudent = Student()
		self.newInstructor = Instructor()
		self.newLesson = Lesson()


	def subscribe():
		student_id = ObjectId(session['student']['id'])

		if(('cart' in session) and (len(session['cart']) > 0)):
			for item in session['cart']:
				course_id = ObjectId(item['id'])
				result = self.newStudent_subscription.add(student_id, course_id)
				if result == 'OK':
					session['success'] = 1
					session['cart'] = [];
					return redirect(url_for('subscription_result'))
				else:
					session['success'] = 0
					session['checkout_msg'] = 'OOPS! Problem occured while trying to process your subscription, try again later'
					#return jsonify(student_id)
					return redirect(url_for('checkout'))

		else:
			return redirect(url_for('dashboard'))

			