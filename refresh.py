from login import login
from bs4 import BeautifulSoup
import datetime, pytz
import threading

#initialising some required variables
threadLock = threading.Lock()
threads = []
months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}

#getting today's date
tz = pytz.timezone('Asia/Kolkata')
now = datetime.datetime.now(tz)
today = str(now.day) + "-" + months[now.month] + "-" + str(now.year)

#overloading thread init and run function
class myThread(threading.Thread):

	#overloading the __init__ function
	def __init__(self, row, status, reqvar, *args):
		threading.Thread.__init__(self)

		self.row = row
		self.status = status
		self.reqvar = reqvar

		#for attendance and cal
		if self.status in [2,8]: 
			self.i = args[0]
			self.br = args[1]

	#overloading the run function
	def run(self):
		
		threadLock.acquire()

		if self.status == 1:
			timeScrape(self.row, self.reqvar)

		elif self.status == 2:
			attenScrape(self.row, self.br, self.i, self.reqvar)

		elif self.status == 3:
			mark14Scrape(self.row, self.reqvar)

		elif self.status == 4:
			mark15Scrape(self.row, self.reqvar)

		elif self.status == 5:
			facScrape(self.row, self.reqvar)

		elif self.status == 6:
			msgScrape(self.row, self.reqvar)

		elif self.status > 70 and self.status < 80:
			acadScrape(self.row, self.reqvar, self.status)

		elif self.status == 8:
			calScrape(self.br, self.row, self.i, self.reqvar)

		threadLock.release()

#fuction to scrape the row data of timetable
def timeScrape(row, time_table):

	cells = row.findAll('td')

	#handeling the row with 1 column
	if len(cells) == 1:

		print "row_with_no_entries"

	else:
				
		#for embedded labs or lab only courses
		if len(cells) == 10:

			#for embedded labs
			if cells[1].getText().replace("\r\n\t\t","") in time_table.keys():

				time_table[cells[1].getText().replace("\r\n\t\t","")+"_L"] = dict({("class_number",cells[0].getText().replace("\r\n\t\t","")), ("course_code",cells[1].getText().replace("\r\n\t\t","")), ("course_title",cells[2].getText().replace("\r\n\t\t","")), ("course_type",cells[3].getText().replace("\r\n\t\t","")), ("ltpjc",cells[4].getText().replace("\n\r\n\t\t\t\t","").replace("\r\n\t\t\t\t\n","")), ("course_mode",cells[5].getText().replace("\r\n\t\t","")), ("course_option",cells[6].getText().replace("\r\n\t\t","")), ("slot",cells[7].getText().replace("\r\n\t\t","")), ("venue",cells[8].getText().replace("\r\n\t\t","")), ("faculty",cells[9].getText().replace("\r\n\t\t",""))})

			#for lab only courses
			else:

				time_table[cells[1].getText().replace("\r\n\t\t","")] = dict({("class_number",cells[0].getText().replace("\r\n\t\t","")), ("course_code",cells[1].getText().replace("\r\n\t\t","")), ("course_title",cells[2].getText().replace("\r\n\t\t","")), ("course_type",cells[3].getText().replace("\r\n\t\t","")), ("ltpjc",cells[4].getText().replace("\n\r\n\t\t\t\t","").replace("\r\n\t\t\t\t\n","")), ("course_mode",cells[5].getText().replace("\r\n\t\t","")), ("course_option",cells[6].getText().replace("\r\n\t\t","")), ("slot",cells[7].getText().replace("\r\n\t\t","")), ("venue",cells[8].getText().replace("\r\n\t\t","")), ("faculty",cells[9].getText().replace("\r\n\t\t",""))})

		#for embedded theory		
		else:

			time_table[cells[3].getText().replace("\r\n\t\t","")] = dict({("class_number",cells[2].getText().replace("\r\n\t\t","")), ("course_code",cells[3].getText().replace("\r\n\t\t","")), ("course_title",cells[4].getText().replace("\r\n\t\t","")), ("course_type",cells[5].getText().replace("\r\n\t\t","")), ("ltpjc",cells[6].getText().replace("\n\r\n\t\t\t\t","").replace("\r\n\t\t\t\t\n","")), ("course_mode",cells[7].getText().replace("\r\n\t\t","")), ("course_option",cells[8].getText().replace("\r\n\t\t","")), ("slot",cells[9].getText().replace("\r\n\t\t","")), ("venue",cells[10].getText().replace("\r\n\t\t","")), ("faculty",cells[11].getText().replace("\r\n\t\t","")), ("registration_status",cells[12].getText().replace("\r\n\t\t",""))})

