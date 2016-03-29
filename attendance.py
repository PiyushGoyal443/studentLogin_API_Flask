from login import login
from bs4 import BeautifulSoup
import datetime, pytz
import threading

#initialising some required variables
months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
attendance = {}
details = []
threadLock = threading.Lock()
threads = []

#getting today's date
tz = pytz.timezone('Asia/Kolkata')
now = datetime.datetime.now(tz)
today = str(now.day) + "-" + months[now.month] + "-" + str(now.year)


class myThread(threading.Thread):

	def __init__(self, br, row, i):
		threading.Thread.__init__(self)
		self.br = br
		self.row = row
		self.i = i

	def run(self):

		threadLock.acquire()
		scrape(self.br, self.row, self.i)
		threadLock.release()

def scrape(br, row, i):

	cells = row.findChildren('td')

	br.select_form(nr=i)

	detail = details(br)

	if cells[1].getText().replace("\r\n\t\t","") not in attendance.keys():
		attendance[cells[1].getText().replace("\r\n\t\t","")] = {"registration_date" : cells[5].getText().replace("\r\n\t\t",""), "attended_classes" : cells[6].getText().replace("\r\n\t\t",""), "total_classes" : cells[7].getText().replace("\r\n\t\t",""), "attendance_percentage" : cells[8].getText().replace("\r\n\t\t",""), "details" : detail}
	else:
		attendance[cells[1].getText().replace("\r\n\t\t","")+"_L"] = {"registration_date" : cells[5].getText().replace("\r\n\t\t",""), "attended_classes" : cells[6].getText().replace("\r\n\t\t",""), "total_classes" : cells[7].getText().replace("\r\n\t\t",""), "attendance_percentage" : cells[8].getText().replace("\r\n\t\t",""), "details" : detail}

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

def getAttendance(reg_no = "", pwd = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	if br.geturl() == ("https://academics.vit.ac.in/student/stud_home.asp") or br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		#opening the attendance page
		br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })
		response = br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=WS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })
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
			thrd = myThread(br, row, i)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)

			i = i+1 
		
		#waiting for each thread to end
		for t in threads:
			t.join()

		return {"status" : "Success" , "attendance_det" : attendance}

	else :
		print "FAIL"
		return {"Status" : "Failure", "Reason" : "Wrong Captcha"}