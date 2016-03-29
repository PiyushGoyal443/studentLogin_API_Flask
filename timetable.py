#importing the required modules
from login import login
from bs4 import BeautifulSoup
import threading

#initialising some required variables
time_table = {}
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

#function to return the scraped time table
def getTimetable(reg_no = "", pswd = ""):

	#logging in
	br = login(reg_no,pswd)

	#checking that are we logged in or not
	if br.geturl() == ("https://academics.vit.ac.in/student/stud_home.asp") or br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		#opening time table page
		br.open("https://academics.vit.ac.in/student/timetable_ws.asp")
		response = br.open("https://academics.vit.ac.in/student/timetable_ws.asp")

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
			thrd = myThread(row)
			#starting the thread
			thrd.start()

			#appending into thread list
			threads.append(thrd)
		
		#waiting for each thread to complete
		for t in threads:
			t.join()

		#returning the attendance
		return {"status" : "Success" , "time_table" : time_table}

	#failure due to wrong captcha
	else :
		print "FAIL"
		return {"Status" : "Failure", "Reason" : "Wrong Captcha"}