#function to get details of each page
def details(br):

	details = []
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

	except:
		print "No_table"

	br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })
	
	return details

#fuction to scrape the row data of timetable
def attenScrape(row, br, i, attendance):

	cells = row.findChildren('td')

	br.select_form(nr=i)

	detail = details(br)

	if cells[1].getText().replace("\r\n\t\t","") not in attendance.keys():
		attendance[cells[1].getText().replace("\r\n\t\t","")] = {"registration_date" : cells[5].getText().replace("\r\n\t\t",""), "attended_classes" : cells[6].getText().replace("\r\n\t\t",""), "total_classes" : cells[7].getText().replace("\r\n\t\t",""), "attendance_percentage" : cells[8].getText().replace("\r\n\t\t",""), "details" : detail}
	else:
		attendance[cells[1].getText().replace("\r\n\t\t","")+"_L"] = {"registration_date" : cells[5].getText().replace("\r\n\t\t",""), "attended_classes" : cells[6].getText().replace("\r\n\t\t",""), "total_classes" : cells[7].getText().replace("\r\n\t\t",""), "attendance_percentage" : cells[8].getText().replace("\r\n\t\t",""), "details" : detail}

#fuction to scrape the row data of marks
def mark14Scrape(row, marks):

	rowdata = []
	assessments = []
	cells = row.findAll('td')

	for cell in cells:

		value = cell.getText()
		#print value
		if value is u'' or value is u'N/A':

			rowdata.append('0')
					
		else:

			rowdata.append(value)

	if len(cells) == 18:

		assessments.append({"title" : "CAT-I", "max_marks" : 50, "weightage" : 15, "conducted_on" : "Check Exam Schedule", "status" : rowdata[5], "scored_marks" : rowdata[6], "scored_percentage" : (((float(rowdata[6]))/50)*15) })
		assessments.append({"title" : "CAT-II", "max_marks" : 50, "weightage" : 15, "conducted_on" : "Check Exam Schedule", "status" : rowdata[7], "scored_marks" : rowdata[8], "scored_percentage" : (((float(rowdata[8]))/50)*15) })
		assessments.append({"title" : "Quiz-I", "max_marks" : 5, "weightage" : 5, "conducted_on" : "Check Exam Schedule", "status" : rowdata[9], "scored_marks" : rowdata[10], "scored_percentage" : (((float(rowdata[10]))/5)*100) })
		assessments.append({"title" : "Quiz-II", "max_marks" : 5, "weightage" : 5, "conducted_on" : "Check Exam Schedule", "status" : rowdata[11], "scored_marks" : rowdata[12], "scored_percentage" : (((float(rowdata[12]))/5)*100) })
		assessments.append({"title" : "Quiz-III", "max_marks" : 5, "weightage" : 5, "conducted_on" : "Check Exam Schedule", "status" : rowdata[13], "scored_marks" : rowdata[14], "scored_percentage" : (((float(rowdata[14]))/5)*100) })
		assessments.append({"title" : "Assignment", "max_marks" : 5, "weightage" : 5, "conducted_on" : "Check Exam Schedule", "status" : rowdata[15], "scored_marks" : rowdata[16], "scored_percentage" : (((float(rowdata[16]))/5)*100) })
		#assessments.append({"title" : "FAT", "max_marks" : 100, "weightage" : 50, "conducted_on" : "Check Exam Schedule", "status" : rowdata[18], "scored_marks" : rowdata[19], "scored_percentage" : (((float(rowdata[19]))/100)*50) }) 

		marks[rowdata[2].replace("\r\n\t\t","")] = {"assessments" : assessments, "max_marks" : 220, "max_percentage" : 100, "scored_marks" : (float(rowdata[6])+float(rowdata[8])+float(rowdata[10])+float(rowdata[12])+float(rowdata[14])+float(rowdata[16])), "scored_percentage" : ((((float(rowdata[6]))/50)*15)+(((float(rowdata[8]))/50)*15)+(float(rowdata[10]))+(float(rowdata[12]))+(float(rowdata[14]))+(float(rowdata[16])))}

	elif len(cells) == 6:

		print "no data"

	else:

		assessments.append({"title" : "Lab_cam", "max_marks" : 50, "weightage" : 50, "conducted_on" : "Tentative, set by lab faculty", "status" : rowdata[6], "scored_marks" : rowdata[7], "scored_percentage" : rowdata[7] })
		#assessments.append({"title" : "FAT", "max_marks" : 50, "weightage" : 50, "conducted_on" : "Tentative, set by lab faculty", "status" : rowdata[8], "scored_marks" : rowdata[9], "scored_percentage" : rowdata[9] })
		if rowdata[4] == "Embedded Lab":

			marks[rowdata[2]+"_L"] = {"assessments" : assessments, "max_marks" : 100, "max_percentage" : 100, "scored_marks" : float(rowdata[7]), "scored_percentage" : (float(rowdata[7]))}

		else:

			marks[rowdata[2]] = {"assessments" : assessments, "max_marks" : 100, "max_percentage" : 100, "scored_marks" : float(rowdata[7]), "scored_percentage" : (float(rowdata[7]))}

