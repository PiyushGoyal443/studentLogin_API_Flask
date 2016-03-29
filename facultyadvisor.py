#importing the required modules
from login import login
from bs4 import BeautifulSoup
import threading

#initialising some required variables
faculty_advisor = {}
threadLock = threading.Lock()
threads = []

#overloading thread init and run function
class myThread(threading.Thread):

	#overloading the __init__ function
	def __init__(self, row):
		threading.Thread.__init__(self)
		self.row = row

	#overloading the run function
	def run(self):
		
		threadLock.acquire()
		scrape(self.row)
		threadLock.release()
		
#fuction to scrape the row data
def scrape(row):

	cells = row.findChildren('td')

	if len(cells) == 1:

		print "nothing"

	else:

		faculty_advisor[cells[0].string.replace("\r\n\t\t","")] = cells[1].string.replace("\r\n\t\t","")

#function to return the scraped faculty advisor details
def getFacultyAdvisor(reg_no = "", pwd = ""):

	#logging in
	br = login(reg_no,pwd)

	#checking that are we logged in or not
	if br.geturl() == ("https://academics.vit.ac.in/student/stud_home.asp") or br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		#opening faculty advisor details page
		br.open("https://academics.vit.ac.in/student/faculty_advisor_view.asp")
		response = br.open("https://academics.vit.ac.in/student/faculty_advisor_view.asp")

		#getting the soup
		soup = BeautifulSoup(response.get_data())

		#extracting tables
		tables = soup.findChildren('table')
		myTable = tables[1]
		rows = myTable.findChildren(['th','tr'])

		#extracting data
		for row in rows:

			#creating thread for each row
			thrd = myThread(row)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)
		
		#waiting for each thread to complete
		for t in threads:
			t.join()

		return {"status" : "Success" , "faculty_det" : faculty_advisor}

	else :
		print "FAIL"
		return {"Status" : "Failure", "Reason" : "Wrong Captcha"}
