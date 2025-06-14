from flask import Flask, render_template, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json
# Initialize Flask application
app = Flask(__name__,static_url_path='/static',template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///universityDB.db'  # Replace with your database URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    enroll_date = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Student {self.fname} {self.lname}>'
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    faculty_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Class {self.name}>'
class faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Faculty {self.fname} {self.lname}>'
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    head = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f'<Department {self.name}>'
class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, nullable=False),
    semester = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Course {self.name}>'
class Enrollments(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, primary_key=False)
    class_id = db.Column(db.Integer, primary_key=False)
    def __repr__(self):
        return f'<Enrollments {self.student_id} {self.class_id}>'
class Grade(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), primary_key=True)
    grade = db.Column(db.String(100), nullable=False)
    grade_date = db.Column(db.String(100), primary_key=False)
    def __repr__(self):
        return f'<Grades {self.student_id} {self.class_id}>'
class Authentication(db.Model):
    email = db.Column(db.String(100), nullable=False,primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Authentication {self.email}>'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addstudent',methods=['POST'])
def add_student():
    # Sample student data
    data=request.get_json()
    student_id = data.get('id')
    fname = data.get('fname')
    lname = data.get('lname')
    dob = data.get('dob')
    email = data.get('email')
    phone = data.get('phone')
    enroll_date = data.get('enroll_date')
    class_id = data.get('class_id')

    # Create a new student instance
    new_student = Student(
        id=student_id,
        fname=fname,
        lname=lname,
        dob=dob,
        email=email,
        phone=phone,
        enroll_date=enroll_date,
        class_id=class_id
    )
    print(new_student)

    # Add the student to the session and commit
    db.session.add(new_student)
    db.session.commit()

    return "Student added successfully!"
@app.route('/addstudent1',methods=['POST'])
def test():
    data=request.get_json()
    print(data)
    return "Student added successfully!"
@app.route('/addclass', methods=['POST'])
def add_class():
    data = request.get_json()
    class_id = data.get('class_id')
    name = data.get('name')
    course_id = data.get('course_id')
    faculty_id = data.get('faculty_id')

    new_class = Class(
        id=class_id,
        name=name,
        course_id=course_id,
        faculty_id=faculty_id
    )

    db.session.add(new_class)
    db.session.commit()

    return "Class added successfully!"

@app.route('/addfaculty', methods=['POST'])
def add_faculty():
    data = request.get_json()
    faculty_id = data.get('faculty_id')
    fname = data.get('fname')
    lname = data.get('lname')
    email = data.get('email')
    phone = data.get('phone')
    department_id = data.get('department_id')

    new_faculty = faculty(
        id=faculty_id,
        fname=fname,
        lname=lname,
        email=email,
        phone=phone,
        department_id=department_id
    )

    db.session.add(new_faculty)
    db.session.commit()
    return "Faculty added successfully!"

@app.route('/adddepartment', methods=['POST'])
def add_department():
    data = request.get_json()
    department_id = data.get('department_id')
    name = data.get('name')
    head = data.get('head')

    new_department = Department(
        id=department_id,
        name=name,
        head=head
    )
    db.session.add(new_department)
    db.session.commit()
    return "Department added successfully!"

@app.route('/addcourse', methods=['POST'])
def add_course():
    data = request.get_json()
    course_id = data.get('course_id')
    course_name = data.get('course_name')
    department_id = data.get('department_id')
    credits = data.get('credits')
    semester = data.get('semester')

    new_course = Courses(
        course_id=course_id,
        course_name=course_name,
        department_id=department_id,
        credits=credits,
        semester=semester
    )
    db.session.add(new_course)
    db.session.commit()
    return "Course added successfully!"

@app.route('/addenrollment', methods=['POST'])
def add_enrollment():
    data = request.get_json()
    enrollment_id = data.get('enrollment_id')
    student_id = data.get('student_id')
    class_id = data.get('class_id')

    new_enrollment = Enrollments(
        enrollment_id=enrollment_id,
        student_id=student_id,
        class_id=class_id
    )
    db.session.add(new_enrollment)
    db.session.commit()
    return "Enrollment added successfully!"