#fuction to scrape the row data of marks
def mark15Scrape(row, marks):

	rowdata = []
	assessments = []
	cells = row.findAll('td')

	if len(cells) == 10:

		for cell in cells:
			value = cell.getText()

			if value is u'' or value is u'N/A':
				rowdata.append('0')
						
			else:
				rowdata.append(value)


		assessments.append({"title" : "CAT-I", "max_marks" : 50, "weightage" : 10, "conducted_on" : "Check Exam Schedule", "status" : rowdata[5], "scored_marks" : rowdata[6], "scored_percentage" : (((float(rowdata[6]))/50)*10) })
		assessments.append({"title" : "CAT-II", "max_marks" : 50, "weightage" : 10, "conducted_on" : "Check Exam Schedule", "status" : rowdata[7], "scored_marks" : rowdata[8], "scored_percentage" : (((float(rowdata[8]))/50)*10) })
		assessments.append({"title" : "Digital Assignment", "max_marks" : 30, "weightage" : 30, "conducted_on" : "Check Exam Schedule", "scored_marks" : rowdata[9], "scored_percentage" : rowdata[9] })

		marks[rowdata[2].replace("\r\n\t\t","")] = {"assessments" : assessments, "max_marks" : 130, "max_percentage" : 50, "scored_marks" : (float(rowdata[6])+float(rowdata[8])+float(rowdata[9])), "scored_percentage" : ((((float(rowdata[6]))/50)*10)+(((float(rowdata[8]))/50)*10)+(float(rowdata[9])))}

#fuction to scrape the row data of faculty advisor
def facScrape(row, faculty_advisor):

	cells = row.findChildren('td')

	if len(cells) == 1:

		print "nothing"

	else:

		faculty_advisor[cells[0].string.replace("\r\n\t\t","")] = cells[1].string.replace("\r\n\t\t","")

#fuction to scrape the row data of messages
def msgScrape(row, messages):

	cells = row.findChildren('td')
				
	messages.append({"From" : cells[0].string.replace("\r\n\t\t",""), "Course" : cells[1].string.replace("\r\n\t\t",""), "Message" : cells[2].string.replace("\r\n\t\t","").replace("\r\n"," "), "Posted on" : cells[3].string.replace("\r\n\t\t","")})

#fuction to scrape the row data of academic history
def acadScrape(row, academicHistory, status):

	if status == 71:
		cells = row.findChildren('td')
		cells = cells[1:6]

		if cells[2].string.replace("\r\n\t\t","")[0:2] == "ET" or cells[2].string.replace("\r\n\t\t","")[0:2] == "EL" or cells[2].string.replace("\r\n\t\t","")[0:2] == "EP":
			academicHistory["history1"].append(dict({("course_code" , cells[0].string.replace("\r\n\t\t","")) , ("course_title" , cells[1].string.replace("\r\n\t\t","")) , ("course_type" , cells[2].string.replace("\r\n\t\t","")) , ("credit" , "NA") , ("grade" , "NA")}))

		else:
			academicHistory["history1"].append(dict({("course_title" , cells[1].string.replace("\r\n\t\t","")) , ("course_type" , cells[2].string.replace("\r\n\t\t","")) , ("credit" , cells[3].string) , ("grade" , cells[4].string)}))

	elif status == 72:
		cells = row.findChildren('td')

		academicHistory["history2"].append(dict({("credits registered" , cells[0].string.replace("\r\n\t\t","")) , ("credits earned" , cells[1].string.replace("\r\n\t\t","")) , ("cgpa" , cells[2].string.replace("\r\n\t\t","")) , ("rank" , cells[3].string.replace("\r\n\t\t",""))}))

	else:
		cells = row.findChildren('td')

		academicHistory["grdSumm"].append(dict({("S grades" , cells[0].string.replace("\r\n\t\t","")) , ("A grades" , cells[1].string.replace("\r\n\t\t","")) , ("B grades" , cells[2].string.replace("\r\n\t\t","")) , ("C grades" , cells[3].string.replace("\r\n\t\t","")) , ("D grades" , cells[4].string.replace("\r\n\t\t","")) , ("E grades" , cells[5].string.replace("\r\n\t\t","")) , ("F grades" , cells[6].string.replace("\r\n\t\t","")) , ("N grades" , cells[7].string.replace("\r\n\t\t",""))}))

