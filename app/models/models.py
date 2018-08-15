from flask_pymongo import PyMongo
import bcrypt
import datetime as date
from bson import ObjectId

mongo = PyMongo()

class Student():

    def set_password(self, password):
	    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
	    return check_password_hash(type(self).password, password)

    def add(self, name, email, password, phone):
        students = mongo.db.students
        hashpass = self.set_password(password)
        name = name.title()
        email = email.lower()
        students.insert({'name' : name, 'password' : hashpass, 'email' : email, 'phone' : phone})

    def get_student_by_name(self, name):
        return mongo.db.students.find_one({"name": name})

    def get_student_by_id(self, id):
        return mongo.db.students.find_one({"_id": id})

class Instructor():
    
    def instructors(self):
        return mongo.db.interests.find()

    def get_instructor_by_name(self, name):
        return mongo.db.instructors.find_one({"name": name})

    def get_instructor_by_id(self, id):
        return mongo.db.instructors.find_one({"_id": id})


class Interest():

    def interests(self):
        return mongo.db.interests.find()

    def get_interest_by_name(self, name):
        return mongo.db.interests.find_one({"name": name})

    def get_interest_by_id(self, id):
        return mongo.db.interests.find_one({"_id": id})

class Course():

    def courses(self):
        return mongo.db.courses.find()

    def get_courses(self, field):
        fields = {}
        for key, val in field.items():
            fields[key] = val

        return mongo.db.courses.find(fields)

    def get_course_by_title(self, title):
        return mongo.db.courses.find_one({"title": title})

    def get_course_by_id(self, ids):
        return mongo.db.courses.find_one({"_id": ids})

    def add(self, title, cover_photo, description, instructor_id):
        courses = mongo.db.courses
        #course_id = mongo.db.courses.find_one({"_id":course_id})
        try:
            result = courses.insert({"title": title, "cover_photo": cover_photo, "description": description, "instructor_id": instructor_id, "price": None, "approved": 0})
            return 'OK'
        except Exception, e:
            return e

    def update(self, course_id, title, cover_photo, description):
        #course_id = mongo.db.courses.find_one({"_id":course_id})
        if(cover_photo==''):
            fieldset = {"title": title, "description": description}
        else:
            fieldset = {"title": title, "cover_photo": cover_photo, "description": description}

        try:
            result = mongo.db.courses.update({"_id": course_id}, {"$set": fieldset})
            return 'OK'
        except Exception, e:
            return e

class Lesson():

    def lessons(self):
        return mongo.db.lessons.find()

    def get_lesson(self, field):
        fields = {}
        for key, val in field.items():
            fields[key] = val

        return mongo.db.lessons.find_one(fields)

    def get_lesson_by_title(self, title):
        return mongo.db.lessons.find_one({"title": title})

    def get_lesson_by_id(self, ids):
        return mongo.db.lessons.find_one({"_id": ids})

    def get_lesson_by_courseId(self, ids):
        return mongo.db.lessons.find({"course_id": ids})

    def get_free_lessons(self, course_id):
        free_lessons_id = []
        course_lessons = self.get_lesson_by_courseId(course_id)
        n = 0
        if course_lessons:
            for lesson in course_lessons:
                if n < 3:
                    free_lessons_id.append(lesson['_id'])
                    n = n + 1
                    
        return free_lessons_id

    def add(self, title, url, description, duration, course_id):
        lessons = mongo.db.lessons
        #course_id = mongo.db.courses.find_one({"_id":course_id})
        try:
            result = lessons.insert({"title": title, "video_url": url, "description": description, "duration": duration, "course_id": course_id})
            return 'OK'
        except:
            return 'ERROR'

    def update(self, lesson_id, title, url, description, duration):
        #course_id = mongo.db.courses.find_one({"_id":course_id})
        try:
            result = mongo.db.lessons.update({"_id": lesson_id}, {"$set": {"title": title, "video_url": url, "description": description, "duration": duration}})
            return 'OK'
        except Exception, e:
            return e


class Student_interest():

    def add(self, student_name, interest):
        student_interests = mongo.db.student_interests
        student_id = mongo.db.students.find({"name":student_name})[0]['_id']
        interest_id = mongo.db.interests.find({"name":interest})[0]['_id']
        try:
            result = student_interests.insert({"student_id": student_id, "interest_id": interest_id})
            return 'OK'
        except:
            return 'ERROR'

    def remove(self, student_name, interest):
        student_interests = mongo.db.student_interests
        student_id = mongo.db.students.find({"name":student_name})[0]['_id']
        interest_id = mongo.db.interests.find({"name":interest})[0]['_id']
        try:
            result = student_interests.remove({"student_id": student_id, "interest_id": interest_id})
            return 'OK'
        except:
            return 'ERROR'

    def get_student_interests(self, student_name):
        student_interests = mongo.db.student_interests
        student_id = mongo.db.students.find({"name":student_name})[0]['_id']
        return mongo.db.student_interests.find({"student_id": student_id})


