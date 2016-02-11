from fetchData import *
from login import login
from bs4 import BeautifulSoup
import datetime, pytz

def majorRoute(reg_no = "", pswd = ""):
	#courses

	#logging into student login
	br = login(reg_no,pswd)

	#checking that are we logged in or not
	if br.geturl() == ("https://academics.vit.ac.in/student/stud_home.asp") or br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		#opening time table page
		br.open("https://academics.vit.ac.in/student/timetable_ws.asp")
		response = br.open("https://academics.vit.ac.in/student/timetable_ws.asp")
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findAll('table')

		#getting required table
		myTable = tables[1]
		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#initialising some required variables
		time_table = {}

		#extracting data
		for row in rows:

			cells = row.findAll('td')
			if len(cells) == 1:
				print "row_with_no_entries"
				continue

			else:
				
				#if the course contains embedded lab
				if len(cells) == 10:
					if cells[1].getText().replace("\r\n\t\t","") in time_table.keys():
						time_table[cells[1].getText().replace("\r\n\t\t","")+"_L"] = dict({("class_number",cells[0].getText().replace("\r\n\t\t","")), ("course_code",cells[1].getText().replace("\r\n\t\t","")), ("course_title",cells[2].getText().replace("\r\n\t\t","")), ("course_type",cells[3].getText().replace("\r\n\t\t","")), ("ltpjc",cells[4].getText().replace("\n\r\n\t\t\t\t","").replace("\r\n\t\t\t\t\n","")), ("course_mode",cells[5].getText().replace("\r\n\t\t","")), ("course_option",cells[6].getText().replace("\r\n\t\t","")), ("slot",cells[7].getText().replace("\r\n\t\t","")), ("venue",cells[8].getText().replace("\r\n\t\t","")), ("faculty",cells[9].getText().replace("\r\n\t\t",""))})
					else:
						time_table[cells[1].getText().replace("\r\n\t\t","")] = dict({("class_number",cells[0].getText().replace("\r\n\t\t","")), ("course_code",cells[1].getText().replace("\r\n\t\t","")), ("course_title",cells[2].getText().replace("\r\n\t\t","")), ("course_type",cells[3].getText().replace("\r\n\t\t","")), ("ltpjc",cells[4].getText().replace("\n\r\n\t\t\t\t","").replace("\r\n\t\t\t\t\n","")), ("course_mode",cells[5].getText().replace("\r\n\t\t","")), ("course_option",cells[6].getText().replace("\r\n\t\t","")), ("slot",cells[7].getText().replace("\r\n\t\t","")), ("venue",cells[8].getText().replace("\r\n\t\t","")), ("faculty",cells[9].getText().replace("\r\n\t\t",""))})
				else:
					time_table[cells[3].getText().replace("\r\n\t\t","")] = dict({("class_number",cells[2].getText().replace("\r\n\t\t","")), ("course_code",cells[3].getText().replace("\r\n\t\t","")), ("course_title",cells[4].getText().replace("\r\n\t\t","")), ("course_type",cells[5].getText().replace("\r\n\t\t","")), ("ltpjc",cells[6].getText().replace("\n\r\n\t\t\t\t","").replace("\r\n\t\t\t\t\n","")), ("course_mode",cells[7].getText().replace("\r\n\t\t","")), ("course_option",cells[8].getText().replace("\r\n\t\t","")), ("slot",cells[9].getText().replace("\r\n\t\t","")), ("venue",cells[10].getText().replace("\r\n\t\t","")), ("faculty",cells[11].getText().replace("\r\n\t\t","")), ("registration_status",cells[12].getText().replace("\r\n\t\t",""))})

		
		############################################### ATTENDANCE ##############################################################
		

		months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}

		#getting today's date
		tz = pytz.timezone('Asia/Kolkata')
		now = datetime.datetime.now(tz)
		today = str(now.day) + "-" + months[now.month] + "-" + str(now.year)

		#opening the attendance page
		br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS")
		response = br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS")
		soup = BeautifulSoup(response.get_data())

		br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })
		response = br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findChildren('table')
		myTable = tables[3]
		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]
		i = 1

		#initialising some required variables
		attendance = {}

		#extracting data
		for row in rows:

			details = []
			cells = row.findChildren('td')

			br.select_form(nr=i)
			i = i+1

			r = br.submit()
			dsoup = BeautifulSoup(r.get_data())
			dtables = dsoup.findChildren('table')

			try:
				dmyTable = dtables[2]
				drows = dmyTable.findChildren(['th','tr'])
				drows = drows[2:]


				for drow in drows:

					dcells = drow.findChildren('td')

					details.append({"date" : dcells[1].getText(), "slot" : dcells[2].getText(), "status" : dcells[3].getText(), "class_units" : dcells[4].getText(), "reason" : dcells[5].getText()})

				br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })

				if cells[1].getText().replace("\r\n\t\t","") not in attendance.keys():
					attendance[cells[1].getText().replace("\r\n\t\t","")] = {"registration_date" : cells[5].getText().replace("\r\n\t\t",""), "attended_classes" : cells[6].getText().replace("\r\n\t\t",""), "total_classes" : cells[7].getText().replace("\r\n\t\t",""), "attendance_percentage" : cells[8].getText().replace("\r\n\t\t",""), "details" : details}
				else:
					attendance[cells[1].getText().replace("\r\n\t\t","")+"_L"] = {"registration_date" : cells[5].getText().replace("\r\n\t\t",""), "attended_classes" : cells[6].getText().replace("\r\n\t\t",""), "total_classes" : cells[7].getText().replace("\r\n\t\t",""), "attendance_percentage" : cells[8].getText().replace("\r\n\t\t",""), "details" : details}

			except:
				br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })
				if cells[1].getText().replace("\r\n\t\t","") not in attendance.keys():
					attendance[cells[1].getText().replace("\r\n\t\t","")] = {"registration_date" : cells[5].getText().replace("\r\n\t\t",""), "attended_classes" : cells[6].getText().replace("\r\n\t\t",""), "total_classes" : cells[7].getText().replace("\r\n\t\t",""), "attendance_percentage" : cells[8].getText().replace("\r\n\t\t",""), "details" : {}}
				else:
					attendance[cells[1].getText().replace("\r\n\t\t","")+"_L"] = {"registration_date" : cells[5].getText().replace("\r\n\t\t",""), "attended_classes" : cells[6].getText().replace("\r\n\t\t",""), "total_classes" : cells[7].getText().replace("\r\n\t\t",""), "attendance_percentage" : cells[8].getText().replace("\r\n\t\t",""), "details" : {}}

		
		################################################# MARKS #######################################################

		#opening marks page

		br.open("https://academics.vit.ac.in/student/marks.asp?sem=WS")
		response = br.open("https://academics.vit.ac.in/student/marks.asp?sem=WS")
		soup = BeautifulSoup(response.get_data())

		#extracting tables

		tables = soup.findAll('table')
		myTable = tables[1]

		#initialising some required variables

		marks = {}
		rows = myTable.findChildren(['th','tr'])
		rows = rows[2:]

		#extracting data

		for row in rows:
			rowdata = []
			assessments = []
			cells = row.findAll('td')
			j = 0

			for cell in cells:
				value = cell.getText()
				#print value
				if value is u'' or value is u'N/A':
					rowdata.append('0')
					
				else:
					rowdata.append(value)
			#print rowdata

			if len(cells) == 18:
				assessments.append({"title" : "CAT-I", "max_marks" : 50, "weightage" : 15, "conducted_on" : "Check Exam Schedule", "status" : rowdata[5], "scored_marks" : rowdata[6], "scored_percentage" : (((float(rowdata[6]))/50)*15) })
				assessments.append({"title" : "CAT-II", "max_marks" : 50, "weightage" : 15, "conducted_on" : "Check Exam Schedule", "status" : rowdata[7], "scored_marks" : rowdata[8], "scored_percentage" : (((float(rowdata[8]))/50)*15) })
				assessments.append({"title" : "Quiz-I", "max_marks" : 5, "weightage" : 5, "conducted_on" : "Check Exam Schedule", "status" : rowdata[9], "scored_marks" : rowdata[10], "scored_percentage" : rowdata[10] })
				assessments.append({"title" : "Quiz-II", "max_marks" : 5, "weightage" : 5, "conducted_on" : "Check Exam Schedule", "status" : rowdata[11], "scored_marks" : rowdata[12], "scored_percentage" : rowdata[12] })
				assessments.append({"title" : "Quiz-III", "max_marks" : 5, "weightage" : 5, "conducted_on" : "Check Exam Schedule", "status" : rowdata[13], "scored_marks" : rowdata[14], "scored_percentage" : rowdata[14] })
				assessments.append({"title" : "Assignment", "max_marks" : 5, "weightage" : 5, "conducted_on" : "Check Exam Schedule", "status" : rowdata[15], "scored_marks" : rowdata[16], "scored_percentage" : rowdata[16] })
				#assessments.append({"title" : "FAT", "max_marks" : 100, "weightage" : 50, "conducted_on" : "Check Exam Schedule", "status" : rowdata[18], "scored_marks" : rowdata[19], "scored_percentage" : (((float(rowdata[19]))/100)*50) }) 

				marks[rowdata[2].replace("\r\n\t\t","")] = {"assessments" : assessments, "max_marks" : 220, "max_percentage" : 100, "scored_marks" : (float(rowdata[6])+float(rowdata[8])+float(rowdata[10])+float(rowdata[12])+float(rowdata[14])+float(rowdata[16])), "scored_percentage" : ((((float(rowdata[6]))/50)*15)+(((float(rowdata[8]))/50)*15)+(float(rowdata[10]))+(float(rowdata[12]))+(float(rowdata[14]))+(float(rowdata[16])))}
			elif len(cells) == 6:
				continue
			else:
				assessments.append({"title" : "Lab_cam", "max_marks" : 50, "weightage" : 50, "conducted_on" : "Tentative, set by lab faculty", "status" : rowdata[6], "scored_marks" : rowdata[7], "scored_percentage" : rowdata[7] })
				#assessments.append({"title" : "FAT", "max_marks" : 50, "weightage" : 50, "conducted_on" : "Tentative, set by lab faculty", "status" : rowdata[8], "scored_marks" : rowdata[9], "scored_percentage" : rowdata[9] })
				if rowdata[2] in marks.keys():
					marks[rowdata[2]+"_L"] = {"assessments" : assessments, "max_marks" : 100, "max_percentage" : 100, "scored_marks" : float(rowdata[7]), "scored_percentage" : (float(rowdata[7]))}
				else:
					marks[rowdata[2]] = {"assessments" : assessments, "max_marks" : 100, "max_percentage" : 100, "scored_marks" : float(rowdata[7]), "scored_percentage" : (float(rowdata[7]))}

		try:
			myTable = tables[2]
		except IndexError:
			myTable = 'null'

		else:

			rows = myTable.findAll(['th','tr'])
			rows = rows[1:]
			flag = 0
			assessments = []

			for row in rows:

				rowdata = []
				cells = row.findAll('td')

				for cell in cells:
					value = cell.string
					#print value
					if value is u'' or value is u'N/A':
						rowdata.append('0')
					else:
						rowdata.append(value)

				#print rowdata

				if len(cells) == 11:
					if flag == 1:
						marks[key] = {"assessments" : assessments}
						assessments = []
					else:
						flag = 1
					key = rowdata[2].replace("\r\n\t\t","")
					assessments.append({"title" : rowdata[6]})
					assessments.append({"title" : rowdata[7]})
					assessments.append({"title" : rowdata[8]})
					assessments.append({"title" : rowdata[9]})
					assessments.append({"title" : rowdata[10]})
					#assessments.append({"title" : rowdata[11]})
			

				else:
					assessments[0][rowdata[0]] = rowdata[1]
					assessments[1][rowdata[0]] = rowdata[2]
					assessments[2][rowdata[0]] = rowdata[3]
					assessments[3][rowdata[0]] = rowdata[4]
					assessments[4][rowdata[0]] = rowdata[5]
					#assessments[5][rowdata[0]] = rowdata[6]

		########################################## EXAM SCHEDULE ###########################################

		#inmporting Queue
		import Queue as q

		#opening exam schedule page

		br.open("https://academics.vit.ac.in/student/exam_schedule.asp?sem=WS")
		response = br.open("https://academics.vit.ac.in/student/exam_schedule.asp?sem=WS")
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findAll('table')

		try:
			myTable = tables[1]
		except IndexError:
			myTable = 'null'
			examSchedule = {"cat1" : "Not_updated" , "cat2" : "Not_updated" , "term_end" : "Not_updated"}

		else:

			rows = myTable.findChildren(['th','tr'])
			rows = rows[2:]

			#initialising some required variables for getting schedule for CAT-1
			schedule = {}

			#holding the cat1, cat2, termend schedules in queue
			p = q.Queue()
			
			#extracting data
			for row in rows:

				cells = row.findChildren('td')

				if len(cells) != 1:

					schedule[cells[1].string.replace("\r\n\t\t","")] = dict({("crTitle",cells[2].string.replace("\r\n\t\t","")), ("slot",cells[4].string.replace("\r\n\t\t","")), ("date",cells[5].string.replace("\r\n\t\t","")), ("day",cells[6].string.replace("\r\n\t\t","")), ("session",cells[7].string.replace("\r\n\t\t","")), ("time",cells[8].string.replace("\r\n\t\t",""))})
			
				elif len(cells) == 1:

					p.put(schedule)
					schedule = {}
					continue

			cat1 = p.get()

			if p.empty():
				cat2 = {}
			else:
				cat2 = p.get()
			if p.empty():
				termend = {}
			else:
				termend = p.get()

			examSchedule = {"cat1" : cat1 , "cat2" : cat2 , "term_end" : termend}


		################################################### ACADEMIC HISTORY ##################################################


		br.open("https://academics.vit.ac.in/student/student_history.asp")
		response = br.open("https://academics.vit.ac.in/student/student_history.asp")
		soup = BeautifulSoup(response.get_data())

		tables = soup.findAll('table')
		myTable = tables[2]

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#initialising some required variables
		history1 = {}

		#extracting data
		for row in rows:

			cells = row.findChildren('td')
			cells = cells[1:6]

			history1[cells[0].string.replace("\r\n\t\t","")] = dict({("course_title" , cells[1].string.replace("\r\n\t\t","")) , ("course_type" , cells[2].string.replace("\r\n\t\t","")) , ("credit" , cells[3].string.replace("\r\n\t\t","")) , ("grade" , cells[4].string.replace("\r\n\t\t",""))})

		myTable = tables[3]

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#initialising some required variables
		history2 = {}

		#extracting data
		for row in rows:

			cells = row.findChildren('td')

			history2 = dict({("credits registered" , cells[0].string.replace("\r\n\t\t","")) , ("credits earned" , cells[1].string.replace("\r\n\t\t","")) , ("cgpa" , cells[2].string.replace("\r\n\t\t","")) , ("rank" , cells[3].string.replace("\r\n\t\t",""))})

		myTable = tables[4]

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#initialising some required variables
		grdSumm = {}

		#extracting data
		for row in rows:

			cells = row.findChildren('td')

			grdSumm = dict({("S grades" , cells[0].string.replace("\r\n\t\t","")) , ("A grades" , cells[1].string.replace("\r\n\t\t","")) , ("B grades" , cells[2].string.replace("\r\n\t\t","")) , ("C grades" , cells[3].string.replace("\r\n\t\t","")) , ("D grades" , cells[4].string.replace("\r\n\t\t","")) , ("E grades" , cells[5].string.replace("\r\n\t\t","")) , ("F grades" , cells[6].string.replace("\r\n\t\t","")) , ("N grades" , cells[7].string.replace("\r\n\t\t",""))})

		academicHistory = {"history 1" : history1 , "history 2" : history2 , "grade summary" : grdSumm}

		############################################# FACULTY ADVISOR DETAILS ###############################################


		#opening faculty advisor details page
		br.open("https://academics.vit.ac.in/student/faculty_advisor_view.asp")
		response = br.open("https://academics.vit.ac.in/student/faculty_advisor_view.asp")
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findChildren('table')
		myTable = tables[1]
		rows = myTable.findChildren(['th','tr'])

		#initialising some required variables
		faculty_advisor = {}

		#extracting data
		for row in rows:

			cells = row.findChildren('td')

			if len(cells) == 1:
				continue

			else:
				faculty_advisor[cells[0].string.replace("\r\n\t\t","")] = cells[1].string.replace("\r\n\t\t","")

		############################################# MESSAGES ###############################################

		br.open("https://academics.vit.ac.in/student/class_message_view.asp?sem=WS")
		response = br.open("https://academics.vit.ac.in/student/class_message_view.asp?sem=WS")

		soup = BeautifulSoup(response.get_data())
		try:
			tables = soup.findAll('table')
			myTable = tables[1]
			rows = myTable.findChildren(['th','tr'])

			rows = rows[1:]
			messages = []

			for row in rows[:-1]:

				cells = row.findChildren('td')
				
				messages.append({"From" : cells[0].string.replace("\r\n\t\t",""), "Course" : cells[1].string.replace("\r\n\t\t",""), "Message" : cells[2].string.replace("\r\n\t\t","").replace("\r\n"," "), "Posted on" : cells[3].string.replace("\r\n\t\t","")})
		except:
			messages = []

		#combining timetable attendance and marks as per their course code
		mkeys = marks.keys()
		tkeys = time_table.keys()
		akeys = attendance.keys()
		data = []
		i = 0
		for key in tkeys:

			data.append({})
			data[i] = time_table[key]
			if key in akeys:
				data[i]["attendance"] = attendance[key]
			else:
				print "no attendance details"
			if key in mkeys:
				data[i]["marks"] = marks[key]
			else:
				print "no marks details"
			i = i+1

		return {"reg_no" : reg_no, "campus" : "vellore", "semester" : "WS", "courses" : data, "exam_schedule" : examSchedule, "faculty_advisor" : faculty_advisor, "academic_history" : academicHistory, "messages" : messages}

	else :
		print "FAIL"
		return {"status" : "Failure"}