#fuction to scrape the row data of cal marks
def calScrape(br, row, i, calmarks):

	details = []
	cells = row.findChildren('td')

	br.select_form(nr=i)
	i = i+1

	r = br.submit()
	dsoup = BeautifulSoup(r.get_data())
	dtables = dsoup.findChildren('table')

	#if table is present
	try:
		dmyTable = dtables[2]
		
	#if table is absent
	except:

		br.open("https://academics.vit.ac.in/student/cal_da.asp?sem=WS")

		if cells[2].getText().replace("\r\n\t\t","") not in calmarks.keys():

			calmarks[cells[2].getText().replace("\r\n\t\t","")] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : details}

		else:
			if cells[4].getText().replace("\r\n\t\t","") == "Embedded Lab":
				calmarks[cells[2].getText().replace("\r\n\t\t","")+"L"] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : details}

			elif cells[4].getText().replace("\r\n\t\t","") == "Embedded Project":
				calmarks[cells[2].getText().replace("\r\n\t\t","")+"P"] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : details}

	else:

		drows = dmyTable.findChildren(['th','tr'])
		drows = drows[2:-1]

		for drow in drows:

			dcells = drow.findAll('td')
			details.append({"assignment_title" : dcells[1].getText(), "due_date" : dcells[2].getText(),"max_marks" : dcells[3].getText() ,"assignment_status" : dcells[5].getText() if dcells[5].getText() else "NA", "marks_status" : dcells[7].getText() if dcells[7].getText() else "NA", "marks_score" : dcells[8].getText() if dcells[3].getText() else "NA"})

		br.open("https://academics.vit.ac.in/student/cal_da.asp?sem=WS")

		if cells[2].getText().replace("\r\n\t\t","") not in calmarks.keys():

			calmarks[cells[2].getText().replace("\r\n\t\t","")] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : details}

		else:
			if cells[4].getText().replace("\r\n\t\t","") == "Embedded Lab":
				calmarks[cells[2].getText().replace("\r\n\t\t","")+"L"] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : details}

			elif cells[4].getText().replace("\r\n\t\t","") == "Embedded Project":
				calmarks[cells[2].getText().replace("\r\n\t\t","")+"P"] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : details}

	return calmarks

