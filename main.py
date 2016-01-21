################################################################################ IMPORTS ##############

from flask import Flask, request, jsonify
from fetchData import *
from CoursePage import get_courses, get_slot, get_faculty, get_data
from majorRoute import majorRoute
import os

app = Flask(__name__)

################################################################################ HOME ##################

@app.route('/home')
def hello_world(): return "welcome_to_student_login_api"

################################################################################ FACULTY ADVISOR #######

@app.route('/login', methods=["GET"])
def login_det():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")

	return jsonify(**lgin(reg_no, pwd))

################################################################################ SPOTLIGHT #############

@app.route('/spotlight')
def spotlight():
	return jsonify(**get_spotlight())

################################################################################ FACULTY ADVISOR #######

@app.route('/facadvdet', methods=["GET"])
def login_facultyAdvisor():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")

	return jsonify(**get_facultyAdvisor_details(reg_no, pwd))

################################################################################ TIME TABLE ############

@app.route('/timetable', methods=["GET"])
def login_timetable():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")

	return jsonify(**timetable(reg_no, pwd))

################################################################################ ATTENDANCE ############

@app.route('/attendance', methods=["GET"])
def login_attendance():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")

	return jsonify(**get_attendance_details(reg_no, pwd))

################################################################################ MARKS #################

@app.route('/marks', methods=["GET"])
def get_mark():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")

	return jsonify(**get_marks(reg_no, pwd))

################################################################################ EXAM SCHEDULE #########

@app.route('/examschedule', methods=["GET"])
def login_examschedule():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")

	return jsonify(**get_exam_schedule(reg_no, pwd))

################################################################################ COURSE PAGE ###########

@app.route('/coursepage/courses', methods=["GET"])
def courseBase():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")

	return jsonify(**get_courses(reg_no, pwd))

@app.route('/coursepage/slots', methods=["GET"])
def courselevel1():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")
	crs = request.args.get("crs")

	return jsonify(**get_slot(reg_no, pwd,crs))

@app.route('/coursepage/faculties', methods=["GET"])
def courselevel2():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")
	crs = request.args.get("crs")
	slt = request.args.get("slt").replace(" ","+")

	return jsonify(**get_faculty(reg_no, pwd,crs,slt))

@app.route('/coursepage/data', methods=["GET"])
def courselevel3():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")
	crs = request.args.get("crs")
	slt = request.args.get("slt").replace(" ","+")
	fac = request.args.get("fac")

	return jsonify(**get_data(reg_no, pwd,crs,slt,fac))

################################################################################ APT ATTENDANCE ########

"""@app.route('/aptattn', methods=["GET"])
def aptattendance():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")

	data = get_apt_attendance(reg_no, pwd)
	return jsonify(**data)"""

################################################################################ ACADEMIC HISTORY ######

@app.route('/acadhist', methods=["GET"])
def acadHistory():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")

	return jsonify(**get_acad_history(reg_no, pwd))

################################################################################ RESULT ################

@app.route('/result')
def result():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")

	return jsonify(**results(reg_no,pwd))

################################################################################ CHANGE PASSWORD #######

@app.route('/changepswd', methods=["GET"])
def passwordchange():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")
	newpwd = request.args.get("npsswd")

	return jsonify(**change_password(reg_no, pwd, newpwd))

################################################################################ FACULTY SEARCH ######

@app.route('/getFaculty', methods = ["GET"])
def getData():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")
	query = request.args.get("facName")
	data = getFaculties(reg_no, pwd, query)
	return jsonify(**data)

################################################################################ FACULTY DETAILS ######

@app.route('/getFacultyDet', methods = ["GET"])
def getdata():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")
	empid = request.args.get("empId")
	data = getFaculty_det(reg_no, pwd, empid)
	return jsonify(**data)

################################################################################ REFRESH ###############

@app.route('/refresh', methods = ["GET"])
def Refresh():
	reg_no = request.args.get("regNo")
	pwd = request.args.get("psswd")

	return jsonify(**majorRoute(reg_no, pwd))

################################################################################ MAIN ##################

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.debug = True
	app.run(host='0.0.0.0', port=port)

################################################################################ END ###################
