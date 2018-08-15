from flask import Flask, render_template, url_for, request, session, redirect, json, jsonify
from models.models import mongo, Student, Instructor, Interest, Student_interest, Course_interest, Course, Lesson, Student_subscription
import bcrypt
import locale
from bson import ObjectId
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import json

class CartController():

	def  __init__(self):
		self.newStudent_interest = Student_interest()
		self.newCourse_interest = Course_interest()
		self.newInterest = Interest()
		self.newCourse = Course()
		self.newStudent_subscription = Student_subscription()
		self.newStudent = Student()
		self.newInstructor = Instructor()
		self.newLesson = Lesson()


	def update_cart(self):
		#session['cart'] = []
		data = {}
		data['loggedIn'] = False
		data['course_lessons'] = []
		course = {}	
		reverse_cart = []
		if 'cart' not in session:
			session['cart'] = []
		
		if 'reverse_cart' not in session:
			session['reverse_cart'] = []


		if 'student' in session:
			data['loggedIn'] = True
			data['student'] = session['student']

			if request.method == 'POST':
				newCourse = Course()
				course_id = request.form['course_id']
				selCourse = newCourse.get_course_by_id(ObjectId(course_id))
				course['title'] = selCourse['title']
				course['cost'] = selCourse['price']
				course['id'] = str(selCourse['_id'])
				if course not in session['cart']:
					session['cart'].append(course)
					session.modified = True

				#return jsonify(session)
				#return jsonify(session['cart'])
				if len(session['cart']) > 0:
					session['cart_total'] = 0
					session['reverse_cart'] = []
					for cart in session['cart']:
						reverse_cart.append(cart)
						session['cart_total'] = session['cart_total'] + cart['cost']

					rcount = len(reverse_cart)
					#return jsonify(reverse_cart)
					while(rcount > 0):
						session['reverse_cart'].append(reverse_cart.pop())
						session.modified = True
						rcount = rcount - 1

				return redirect(url_for('purchase_course', courseId=course['id']))
				#return redirect(url_for('dashboard'))
			else:
				return redirect(url_for('dashboard'))
		else:
			return redirect(url_for('index'))


	def remove_from_cart(self, title):
		data = {}
		data['loggedIn'] = False
		if 'student' in session:
			data['loggedIn'] = True
			data['student'] = session['student']

			n = 0 
			for cart in session['cart']:
				if cart['title'] == title:
					session['cart'].pop(n)
					session['cart_total'] = session['cart_total'] - cart['cost']
					session.modified = True
				n = n + 1

			n = 0
			for rcart in session['reverse_cart']:
				if rcart['title'] == title:
					session['reverse_cart'].pop(n)
					session.modified = True
				n = n + 1

			return redirect(request.referrer)
		else:
			return redirect(url_for('index'))


	def view_cart(self):
		data = {}
		data['loggedIn'] = False

		if 'cart' in session:
			data['cart'] = session['cart']
		else:
			data['cart'] = []

		if 'reverse_cart' in session:
			data['reverse_cart'] = session['reverse_cart']

		if 'cart_total' in session:
			data['sub_total'] = session['cart_total']
		else:
			data['sub_total'] = 0

		if 'student' in session:
			data['loggedIn'] = True
			data['student'] = session['student']
			return render_template("cart.html", data=data)
		else:
			return redirect(url_for('index'))


	def checkout(self):
		data = {}
		data['loggedIn'] = False

		if 'cart' in session:
			data['cart'] = session['cart']
		else:
			data['cart'] = []

		if 'reverse_cart' in session:
			data['reverse_cart'] = session['reverse_cart']

		if 'cart_total' in session:
			data['sub_total'] = session['cart_total']
		else:
			data['sub_total'] = 0

		if 'student' in session:
			data['loggedIn'] = True
			data['student'] = session['student']
			return render_template("checkout.html", data=data)
		else:
			return redirect(url_for('index'))
