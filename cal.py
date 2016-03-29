from login import login
from bs4 import BeautifulSoup
import threading

#initialising some required variables
threadLock = threading.Lock()
threads = []


class myThread(threading.Thread):

	def __init__(self, br, row, i, calmarks):
		threading.Thread.__init__(self)
		self.br = br
		self.row = row
		self.i = i
		self.calmarks = calmarks

	def run(self):

		threadLock.acquire()
		scrape(self.br, self.row, self.i, self.calmarks)
		threadLock.release()

def scrape(br, row, i, calmarks):

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


def getCalmarks(reg_no = "", pwd = ""):

	#logging in
	br = login(reg_no,pwd)

	#checking that are we logged in or not
	if br.geturl() == ("https://academics.vit.ac.in/student/stud_home.asp") or br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		#opening the cal marks page
		br.open("https://academics.vit.ac.in/student/cal_da.asp?sem=WS")
		response = br.open("https://academics.vit.ac.in/student/cal_da.asp?sem=WS")

		#getting the soup
		soup = BeautifulSoup(response.get_data())

		#getting the required table
		print len(soup.findAll(table))
		myTable = soup.findAll('table')[1]

		#initialising some required variables
		calmarks = {}

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		calmarks = {}
		i = 0

		#extracting the table
		for row in rows:

			#creating thread for each row
			thrd = myThread(br, row, i, calmarks)
			i= i+1
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)

		#waiting for each thread to complete
		for t in threads:
			t.join()

		return {"status" : "Success" , "CAL_marks" : calmarks}

	else :
		print "FAIL"
		return {"Status" : "Failure", "Reason" : "Wrong Captcha"}