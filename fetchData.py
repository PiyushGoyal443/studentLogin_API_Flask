from login import login
from bs4 import BeautifulSoup
import datetime, pytz

#####################################################################################################################################################

def lgin(reg_no = "", pswd = ""):
	return { "reg_no": reg_no, "campus": "vellore", "status": {"message": "Successful execution", "code": 0} }

#####################################################################################################################################################

def results(reg_no = "", pswd = ""):

	#logging into student login
	br = login(reg_no,pswd)

	#checking that are we logged in or not
	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		br.open("https://academics.vit.ac.in/student/grade.asp?sem=WS")
		response = br.open("https://academics.vit.ac.in/student/grade.asp?sem=WS")
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findChildren('table')

		try:
			myTable = tables[1]
		except IndexError:
			myTable = 'null'
			return {"status" : "Not_Updated"}

		rows = myTable.findChildren(['th','tr'])
		result = {}

		return {"status" : "Updated"}
	else:
		print "FAIL"
		return {"status" : "Failure"}

#####################################################################################################################################################

def timetable(reg_no = "", pswd = ""):

	#logging into student login
	br = login(reg_no,pswd)

	#checking that are we logged in or not
	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
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
		ttable = {}

		#extracting data
		for row in rows:

			rowdata =  []
			cells = row.findAll('td')
			if len(cells) == 1:
				print "row_with_no_entries"
				continue

			else:

				for cell in cells:
					value = cell.getText()
					#print value
					rowdata.append(value)

				
				#if the course contains embedded lab
				if len(cells) == 10:
					ttable[rowdata[1].replace("\r\n\t\t","")+"_L"] = dict({("class_number",rowdata[0].replace("\r\n\t\t","")), ("course_code",rowdata[1].replace("\r\n\t\t","")), ("course_title",rowdata[2].replace("\r\n\t\t","")), ("course_type",rowdata[3].replace("\r\n\t\t","")), ("ltpjc",rowdata[4].replace("\n\r\n\t\t\t\t","").replace("\r\n\t\t\t\t\n","")), ("course_mode",rowdata[5].replace("\r\n\t\t","")), ("course_option",rowdata[6].replace("\r\n\t\t","")), ("slot",rowdata[7].replace("\r\n\t\t","")), ("venue",rowdata[8].replace("\r\n\t\t","")), ("faculty",rowdata[9].replace("\r\n\t\t",""))})
				else:
					ttable[rowdata[3].replace("\r\n\t\t","")] = dict({("class_number",rowdata[2].replace("\r\n\t\t","")), ("course_code",rowdata[3].replace("\r\n\t\t","")), ("course_title",rowdata[4].replace("\r\n\t\t","")), ("course_type",rowdata[5].replace("\r\n\t\t","")), ("ltpjc",rowdata[6].replace("\n\r\n\t\t\t\t","").replace("\r\n\t\t\t\t\n","")), ("course_mode",rowdata[7].replace("\r\n\t\t","")), ("course_option",rowdata[8].replace("\r\n\t\t","")), ("slot",rowdata[9].replace("\r\n\t\t","")), ("venue",rowdata[10].replace("\r\n\t\t","")), ("faculty",rowdata[11].replace("\r\n\t\t","")), ("registration_status",rowdata[12].replace("\r\n\t\t",""))})
		return {"status" : "Success" , "time_table" : ttable}
	else :
		print "FAIL"
		return {"status" : "Failure"}

#####################################################################################################################################################