@app.route('/addgrade', methods=['POST'])
def add_grade():
    data = request.get_json()
    enrollment_id = data.get('enrollment_id')
    subject = data.get('subject')
    grade = data.get('grade')
    grade_date = data.get('grade_date')

    new_grade = Grade(
        enrollment_id=enrollment_id,
        subject=subject,
        grade=grade,
        grade_date=grade_date
    )
    db.session.add(new_grade)
    db.session.commit()
    return "Grade added successfully!"

@app.route('/displaystudents')
def display_students():
    sql = text('SELECT * FROM Student')
    result= db.session.execute(sql)
    return result.fetchall().__str__()
from sqlalchemy.sql import text

@app.route('/createview')
def create_view():
    view_sql =text( """
    CREATE VIEW view1 AS
    SELECT 
        s.id AS student_id,
        s.fname AS student_fname,
        s.lname AS student_lname,
        s.dob AS student_dob,
        s.email AS student_email,
        s.phone AS student_phone,
        s.enroll_date AS student_enroll_date,
        c.name AS class_name,
        f.fname AS faculty_fname,
        f.lname AS faculty_lname,
        d.name AS department_name,
        co.course_name,
        g.grade,
        g.grade_date
    FROM 
        Student s
    JOIN 
        Enrollments e ON s.id = e.student_id
    JOIN 
        Class c ON e.class_id = c.id
    JOIN 
        faculty f ON c.faculty_id = f.id
    JOIN 
        Department d ON f.department_id = d.id
    JOIN 
        Courses co ON c.course_id = co.course_id
    
    JOIN 
        Grade g ON e.enrollment_id = g.enrollment_id;
    """)
    db.session.execute(view_sql)
#@app.route('/displayview')
#def display_view():
 #   sql = text('SELECT * FROM view1')
  #  result= db.session.execute(sql)
   # return result.fetchall().__str__()
@app.route('/viewstudent')
def display_test():
    students = Student.query.all()
    student_data = []
    for student in students:
        c=Class.query.filter_by(id=student.class_id).first()
        student_dict = {
            'id': student.id,
            'fname': student.fname,
            'lname': student.lname,
            'dob': student.dob,
            'email': student.email,
            'phone': student.phone,
            'enroll_date': student.enroll_date,
            'class_id': c.name
        }
        student_data.append(student_dict)
    return jsonify(student_data)
@app.route('/viewclass')
def display_class():
    classes = Class.query.all()

    class_data = []
    for class1 in classes:
        f = faculty.query.filter_by(id=class1.faculty_id).first()
        c= Courses.query.filter_by(course_id=class1.course_id).first()
        class_dict = {
            'id': class1.id,
            'name': class1.name,
            'course_id': c.course_name,
            'faculty_id': f.fname
        }
        class_data.append(class_dict)
    return jsonify(class_data)
@app.route('/viewfaculty')
def display_faculty():
    faculties = faculty.query.all()
    faculty_data = []
    for faculty1 in faculties:
        d=Department.query.filter_by(id=faculty1.department_id).first()
        faculty_dict = {
            'id': faculty1.id,
            'fname': faculty1.fname,
            'lname': faculty1.lname,
            'email': faculty1.email,
            'phone': faculty1.phone,
            'department_id': d.name
        }
        faculty_data.append(faculty_dict)
    return jsonify(faculty_data)
@app.route('/viewdepartment')
def display_department():
    departments = Department.query.all()

    department_data = []
    for department in departments:
        h=faculty.query.filter_by(id=department.head).first()
        department_dict = {
            'id': department.id,
            'name': department.name,
            'head': h.fname + " " + h.lname
        }
        department_data.append(department_dict)
    return jsonify(department_data)

@app.route('/verifylogin', methods=['POST'])
def verify_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Authentication.query.filter_by(email=email).first()
    if user and user.password == password:
        return {"status":True}
    else:
        return {"status":False}