#function to call every function for refresh module
class Refresh():

	def __init__(self, reg_no, pswd):

		#logging into student login
		self.br = login(reg_no,pswd)

		#checking that are we logged in or not
		if self.br.geturl() == ("https://academics.vit.ac.in/student/stud_home.asp") or self.br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
			print "SUCCESS"

		else :
			print "FAIL"

	#function to get the timetable
	def getTimetable(self, time_table):

		#opening time table page
		self.br.open("https://academics.vit.ac.in/student/timetable_ws.asp")
		response = self.br.open("https://academics.vit.ac.in/student/timetable_ws.asp")

		#getting the soup
		soup = BeautifulSoup(response.get_data())

		#extracting tables from soup
		tables = soup.findAll('table')


		#getting required table
		myTable = tables[1]
		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]


		#extracting data
		for row in rows:

			#creating thread for each row
			thrd = myThread(row, 1, time_table)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)
		
		#waiting for each thread to complete
		for t in threads:
			t.join()

		#returning the attendance
		return time_table

	#function to get the attendance
	def getAttendance(self, attendance):

		#opening the attendance page
		self.br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })
		response = self.br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findChildren('table')
		myTable = tables[3]
		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]
		i = 1


		#extracting data
		for row in rows:

			#creating thread for each row
			thrd = myThread(row, 2, attendance, i, self.br)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)

			i = i+1 
		
		#waiting for each thread to end
		for t in threads:
			t.join()

		return attendance

	#function to get the marks
	def getMarks14(self, marks):

		#opening marks page
		self.br.open("https://academics.vit.ac.in/student/marks.asp?sem=WS")
		response = self.br.open("https://academics.vit.ac.in/student/marks.asp?sem=WS")

		#getting the soup
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findAll('table')
		myTable = tables[1]


		#initialising some required variables
		rows = myTable.findChildren(['th','tr'])
		rows = rows[2:]

		#extracting data
		for row in rows:

			#creating thread for each row
			thrd = myThread(row, 3, marks)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)

		try:

			myTable = tables[2]

		except IndexError:

			myTable = 'null'
			return {"status" : "Success" , "marks" : marks}

		rows = myTable.findAll(['th','tr'])
		rows = rows[1:]
		rowcount = 0
		assessments = []

		for row in rows:

			rowcount += 1
			rowdata = []
			cells = row.findAll('td')

			for cell in cells:

				value = cell.string

				if value is u'' or value is u'N/A':

					rowdata.append('0')

				else:

					rowdata.append(value)

			if len(cells) == 11:
				
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

			if rowcount == 7:

				rowcount = 0
				marks[key] = {"assessments" : assessments}
				assessments = []

		#waiting for each thread to complete
		for t in threads:
			t.join()

		#returning the marks
		return marks

	#function to get the marks
	def getMarks15(self, marks):

		#opening marks page
		self.br.open("https://academics.vit.ac.in/student/marks.asp?sem=WS")
		response = self.br.open("https://academics.vit.ac.in/student/marks.asp?sem=WS")

		#getting the soup
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findAll('table')
		myTable = tables[1]

		#initialising some required variables
		rows = myTable.findChildren(['th','tr'])
		rows = rows[2:]


		#extracting data
		for row in rows:

			#creating thread for each row
			thrd = myThread(row, 4, marks)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)

		#waiting for each thread to complete
		for t in threads:
			t.join()

		#returning marks
		return marks

	#function to get the exam schedule
	def getExamschedule(self, examSchedule):

		#inmporting Queue
		import Queue as q

		#opening exam schedule page
		self.br.open("https://academics.vit.ac.in/student/exam_schedule.asp?sem=WS")
		response = self.br.open("https://academics.vit.ac.in/student/exam_schedule.asp?sem=WS")

		#getting the soup
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findAll('table')

		#if table is absent
		try:

			myTable = tables[1]

		except IndexError:

			myTable = 'null'
			examSchedule = {"cat1" : {} , "cat2" : {} , "term_end" : {}}

		else:

			#extracting the rows
			rows = myTable.findChildren(['th','tr'])
			rows = rows[2:]

			#initialising some required variables
			schedule = {}

			#holding the cat1, cat2, termend schedules in queue
			p = q.Queue()
			
			#extracting data
			for row in rows:

				cells = row.findChildren('td')

				if len(cells) != 1:

					schedule[cells[1].string.replace("\r\n\t\t","")] = dict({("crTitle",cells[2].string.replace("\r\n\t\t","")), ("slot",cells[4].string.replace("\r\n\t\t","")), ("date",cells[5].string.replace("\r\n\t\t","")), ("day",cells[6].string.replace("\r\n\t\t","")), ("session",cells[7].string.replace("\r\n\t\t","")), ("time",cells[8].string.replace("\r\n\t\t",""))})

				#for changing to the different exam
				elif len(cells) == 1:

					p.put(schedule)
					schedule = {}
					continue

			examSchedule["cat1"] = p.get()

			if p.empty():

				examSchedule["cat2"] = {}

			else:

				examSchedule["cat2"] = p.get()

			if p.empty():

				examSchedule["termend"] = {}

			else:

				examSchedule["termend"] = p.get()

		return examSchedule

	#function to get the faculty advisor datails
	def getFacultyAdvisor(self, faculty_advisor):

		#opening faculty advisor details page
		self.br.open("https://academics.vit.ac.in/student/faculty_advisor_view.asp")
		response = self.br.open("https://academics.vit.ac.in/student/faculty_advisor_view.asp")

		#getting the soup
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findChildren('table')
		myTable = tables[1]
		rows = myTable.findChildren(['th','tr'])

		#extracting data
		for row in rows:

			#creating thread for each row
			thrd = myThread(row, 5, faculty_advisor)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)
		
		#waiting for each thread to complete
		for t in threads:
			t.join()

		#returning faculty_advisor
		return faculty_advisor

	#function to get the messages
	def getMessages(self, messages):

		#opening the meesages page
		self.br.open("https://academics.vit.ac.in/student/class_message_view.asp?sem=WS")
		response = self.br.open("https://academics.vit.ac.in/student/class_message_view.asp?sem=WS")

		#getting the soup
		soup = BeautifulSoup(response.get_data())

		#checking if there is a mesage or not
		try:

			tables = soup.findAll('table')
			myTable = tables[1]
			rows = myTable.findChildren(['th','tr'])

			rows = rows[1:]

			for row in rows[:-1]:

				#creating thread for each row
				thrd = myThread(row, 6, messages)
				#starting the thread
				thrd.start()

				#appending into thread list
				threads.append(thrd)
		
			#waiting for each thread to complete
			for t in threads:
				t.join()


		except:

			print "nothing"

		#returning messages
		return messages

	#function to get the academic history
	def getAcademicHistory(self, academicHistory):

		#opening the academic history page
		self.br.open("https://academics.vit.ac.in/student/student_history.asp")
		response = self.br.open("https://academics.vit.ac.in/student/student_history.asp")

		#getting the soup
		soup = BeautifulSoup(response.get_data())

		tables = soup.findAll('table')

		#getting the required table
		myTable = tables[2]

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#extracting data
		for row in rows:

			#creating thread for each row
			thrd = myThread(row,71, academicHistory)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)

		myTable = tables[3]

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#extracting data
		for row in rows:

			#creating thread for each row
			thrd = myThread(row,72, academicHistory)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)

		myTable = tables[4]

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		#extracting data
		for row in rows:

			#creating thread for each row
			thrd = myThread(row,73, academicHistory)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)

		#waiting for each thread to complete
		for t in threads:
			t.join()

		return academicHistory

	#function to get the cal marks
	def getCalMarks(self, calmarks):

		#opening the cal marks page
		self.br.open("https://academics.vit.ac.in/student/cal_da.asp?sem=WS")
		response = self.br.open("https://academics.vit.ac.in/student/cal_da.asp?sem=WS")

		#getting the soup
		soup = BeautifulSoup(response.get_data())

		#getting the required table
		myTable = soup.findAll('table')[1]

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		i = 0

		#extracting the table
		for row in rows:

			#creating thread for each row
			thrd = myThread(row, 8, calmarks, i, self.br)

			i= i+1
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)

		#waiting for each thread to complete
		for t in threads:
			t.join()

		return calmarks