def get_facultyAdvisor_details(reg_no = "", pwd = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	#checking that are we logged in or not

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		#opening faculty advisor details page
		br.open("https://academics.vit.ac.in/student/faculty_advisor_view.asp")
		response = br.open("https://academics.vit.ac.in/student/faculty_advisor_view.asp")
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findChildren('table')
		myTable = tables[1]
		rows = myTable.findChildren(['th','tr'])

		#initialising some required variables
		facdet = {}

		#extracting data
		for row in rows:

			rowdata =  []
			cells = row.findChildren('td')

			if len(cells) == 1:
				continue

			else:
				for cell in cells:

					value = cell.string
					#print value
					rowdata.append(value)

				facdet[rowdata[0].replace("\r\n\t\t","")] = rowdata[1].replace("\r\n\t\t","")
		return {"status" : "Success" , "faculty_det" : facdet}

	else :
		print "FAIL"
		return {"status" : "Failure"}

#####################################################################################################################################################

def get_attendance_details(reg_no = "", pwd = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

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
		attndet = {}

		#extracting data
		for row in rows:

			rowdata = []
			details = []
			cells = row.findChildren('td')
			for cell in cells:

				value = cell.getText()
				#print value
				rowdata.append(value)

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

					data = []
					dcells = drow.findChildren('td')
					for dcell in dcells:

						value = dcell.getText()
						#print value
						data.append(value)

					details.append({"date" : data[1], "slot" : data[2], "status" : data[3], "class_units" : data[4], "reason" : data[5]})

				br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })

				if rowdata[1] not in attndet.keys():
					attndet[rowdata[1]] = {"registration_date" : rowdata[5], "attended_classes" : rowdata[6], "total_classes" : rowdata[7], "attendance_percentage" : rowdata[8], "details" : details}
				else:
					attndet[rowdata[1]+"_L"] = {"registration_date" : rowdata[5], "attended_classes" : rowdata[6], "total_classes" : rowdata[7], "attendance_percentage" : rowdata[8], "details" : details}

			except:
				br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })
				if rowdata[1] not in attndet.keys():
					attndet[rowdata[1]] = {"registration_date" : rowdata[5], "attended_classes" : rowdata[6], "total_classes" : rowdata[7], "attendance_percentage" : rowdata[8], "details" : {}}
				else:
					attndet[rowdata[1]+"_L"] = {"registration_date" : rowdata[5], "attended_classes" : rowdata[6], "total_classes" : rowdata[7], "attendance_percentage" : rowdata[8], "details" : {}}

		return {"status" : "Success" , "attendance_det" : attndet}

	else :
		print "FAIL"
		return {"status" : "Failure"}

#####################################################################################################################################################

