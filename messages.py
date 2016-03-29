#importing the required modules
from login import login
from bs4 import BeautifulSoup
import threading

#initialising some required variables
messages = []
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
				
	messages.append({"From" : cells[0].string.replace("\r\n\t\t",""), "Course" : cells[1].string.replace("\r\n\t\t",""), "Message" : cells[2].string.replace("\r\n\t\t","").replace("\r\n"," "), "Posted on" : cells[3].string.replace("\r\n\t\t","")})

#function to return the scraped messages
def getMessages(reg_no = "", pwd = ""):

	#logging in
	br = login(reg_no,pwd)

	#checking if logged in or not
	if br.geturl() == ("https://academics.vit.ac.in/student/stud_home.asp") or br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		#opening the meesages page
		br.open("https://academics.vit.ac.in/student/class_message_view.asp?sem=WS")
		response = br.open("https://academics.vit.ac.in/student/class_message_view.asp?sem=WS")

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
				thrd = myThread(row)
				#starting the thread
				thrd.start()

				#appending into thread list
				threads.append(thrd)
		
			#waiting for each thread to complete
			for t in threads:
				t.join()

		except:

			print "nothing"

		return {"status" : "Success", "Messages" : messages}

	else :
		print "FAIL"
		return {"Status" : "Failure", "Reason" : "Wrong Captcha"}
