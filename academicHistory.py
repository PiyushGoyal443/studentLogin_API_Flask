from login import login
from bs4 import BeautifulSoup
import threading

#initialising some required variables
history1 = []
history2 = []
grdSumm = []
threadLock = threading.Lock()
threads = []

#overloading thread init and run function
class myThread(threading.Thread):

	#overloading the __init__ function
	def __init__(self, row, status):
		threading.Thread.__init__(self)
		self.row = row
		self.status = status

	#overloading the run function
	def run(self):
		
		threadLock.acquire()
		scrape(self.row, self.status)
		threadLock.release()
		
#fuction to scrape the row data
def scrape(row, status):

	if status == 1:
		cells = row.findChildren('td')
		cells = cells[1:6]

		if cells[2].string.replace("\r\n\t\t","")[0:2] == "ET" or cells[2].string.replace("\r\n\t\t","")[0:2] == "EL" or cells[2].string.replace("\r\n\t\t","")[0:2] == "EP":
			history1.append(dict({("course_code" , cells[0].string.replace("\r\n\t\t","")) , ("course_title" , cells[1].string.replace("\r\n\t\t","")) , ("course_type" , cells[2].string.replace("\r\n\t\t","")) , ("credit" , "NA") , ("grade" , "NA")}))

		else:
			history1.append(dict({("course_title" , cells[1].string.replace("\r\n\t\t","")) , ("course_type" , cells[2].string.replace("\r\n\t\t","")) , ("credit" , cells[3].string) , ("grade" , cells[4].string)}))

	elif status == 2:
		cells = row.findChildren('td')

		history2.append(dict({("credits registered" , cells[0].string.replace("\r\n\t\t","")) , ("credits earned" , cells[1].string.replace("\r\n\t\t","")) , ("cgpa" , cells[2].string.replace("\r\n\t\t","")) , ("rank" , cells[3].string.replace("\r\n\t\t",""))}))

	else:
		cells = row.findChildren('td')

		grdSumm.append(dict({("S grades" , cells[0].string.replace("\r\n\t\t","")) , ("A grades" , cells[1].string.replace("\r\n\t\t","")) , ("B grades" , cells[2].string.replace("\r\n\t\t","")) , ("C grades" , cells[3].string.replace("\r\n\t\t","")) , ("D grades" , cells[4].string.replace("\r\n\t\t","")) , ("E grades" , cells[5].string.replace("\r\n\t\t","")) , ("F grades" , cells[6].string.replace("\r\n\t\t","")) , ("N grades" , cells[7].string.replace("\r\n\t\t",""))}))

#for getting the academic history
def getAcademicHistory(reg_no = "", pwd = ""):

	#logging in
	br = login(reg_no,pwd)

	#checking that are we logged in or not
	if br.geturl() == ("https://academics.vit.ac.in/student/stud_home.asp") or br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		#opening the academic history page
		br.open("https://academics.vit.ac.in/student/student_history.asp")
		response = br.open("https://academics.vit.ac.in/student/student_history.asp")

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
			thrd = myThread(row,1)
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
			thrd = myThread(row,2)
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
			thrd = myThread(row,3)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)

		#waiting for each thread to complete
		for t in threads:
			t.join()

		return {"status" : "Success" , "history 1" : history1 , "history 2" : history2 , "grade summary" : grdSumm}

	else :
		print "FAIL"
		return {"Status" : "Failure", "Reason" : "Wrong Captcha"}