import os
from flask import Flask, render_template, url_for, flash, request, session, redirect, json, jsonify
from models.models import mongo, Student, Instructor, Interest, Student_interest, Course_interest, Course, Lesson, Student_subscription, Student_question, Question_response
from werkzeug.utils import secure_filename
#from models.Student import Student
#from models.Instructor import Instructor
#from models.Interest import Interest
#from models.Student_interest import Student_interest
#from models.Course_interest import Course_interest
#from models.Course import Course
#from models.Lesson import Lesson
#from models.Student_subscription import Student_subscription
#from models.Student_question import Student_question

from forms import CourseForm, EditCourseForm, LessonForm, QuestionForm
import bcrypt
import locale
from bson import ObjectId
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import json

class CourseController():

	def  __init__(self):
		if 'instructor' in session:
			self.loggedIn = True
		else:
			return redirect(url_for('instructor_login'))

		self.newStudent_interest = Student_interest()
		self.newCourse_interest = Course_interest()
		self.newInterest = Interest()
		self.newCourse = Course()
		self.newStudent_subscription = Student_subscription()
		self.newStudent = Student()
		self.newInstructor = Instructor()
		self.newLesson = Lesson()
		self.newStudent_question = Student_question()
		self.newQuestion_response = Question_response()
		self.uploadFolder = 'static/images/courses_cover_photos'
		self.allowedExtensions = set(['png', 'jpg', 'jpeg', 'gif', 'psd'])

	def course_data(self, course_id):
		data = {}
		data['course_lessons'] = []
		data['similar_courses'] = []
		data['loggedIn'] = True
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

		course = self.newCourse.get_course_by_id(ObjectId(course_id))
		data['course'] = course
		if course:
			similar_courses = self.newCourse_interest.get_similar_courses(course['_id'])
			instructor = self.newInstructor.get_instructor_by_id(course['instructor_id'])
			courseLessons = self.newLesson.get_lesson_by_courseId(course['_id'])
			courseDuration = 0
			for lesson in courseLessons:
				courseDuration = int(courseDuration) + int(lesson['duration'])
				data['course_lessons'].append(lesson)

			thisCourse = '';
				

			data['instructor'] = instructor
			data['course_duration'] = courseDuration
			data['similar_courses'] = similar_courses

		return data
		

	def course(self, course_id):
		if self.loggedIn != True:
			return redirect(url_for('instructor_login'))

		data = self.course_data(course_id)
		data['new_course_form'] = CourseForm()
		data['new_course_form'].instructor_id.data = data['instructor']['_id']
		data['new_lesson_form'] = LessonForm()
		data['new_lesson_form'].course_id.data = course_id

			#return jsonify(len(similar_courses))
		if data['course']:
			return render_template("instructor/course.html", data=data)
		else:
			return redirect(url_for('index'))

	def create(self):
		form = CourseForm()

		if request.method == 'POST':
			instructor_id = form.instructor_id.data
			instructor_id = ObjectId(instructor_id)
			if form.validate() == False:
				return redirect(url_for('new_course'))
			else:
				if 'cover_photo' not in request.files:
					flash('No Cover Photo')
					return redirect(url_for('new_course'))
				photo = request.files['cover_photo']
				if photo.filename == '':
					flash('No Photo Selected')
					return redirect(url_for('new_course'))
				if photo and self.allowed_file(photo.filename):
					filename = secure_filename(photo.filename)
					photo.save(os.path.join(self.uploadFolder, filename))
				id = self.newCourse.add(form.title.data, filename, form.description.data, instructor_id)
				return redirect(url_for('instructor_courses'))

		return redirect(url_for('instructor_dashboard'))

	def edit(self, course_id):
		form = EditCourseForm()
		data = {}

		course = self.newCourse.get_course_by_id(ObjectId(course_id))
		data['edit_course_form'] = form
		data['edit_course_form'].course_id.data = course_id
		data['edit_course_form'].title.data = course['title']
		data['edit_course_form'].cover_photo.data = course['cover_photo']
		data['edit_course_form'].description.data = course['description']
		data['course'] = course

		data['instructor'] = self.newInstructor.get_instructor_by_name(session['instructor']['name'])

		return render_template('instructor/edit_course.html', data=data)

	def update(self):
		form = EditCourseForm()
		data = {}

		if request.method == 'POST':
			courseid = form.course_id.data
			course_id = ObjectId(courseid)
			course = self.newCourse.get_course_by_id(course_id)
			if form.validate() == True:
				if 'cover_photo' not in request.files:
					flash('No Cover Photo')
					return redirect(url_for('instructor_edit_course', courseId=course_id))
				photo = request.files['cover_photo']
				if photo.filename == '':
					filename = ''
				if photo and self.allowed_file(photo.filename):
					filename = secure_filename(photo.filename)
					#Add new photo
					photo.save(os.path.join(self.uploadFolder, filename))
					#Remove old photo
					if os.path.isfile(self.uploadFolder+course['cover_photo']):
						os.remove(os.path.join(self.uploadFolder, course['cover_photo']))
				result = self.newCourse.update(course_id, form.title.data, filename, form.description.data)
				if result == 'OK':
					flash('1')
				else:
					flash('0')

				#return jsonify(str(result))
				return redirect(url_for('instructor_edit_course', courseId=course_id))
			else:
				return redirect(url_for('instructor_edit_course', courseId=course_id))

		return redirect(url_for('instructor_dashboard'))


	def lesson(self, lesson_id):
		data = {}
		data['QForm'] = QuestionForm()
		data['course_lessons'] = []
		data['lesson_questions'] = []

		lesson = self.newLesson.get_lesson_by_id(ObjectId(lesson_id))
		course = self.newCourse.get_course_by_id(lesson['course_id'])

		if (lesson):
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
					question['responses'] = self.newQuestion_response.get_question_responses(str(quest['_id']))
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
			return render_template("instructor/lesson.html", data=data)
		else:
			return redirect(url_for('instructor_dashboard'))


	def new_lesson(self):
		form = LessonForm()

		if request.method == 'POST':
			course_id = form.course_id.data
			course_id = ObjectId(course_id)
			if form.validate() == False:
				data = self.course_data(course_id)
				data['new_lesson_form'] = form
				data['new'] = 1
				return render_template('instructor/course.html', data=data)
			else:
				#return jsonify(course_id)
				#course_id = '5a5e2612a8af96b319f84dce'
				#data = self.course_data(str(course_id))
				#duration = request.form['duration']
				id = self.newLesson.add(form.title.data, form.video_url.data, form.description.data, form.duration.data, course_id)
				return redirect(url_for('instructor_course', courseId=course_id))

		return redirect(url_for('instructor_dashboard'))

	def edit_lesson(self, lesson_id):
		form = LessonForm()
		data = {}

		lesson = self.newLesson.get_lesson_by_id(ObjectId(lesson_id))
		course = self.newCourse.get_course_by_id(lesson['course_id'])
		data['edit_lesson_form'] = form
		data['edit_lesson_form'].lesson_id.data = lesson_id
		data['edit_lesson_form'].title.data = lesson['title']
		data['edit_lesson_form'].video_url.data = lesson['video_url']
		data['edit_lesson_form'].description.data = lesson['description']
		data['edit_lesson_form'].duration.data = lesson['duration']
		data['lesson'] = lesson
		data['course'] = course

		data['instructor'] = self.newInstructor.get_instructor_by_name(session['instructor']['name'])

		return render_template('instructor/edit_lesson.html', data=data)

	def update_lesson(self):
		form = LessonForm()
		data = {}

		if request.method == 'POST':
			lesson_id = form.lesson_id.data
			lesson_id = ObjectId(lesson_id)
			lesson = self.newLesson.get_lesson_by_id(lesson_id)
			if form.validate() == True:
				result = self.newLesson.update(lesson_id, form.title.data, form.video_url.data, form.description.data, form.duration.data)
				if result == 'OK':
					flash('1')
				else:
					flash('0')

				#return jsonify(str(result))
				return redirect(url_for('instructor_edit_lesson', lessonId=lesson_id))
			else:
				return redirect(url_for('instructor_edit_lesson', lessonId=lesson_id))

		return redirect(url_for('instructor_dashboard'))


	def course_questions(self, title):
		data = {}
		data['questions'] = []
		course = self.newCourse.get_course_by_title(title)
		questions = self.newStudent_question.get_course_questions(str(course['_id']))
		if questions:
			for question in questions:
				question['student'] = self.newStudent.get_student_by_id(question['student_id'])
				question['lesson'] = self.newLesson.get_lesson_by_id(ObjectId(question['lesson_id']))
				data['questions'].append(question)

			data['course'] = course
			return render_template("instructor/course_questions.html", data=data)

		return redirect(url_for('instructor_dashboard'))


	def allowed_file(self, filename):
		return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in self.allowedExtensions