def get_exam_schedule(reg_no = "", pwd = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	#checking that are we logged in or not

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

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
			return {"status" : "Not_Updated"}

		rows = myTable.findChildren(['th','tr'])
		rows = rows[2:]

		#initialising some required variables for getting schedule for CAT-1
		schedule = {}

		#holding the cat1, cat2, termend schedules in queue
		p = q.Queue()
		
		#extracting data
		for row in rows:

			rowdata = []
			cells = row.findChildren('td')

			if len(cells) != 1:
				for cell in cells:

					value = cell.string
					#print value
					rowdata.append(value)

				schedule[rowdata[1].replace("\r\n\t\t","")] = dict({("crTitle",rowdata[2].replace("\r\n\t\t","")), ("slot",rowdata[4].replace("\r\n\t\t","")), ("date",rowdata[5].replace("\r\n\t\t","")), ("day",rowdata[6].replace("\r\n\t\t","")), ("session",rowdata[7].replace("\r\n\t\t","")), ("time",rowdata[8].replace("\r\n\t\t",""))})
			
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

		return {"status" : "Success" , "cat1" : cat1 , "cat2" : cat2 , "term_end" : termend}

	else :
		print "FAIL"
		return {"status" : "Failure"}

#####################################################################################################################################################

def get_marks(reg_no = "", pwd = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	#checking that are we logged in or not

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

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
			else:
				assessments.append({"title" : "Lab_cam", "max_marks" : 50, "weightage" : 50, "conducted_on" : "Tentative, set by lab faculty", "status" : rowdata[6], "scored_marks" : rowdata[7], "scored_percentage" : rowdata[7] })
				#assessments.append({"title" : "FAT", "max_marks" : 50, "weightage" : 50, "conducted_on" : "Tentative, set by lab faculty", "status" : rowdata[8], "scored_marks" : rowdata[9], "scored_percentage" : rowdata[9] })
				
				marks[rowdata[2]+"_L"] = {"assessments" : assessments, "max_marks" : 100, "max_percentage" : 100, "scored_marks" : float(rowdata[7]), "scored_percentage" : (float(rowdata[7]))}

		try:
			myTable = tables[2]
		except IndexError:
			myTable = 'null'
			return {"status" : "Success" , "marks" : marks}

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

			
		return {"status" : "Success" , "marks" : marks}

	else :
		print "FAIL"
		return {"status" : "Failure"}

#####################################################################################################################################################

def get_spotlight():

	import mechanize

	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)

	br.open("https://academics.vit.ac.in/include_spotlight_part01.asp")
	response = br.open("https://academics.vit.ac.in/include_spotlight_part01.asp")
	soup = BeautifulSoup(response.get_data())
	
	tables = soup.findAll('table')

	myTable = tables[0]

	rows = myTable.findChildren(['th','tr'])
	acad = []

	for row in rows:

		text = row.find('td').string

		if row.find('a') is not None:
			link = "https://academics.vit.ac.in/"+row.find('a')['href'] 
		else:
			link = "No_link"

		if text == None:
			print "hi"
		else:
			acad.append({"text": text, "url" : link})

	br.open("https://academics.vit.ac.in/include_spotlight_part02.asp")
	response = br.open("https://academics.vit.ac.in/include_spotlight_part02.asp")
	soup = BeautifulSoup(response.get_data())
	
	try:
		tables = soup.findAll('table')
		myTable = tables[0]

		rows = myTable.findChildren(['th','tr'])
		coe = []
		for row in rows:

			text = row.find('td').string

			if row.find('a') is not None:
				link = "https://academics.vit.ac.in/"+row.find('a')['href'] 
			else:
				link = "No_link"

			if text == None:
				print "hi"
			else:
				coe.append({"text": text, "url" : link})

	except IndexError:
		myTable = 'null'
		coe = 'no_data'

	br.open("https://academics.vit.ac.in/include_spotlight_part03.asp")
	response = br.open("https://academics.vit.ac.in/include_spotlight_part03.asp")
	soup = BeautifulSoup(response.get_data())

	try:
		tables = soup.findAll('table')
		myTable = tables[0]

		rows = myTable.findChildren(['th','tr'])
		research = []

		for row in rows:

			text = row.find('td').string

			if row.find('a') is not None:
				link = "https://academics.vit.ac.in/"+row.find('a')['href'] 
			else:
				link = "No_link"

			if text != None:
				research.append({"text": text, "url" : link})

	except IndexError:
		myTable = 'null'
		research = 'no_data'

	return {"status" : "Success" , "academics" : acad, "COE" : coe , "research" : research}

#####################################################################################################################################################

"""def get_apt_attendance(reg_no = "", pwd = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		br.open("https://academics.vit.ac.in/student/apt_attendance.asp")
		response = br.open("https://academics.vit.ac.in/student/apt_attendance.asp")
		soup = BeautifulSoup(response.get_data())

		tables = soup.findAll('table')
		try:
			myTable = tables[3]
		except:
			return {"status" : "Success" , "apt attendance" : "not updated"}

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#initialising some required variables
		aptAttn = []

		#extracting data
		for row in rows:

			rowdata =  []
			cells = row.findChildren('td')

			for cell in cells:

				value = cell.string
				#print value
				rowdata.append(value)

			if len(cells) == 4:
				aptAttn.append({ "date" : rowdata[0].replace("\r\n\t\t","") , "session" : rowdata[1].replace("\r\n\t\t","") , "status" : rowdata[2].replace("\r\n\t\t","")})
			else:
				aptAttn.append({ "details" : rowdata[0].replace("\r\n\t\t","") , "value" : rowdata[1].replace("\r\n\t\t","")})

		return {"status" : "Success" , "apt attendance" : aptAttn}

	else :
		print "FAIL"
		return {"status" : "Failure"}"""

#####################################################################################################################################################

def get_acad_history(reg_no = "", pwd = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		br.open("https://academics.vit.ac.in/student/student_history.asp")
		response = br.open("https://academics.vit.ac.in/student/student_history.asp")
		soup = BeautifulSoup(response.get_data())

		tables = soup.findAll('table')
		myTable = tables[2]

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#initialising some required variables
		history1 = {}
		j = 0

		#extracting data
		for row in rows:

			rowdata =  []
			cells = row.findChildren('td')
			cells = cells[1:6]
			j=0
			for cell in cells:

				value = cell.string
				#print value
				rowdata.append(value)

			history1[rowdata[0].replace("\r\n\t\t","")] = dict({("course_title" , rowdata[1].replace("\r\n\t\t","")) , ("course_type" , rowdata[2].replace("\r\n\t\t","")) , ("credit" , rowdata[3].replace("\r\n\t\t","")) , ("grade" , rowdata[4].replace("\r\n\t\t",""))})

		myTable = tables[3]

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#initialising some required variables
		history2 = {}

		#extracting data
		for row in rows:

			rowdata =  []
			cells = row.findChildren('td')
			for cell in cells:

				value = cell.string
				#print value
				rowdata.append(value)

			history2 = dict({("credits registered" , rowdata[0].replace("\r\n\t\t","")) , ("credits earned" , rowdata[1].replace("\r\n\t\t","")) , ("cgpa" , rowdata[2].replace("\r\n\t\t","")) , ("rank" , rowdata[3].replace("\r\n\t\t",""))})

		myTable = tables[4]

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#initialising some required variables
		grdSumm = {}

		#extracting data
		for row in rows:

			rowdata =  []
			cells = row.findChildren('td')
			for cell in cells:

				value = cell.string
				#print value
				rowdata.append(value)

			grdSumm = dict({("S grades" , rowdata[0].replace("\r\n\t\t","")) , ("A grades" , rowdata[1].replace("\r\n\t\t","")) , ("B grades" , rowdata[2].replace("\r\n\t\t","")) , ("C grades" , rowdata[3].replace("\r\n\t\t","")) , ("D grades" , rowdata[4].replace("\r\n\t\t","")) , ("E grades" , rowdata[5].replace("\r\n\t\t","")) , ("F grades" , rowdata[6].replace("\r\n\t\t","")) , ("N grades" , rowdata[7].replace("\r\n\t\t",""))})

		return {"status" : "Success" , "history 1" : history1 , "history 2" : history2 , "grade summary" : grdSumm}

	else :
		print "FAIL"
		return {"status" : "Failure"}

#####################################################################################################################################################

def change_password(reg_no = "", pwd = "", newpwd = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		br.open("https://academics.vit.ac.in/student/changepswd.asp")
		response = br.open("https://academics.vit.ac.in/student/changepswd.asp")

		#selecting the form
		br.select_form("changepswd")

		#filling the form details
		br["oldpswd"] = str(pwd)
		br["newpswd"] = str(newpwd)
		br["cfmnewpswd"] = str(newpwd)

		#submitting the values and changing the password
		br.method = "POST"
		response = br.submit()

		soup = BeautifulSoup(response.get_data())

		#extracting status of password changing procedure
		tables = soup.findAll("table")
		myTable = tables[0]
		rows = myTable.findChildren(['th','tr'])
		cells = rows[0].findChildren("td")
		font = cells[1].findAll("font")
		change_status = font[1].string

		if change_status == "Incorrect old password...!!":
			print change_status

		elif font[1].string == "Your password is successfully changed.":
			print change_status

		else:
			return {"status" : "Success" , "password change status" : "other errors"}

		return {"status" : "Success" , "password change status" : change_status}

	else :
		print "FAIL"
		return {"status" : "Failure"}

#####################################################################################################################################################

"""def getFaculties(reg_no = "", pwd = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		br.open("https://academics.vit.ac.in/student/getfacdet.asp?fac= ")
		response = br.open("https://academics.vit.ac.in/student/getfacdet.asp?fac= ")

		#selecting the form

		soup = BeautifulSoup(response.get_data())
		
		#extracting status of password changing procedure
		tables = soup.findAll("table")
		myTable = tables[0]
		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#initialising some required variables
		facDetails = {}
		j = 0

		#extracting data
		for row in rows:

			rowdata =  []
			cells = row.findChildren('td')
			cells = cells[0:4]
			j=0
			for cell in cells:

				value = cell.string
				#print value
				rowdata.append(value)

			a = cells[3].find('a')['href']
			facDetails[rowdata[0]] = dict({("facName" , rowdata[0]) , ("designation" , rowdata[1]) , ("school" , rowdata[2]) , ("detailedLink" , "https://academics.vit.ac.in/student/"+a)})

		return {"status" : "Success" ,"data" : facDetails}

	else :
		print "FAIL"
		return {"status" : "Failure"}"""
