from flask import Flask, render_template, url_for, request, session, redirect, json, jsonify
from models.models import mongo, Student, Instructor, Interest, Student_interest, Course_interest, Course, Lesson, Student_subscription
from controllers.student.Student import StudentController
from controllers.instructor.Instructor import InstructorController
from controllers.instructor.Course import CourseController as InstructorCourse
from controllers.instructor.Question import QuestionController
from controllers.student.Login import LoginController
from controllers.student.Registeration import RegisterationController
from controllers.student.Course import CourseController
from controllers.student.Subscription import SubscriptionController
from controllers.student.Cart import CartController
from controllers.student.Question import QuestionController as QController
from forms import SignupForm, LoginForm
import bcrypt
import locale
from bson import ObjectId
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'elearn'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/elearn'
mongo.init_app(app)


@app.route("/")
@app.route("/index")
def index():
	form = LoginForm()
	data = {}
	data['loggedIn'] = False
	data['form'] = form
	#data['password'] = bcrypt.hashpw('rita123'.encode('utf-8'), bcrypt.gensalt())

	if 'student' in session:
		data['loggedIn'] = True
		data['student'] = session['student']
		newStudent_interest = Student_interest()
		newStudent_subscription = Student_subscription()
		student_interests = newStudent_interest.get_student_interests(session['student']['name'])
		if student_interests.count() > 0:
			return redirect(url_for('dashboard'))
		else:
			return redirect(url_for('select_interests'))

	return render_template("index.html", data=data)

@app.route('/student/login', methods=['POST', 'GET'])
def student_login():
	login = LoginController()
	return login.student_login()

@app.route('/signout', methods=['GET'])
def signout():
	session.clear()
	return redirect(url_for('index'))

@app.route('/student/signup', methods=['POST', 'GET'])
def student_signup():
	register = RegisterationController()
	return register.signup()

@app.route("/select_interests")
def select_interests():
	student = StudentController()
	return student.select_interests()

@app.route("/student/dashboard")
def dashboard():
	student = StudentController()
	return student.dashboard()

@app.route("/toggle_interest", methods=['POST'])
def toggle_interests():
	student = StudentController()
	return student.toggle_interests()

@app.route("/single_course/<courseId>", methods=['GET'])
def single_course(courseId):
	course = CourseController()
	return course.single_course(courseId)

@app.route("/course_lesson/<course_title>/<lesson_title>", methods=['GET'])
def course_lesson(course_title, lesson_title):
	course = CourseController()
	#lesson = course.course_lesson(title)
	return course.course_lesson(course_title, lesson_title)

@app.route("/purchase_course/<courseId>", methods=['GET'])
def purchase_course(courseId):
	course = CourseController()
	return course.purchase_course(courseId)

@app.route('/update_cart', methods=['POST', 'GET'])
def update_cart():
	cart = CartController()
	return cart.update_cart()

@app.route('/remove_from_cart/<title>', methods=['POST', 'GET'])
def remove_from_cart(title):
	cart = CartController()
	return cart.remove_from_cart(title)

@app.route('/view_cart')
def view_cart():
	cart = CartController()
	return cart.view_cart()


@app.route('/checkout')
def checkout():
	cart = CartController()
	return cart.checkout()

@app.route('/subscribe', methods=['POST'])
def subscribe():
	subscription = SubscriptionController()
	return subscription.subscribe()

@app.route('/subscription_result')
def subscription_result():
	return render_template("subscription_result.html")

@app.route('/student/ask_question', methods=['POST'])
def ask_question():
	course = CourseController()
	return course.ask_question()

@app.route('/student/question/<questionId>')
def question(questionId):
	question = QController()
	return question.question(questionId)

@app.route('/instructor/login', methods=['POST', 'GET'])
def instructor_login():
	login = LoginController()
	return login.instructor_login()

@app.route('/instructor/signout', methods=['GET'])
def instructor_signout():
	session.clear()
	return redirect(url_for('instructor_login'))

@app.route('/instructor/')
@app.route('/instructor/index')
@app.route('/instructor/dashboard')
def instructor_dashboard():
	instructor = InstructorController()
	return instructor.dashboard()

@app.route('/instructor/courses')
def instructor_courses():
	instructor = InstructorController()
	return instructor.courses()

@app.route('/instructor/new_course')
def new_course():
	instructor = InstructorController()
	return instructor.new_course()

@app.route('/instructor/create_course', methods=['POST'])
def create_course():
	course = InstructorCourse()
	return course.create()

@app.route('/instructor/course/<courseId>')
def instructor_course(courseId):
	course = InstructorCourse()
	return course.course(courseId)

@app.route('/instructor/edit_course/<courseId>')
def instructor_edit_course(courseId):
	course = InstructorCourse()
	return course.edit(courseId)

@app.route('/instructor/update_course', methods=['POST'])
def update_course():
	course = InstructorCourse()
	return course.update()

@app.route('/instructor/new_lesson', methods=['POST'])
def new_lesson():
	course = InstructorCourse()
	return course.new_lesson()

@app.route('/instructor/lesson/<lessonId>')
def instructor_lesson(lessonId):
	course = InstructorCourse()
	return course.lesson(lessonId)

@app.route('/instructor/edit_lesson/<lessonId>')
def instructor_edit_lesson(lessonId):
	course = InstructorCourse()
	return course.edit_lesson(lessonId)

@app.route('/instructor/update_lesson', methods=['POST'])
def update_lesson():
	course = InstructorCourse()
	return course.update_lesson()

@app.route('/instructor/course_questions/<title>')
def instructor_course_questions(title):
	question = QuestionController()
	return question.course_questions(title)

@app.route('/instructor/student_question/<questionId>')
def student_question(questionId):
	question = QuestionController()
	return question.question(questionId)

@app.route('/instructor/question_response', methods=['POST'])
def question_instructor_response():
	question = QuestionController()
	return question.respond()

@app.route('/student/question_response', methods=['POST'])
def question_student_response():
	question = QController()
	return question.respond()

def set_session_val():
	session['mylist'] = {}
	session['cart'] = {}
	session['cart']['key'] = 'val'
	session['mylist']['key'] = 'val'
	session.modified = True


if __name__ == "__main__":
	app.secret_key = 'mysecret'
	app.run(debug=True)