from flask import Flask, render_template, url_for, request, session, redirect, json, jsonify
from models.models import mongo, Student, Instructor, Interest, Student_interest, Course_interest, Course, Lesson, Student_subscription, Student_question, Question_response

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
		self.newQuestion_response = Question_response()


	def course_questions(self, title):
		data = {}
		data['questions'] = []
		course = self.newCourse.get_course_by_title(title)
		questions = self.newStudent_question.get_course_questions(str(course['_id']))
		if questions:
			for question in questions:
				question['student'] = self.newStudent.get_student_by_id(question['student_id'])
				question['lesson'] = self.newLesson.get_lesson_by_id(ObjectId(question['lesson_id']))
				question['responses'] = self.newQuestion_response.get_question_responses(str(question['_id']))
				data['questions'].append(question)

			data['course'] = course
			return render_template("instructor/course_questions.html", data=data)

		return redirect(url_for('instructor_dashboard'))


	def question(self, questionId):
		data = {}
		data['responses'] = []
		question_id = ObjectId(questionId)
		question = self.newStudent_question.get_question(question_id)
		lesson = self.newLesson.get_lesson_by_id(ObjectId(question['lesson_id']))
		course = self.newCourse.get_course_by_id(ObjectId(question['course_id']))
		responses = self.newQuestion_response.get_question_responses(questionId)
		if(responses.count() > 0):
			for response in responses:
				if(response['student_id'] == 0):
					instructor = self.newInstructor.get_instructor_by_id(ObjectId(response['instructor_id']))
					response['instructor'] = instructor
				if(response['instructor_id'] == 0):
					student = self.newStudent.get_student_by_id(ObjectId(response['student_id']))
					response['student'] = student
				data['responses'].append(response)

		data['question'] = question
		#data['responses'] = responses
		data['lesson'] = lesson
		data['course'] = course

		return render_template("instructor/question.html", data=data)
		session['error_msg'].clear()

	def respond(self):
		instructor_id = session['instructor']['id']
		
		question_id = request.form['question_id']
		response = request.form['response']
		result = self.newQuestion_response.instructor(question_id, instructor_id, response)
		if(result == 'ERROR'):
			return question_id+' '+instructor_id+' '+response+' OOPS! Problem occured while trying to submit your response, try again later'

		return redirect(url_for('student_question', questionId=question_id))