#function to join every module into a json
def refresh(reg_no = "", pswd = ""):

	refrsh = Refresh(reg_no, pswd)

	#initializing required varibles
	marks = {}
	attendance = {}
	time_table = {}
	examSchedule = {}
	faculty_advisor = {}
	messages = []
	calmarks = {}
	academicHistory = {"history1" : [], "history2" : [], "grdSumm" : []}

	#creating the individual threads for each spotlight
	if int(reg_no[0:2]) > 14:
		marksThread = threading.Thread(target = refrsh.getMarks15(marks))
		calThread = threading.Thread(target = refrsh.getCalMarks(calmarks))
	else:
		marksThread = threading.Thread(target = refrsh.getMarks14(marks))
		calThread = None

	timetableThread = threading.Thread(target = refrsh.getTimetable(time_table))
	attendanceThread = threading.Thread(target = refrsh.getAttendance(attendance))
	examscheduleThread = threading.Thread(target = refrsh.getExamschedule(examSchedule))
	facultyadvisorThread = threading.Thread(target = refrsh.getFacultyAdvisor(faculty_advisor))
	academichistoryThread = threading.Thread(target = refrsh.getAcademicHistory(academicHistory))
	messagesThread = threading.Thread(target = refrsh.getMessages(messages))


	#starting the threads
	marksThread.start()
	timetableThread.start()
	attendanceThread.start()
	examscheduleThread.start()
	facultyadvisorThread.start()
	academichistoryThread.start()
	messagesThread.start()
	if calThread:
		calThread.start()

	#waiting for the threads to complete
	marksThread.join()
	timetableThread.join()
	attendanceThread.join()
	examscheduleThread.join()
	facultyadvisorThread.join()
	academichistoryThread.join()
	messagesThread.join()
	if calThread:
		calThread.join()

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

	return {"reg_no" : reg_no, "campus" : "vellore", "semester" : "WS", "courses" : data, "exam_schedule" : examSchedule, "CAL_marks" : calmarks, "faculty_advisor" : faculty_advisor, "academic_history" : academicHistory, "messages" : messages}