class Course_interest():

    def add(self, course_title, interest):
        course_interests = mongo.db.course_interests
        course_id = mongo.db.courses.find({"title":course_title})[0]['_id']
        interest_id = mongo.db.interests.find({"name":interest})[0]['_id']
        try:
            result = course_interests.insert({"course_id": course_id, "interest_id": interest_id})
            return 'OK'
        except:
            return 'ERROR'

    def get_course_interests(self, course_title):
        course_interests = mongo.db.course_interests
        course_id = mongo.db.courses.find({"title":course_title})[0]['_id']
        return mongo.db.course_interests.find({"course_id": course_id})

    def get_interest_courses(self, interest_id):
        course_interests = mongo.db.course_interests
        #interest = mongo.db.interests.find_one({"name":interest})
        #interest_id = interest['_id']
        return mongo.db.course_interests.find({"interest_id": interest_id})

    def get_similar_courses(self, course_id):
        newCourse = Course()
        course_title = mongo.db.courses.find({"_id":course_id})[0]['title']
        # get the interests associated to that course
        interests = self.get_course_interests(course_title)
        similarInterests = []
        similarCourses = []
        if interests.count() > 0:
            for interest in interests:
                #interestCourse = newCourse.get_course_by_title(interest['title'])
                interestCourse = self.get_interest_courses(interest['interest_id'])
                similarInterests.append(interestCourse)

            for similarInterest in similarInterests:
                for similarInt in similarInterest:
                    similarCourse = mongo.db.courses.find_one({"_id":similarInt['course_id']})
                    if ((similarInt['course_id'] != course_id) and (similarCourse not in similarCourses)):
                        similarCourses.append(similarCourse)

        return similarCourses



class Student_subscription():

    def add(self, student_id, course_id):
        student_subscriptions = mongo.db.student_subscriptions
        try:
            result = student_subscriptions.insert({"student_id": student_id, "course_id": course_id})
            return 'OK'
        except:
            return 'ERROR'

    def remove(self, student_id, course_id):
        try:
            result = student_subscriptions.remove({"student_id": student_id, "course_id": course_id})
            return 'OK'
        except:
            return 'ERROR'

    def get_student_subscriptions(self, student_id):
        return mongo.db.student_subscriptions.find({"student_id": student_id})

    def get_course_subscriptions(self, course_id):
        return mongo.db.student_subscriptions.find({"course_id": course_id})

    def get_student_course_subscriptions(self, student_id, course_id):
        return mongo.db.student_subscriptions.find_one({"student_id": student_id, "course_id": course_id})


class Student_question():

    def __init__(self):
        self.student_questions = mongo.db.Student_questions


    def add(self, lesson_id, course_id, student_id, question):
        try:
            answered = 0
            date_asked = date.datetime.now()
            result = self.student_questions.insert({"lesson_id": lesson_id, "course_id": course_id, "student_id": student_id, "question":question, "answered":answered, "date_asked":date_asked})
            return 'OK'
        except:
            return 'ERROR'

    def get_lesson_questions(self, lesson_id):
        return mongo.db.Student_questions.find({"lesson_id": lesson_id}).sort([("date_asked", -1)])

    def get_course_questions(self, course_id):
        return mongo.db.Student_questions.find({"course_id": course_id})

    def get_question(self, question_id):
        return mongo.db.Student_questions.find_one({"_id": question_id})

class Question_response():

    def __init__(self):
        self.question_responses = mongo.db.question_responses


    def instructor(self, question_id, instructor_id, response):
        try:
            responded = date.datetime.now()
            student_id = 0
            result = self.question_responses.insert({"question_id": question_id, "instructor_id": instructor_id, "student_id": student_id, "response": response, "date":responded})
            return 'OK'
        except:
            return 'ERROR'

    def student(self, question_id, student_id, response):
        try:
            responded = date.datetime.now()
            instructor_id = 0
            result = self.question_responses.insert({"question_id": question_id, "instructor_id": instructor_id, "student_id": student_id, "response": response, "date":responded})
            return 'OK'
        except:
            return 'ERROR'

    def get_question_responses(self, question_id):
        return mongo.db.question_responses.find({"question_id": question_id})


