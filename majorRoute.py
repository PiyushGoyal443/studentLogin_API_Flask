from fetchData import *

def majorRoute(reg_no = "", pswd = ""):
	#courses
	time_table = timetable(reg_no,pswd)['time_table']
	attendance = get_attendance_details(reg_no,pswd)['attendance_det']
	marks = get_marks(reg_no,pswd)['marks']

	examSchedule = get_exam_schedule(reg_no,pswd)

	faculty_advisor = get_facultyAdvisor_details(reg_no,pswd)["faculty_det"]

	academicHistory = get_acad_history(reg_no,pswd)

	#combining timetable attendance and marks as per their course code
	mkeys = marks.keys()
	tkeys = time_table.keys()
	data = []
	i = 0
	for key in tkeys:
		if key in mkeys:
			data.append({})
			data[i] = time_table[key]
			data[i]["attendance"] = attendance[key]
			data[i]["marks"] = marks[key]
			i = i+1
		else:
			data.append({})
			data[i] = time_table[key]
			data[i]["attendance"] = attendance[key]
			i = i+1

	return {"reg_no" : reg_no, "campus" : "vellore", "semester" : "WS", "courses" : data, "exam_schedule" : examSchedule, "faculty_advisor" : faculty_advisor, "academic_history" : academicHistory}