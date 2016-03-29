from login import login
from bs4 import BeautifulSoup
import threading

#initialising some required variables
marks = {}
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

#fuction to scrape the row data of CBL
def scrape(row):

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

#function to return the scraped marks
def getMarks14(reg_no = "", pwd = ""):

	#logging in
	br = login(reg_no,pwd)

	#checking that are we logged in or not
	if br.geturl() == ("https://academics.vit.ac.in/student/stud_home.asp") or br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		#opening marks page
		br.open("https://academics.vit.ac.in/student/marks.asp?sem=WS")
		response = br.open("https://academics.vit.ac.in/student/marks.asp?sem=WS")

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
			thrd = myThread(row)
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
				print "yes"
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
			
		return {"status" : "Success" , "marks" : marks}

	else :

		print "FAIL"
		return {"Status" : "Failure", "Reason" : "Wrong Captcha"}
