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

class QuestionController():

	def  __init__(self):
		if 'instructor' in session:
			self.loggedIn = True

		self.newStudent_interest = Student_interest()
		self.newCourse_interest = Course_interest()
		self.newInterest = Interest()
		self.newCourse = Course()
		self.newStudent_subscription = Student_subscription()
		self.newStudent = Student()
		self.newInstructor = Instructor()
		self.newLesson = Lesson()
		self.newStudent_question = Student_question()


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


	def question(self, questionId):
		data = {}
		question_id = ObjectId(questionId)
		question = self.newStudent_question.get_question(question_id)
		lesson = self.newLesson.get_lesson_by_id(ObjectId(question['lesson_id']))
		course = self.newCourse.get_course_by_id(ObjectId(question['course_id']))

		data['question'] = question
		data['lesson'] = lesson
		data['course'] = course

		return render_template("instructor/question.html", data=data)