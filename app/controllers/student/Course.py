from flask import Flask, render_template, url_for, request, session, redirect, json, jsonify
from models.models import mongo, Student, Instructor, Interest, Student_interest, Course_interest, Course, Lesson, Student_subscription, Student_question

#from models.Student import Student
#from models.Instructor import Instructor
#from models.Interest import Interest
#from models.Student_interest import Student_interest
#from models.Course_interest import Course_interest
#from models.Course import Course
#from models.Lesson import Lesson
#from models.Student_subscription import Student_subscription
#from models.Student_question import Student_question

from forms import QuestionForm
import bcrypt
import locale
from bson import ObjectId
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import json

class CourseController():

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
		self.newStudent_question = Student_question()

	def single_course(self, title):
		data = {}
		data['loggedIn'] = False
		data['course_lessons'] = []
		data['similar_courses'] = []

		data['loggedIn'] = True
		data['student'] = session['student']

		course = self.newCourse.get_course_by_title(title)
		if course:
			student_id = ObjectId(session['student']['id'])
			similar_courses = self.newCourse_interest.get_similar_courses(course['_id'])
			instructor = self.newInstructor.get_instructor_by_id(course['instructor_id'])
			courseLessons = self.newLesson.get_lesson_by_courseId(course['_id'])
			courseDuration = 0
			for lesson in courseLessons:
				courseDuration = int(courseDuration) + int(lesson['duration'])
				data['course_lessons'].append(lesson)

			subscribed = self.newStudent_subscription.get_student_course_subscriptions(student_id, course['_id'])
			if subscribed:
				data['subscribed'] = 1
			else:
				data['subscribed'] = 0

			thisCourse = '';
				

			data['course'] = course
			data['instructor'] = instructor
			data['course_duration'] = courseDuration
			data['similar_courses'] = similar_courses
			#return jsonify(len(similar_courses))

			return render_template("course_single.html", data=data)
		else:
			return redirect(url_for('dashboard'))


	def course_lesson(self, course_title, lesson_title):
		data = {}
		data['QForm'] = QuestionForm()
		data['loggedIn'] = False
		data['loggedIn'] = True
		data['student'] = session['student']
		data['course_lessons'] = []
		data['lesson_questions'] = []

		student_id = ObjectId(session['student']['id'])
		course = self.newCourse.get_course_by_title(course_title)
		fields = {"course_id":course['_id'], "title":lesson_title}
		lesson = self.newLesson.get_lesson(fields)
		subscribed = self.newStudent_subscription.get_student_course_subscriptions(student_id, lesson['course_id'])
		free_lessons = self.newLesson.get_free_lessons(lesson['course_id'])
		if ((subscribed) or (lesson['_id'] in free_lessons)):
			#course = self.newCourse.get_course_by_id(lesson['course_id'])
			similar_courses = self.newCourse_interest.get_similar_courses(course['_id'])
			instructor = self.newInstructor.get_instructor_by_id(course['instructor_id'])
			courseLessons = self.newLesson.get_lesson_by_courseId(course['_id'])
			lesson_questions = self.newStudent_question.get_lesson_questions(str(lesson['_id']))
			if lesson_questions.count() > 0:
				for quest in lesson_questions:
					question = {}
					question['student'] = self.newStudent.get_student_by_id(quest['student_id'])['name']
					question['date_asked'] = str(quest['date_asked'])
					question['quest'] = quest 
					data['lesson_questions'].append(question)

			courseDuration = 0
			n = 0
			nxt = 0
			prev = ''
			for courseLesson in courseLessons:
				n = n + 1;
				if nxt == 1:
					lesson['nxt'] = courseLesson['title']
					nxt = 0
				if courseLesson['title'] == lesson['title']:
					lesson['prev'] = prev
					nxt = 1

				prev = courseLesson['title']
				courseDuration = int(courseDuration) + int(courseLesson['duration'])
				data['course_lessons'].append(courseLesson)
			

			data['course'] = course
			data['lesson'] = lesson
			data['instructor'] = instructor
			data['course_duration'] = courseDuration
			data['similar_courses'] = similar_courses

			#return jsonify(len(similar_courses))
			return render_template("course_lesson.html", data=data)
		else:
			return redirect(url_for('dashboard'))


	def purchase_course(self, title):
		#session['test'] = 'this'
		data = {}
		data['loggedIn'] = False
		data['course_lessons'] = []
		#session['reverse_cart'] = []
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


		data['loggedIn'] = True
		data['student'] = session['student']

		course = self.newCourse.get_course_by_title(title)
			#return jsonify(title)
		instructor = self.newInstructor.get_instructor_by_id(course['instructor_id'])
		courseLessons = self.newLesson.get_lesson_by_courseId(course['_id'])
		courseDuration = 0
		for lesson in courseLessons:
			courseDuration = int(courseDuration) + int(lesson['duration'])
			data['course_lessons'].append(lesson)

		#cart = session['cart']
		#count = len(cart)
		#while count > 0:
		#	session['reverse_cart'].append(cart.pop())
		#	session.modified = True
		#	count = count - 1

		data['course'] = course
		data['instructor'] = instructor
		data['course_duration'] = courseDuration


		return render_template("purchase_course.html", data=data)
	

	def ask_question(self):
		form = QuestionForm()
		student_id = ObjectId(session['student']['id'])
		if form.validate() == False:
			errors = ''
			if form.question.errors:
				for error in form.question.errors:
					errors += ' '+error
			
			return json.dumps({'status':'ERROR','message':errors});
		else:
			question = request.form['question']
			lesson_id = request.form['lesson_id']
			course_id = request.form['course_id']
			result = self.newStudent_question.add(lesson_id, course_id, student_id, question)
			if(result == 'OK'):
				return json.dumps({'status':'OK'});

			if(result == 'ERROR'):
				return json.dumps({'status':'ERROR'});


	def course_questions(self):
		return render_template("course_questions.html")