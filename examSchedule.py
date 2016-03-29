from login import login
from bs4 import BeautifulSoup

#to get the exam schedule
def getExamSchedule(reg_no = "", pwd = ""):

	#loging in
	br = login(reg_no,pwd)

	#checking that are we logged in or not
	if br.geturl() == ("https://academics.vit.ac.in/student/stud_home.asp") or br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		#inmporting Queue
		import Queue as q

		#opening exam schedule page
		br.open("https://academics.vit.ac.in/student/exam_schedule.asp?sem=WS")
		response = br.open("https://academics.vit.ac.in/student/exam_schedule.asp?sem=WS")

		#initializing required variables
		examSchedule = {}

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

			#initialising some required variables for getting schedule for CAT-1
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

		return {"status" : "Success" , "Exam Schedule" : examSchedule}

	else :
		print "FAIL"
		return {"Status" : "Failure", "Reason" : "Wrong Captcha"}