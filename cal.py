from login import login
from bs4 import BeautifulSoup

def calmarks(reg_no = "", pwd = ""):
	br = login(reg_no,pwd)

	print br.geturl()

	#checking that are we logged in or not

	if br.geturl() == ("https://academics.vit.ac.in/student/stud_home.asp") or br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		br.open("https://academics.vit.ac.in/student/cal_da.asp?sem=FS")
		response = br.open("https://academics.vit.ac.in/student/cal_da.asp?sem=FS")

		soup = BeautifulSoup(response.get_data())
		myTable = soup.findAll('table')[1]

		rows = myTable.findChildren(['th','tr'])
		rows = rows[1:]

		calmarks = {}
		i = 0

		for row in rows:

			details = []
			cells = row.findChildren('td')

			br.select_form(nr=i)
			i = i+1

			r = br.submit()
			dsoup = BeautifulSoup(r.get_data())
			dtables = dsoup.findChildren('table')

			print "11\n"

			try:
				dmyTable = dtables[2]
				drows = dmyTable.findChildren(['th','tr'])
				drows = drows[2:]

				for drow in drows:

					dcells = drow.findChildren('td')

					details.append({"assignment_title" : dcells[1].getText(), "due_date" : dcells[2].getText(),"max_marks" : dcells[3].getText(),"assignment_status" : dcells[5].getText(), "assignment_file" : dcells[6].getText(), "marks_status" : dcells[7].getText(), "marks_score" : dcells[8].getText()})

				br.open("https://academics.vit.ac.in/student/cal_da.asp?sem=FS")

				if cells[2].getText().replace("\r\n\t\t","") not in calmarks.keys():

					calmarks[cells[2].getText().replace("\r\n\t\t","")] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : details}

				else:
					if cells[4].getText().replace("\r\n\t\t","") == "Embedded Lab":
						calmarks[cells[2].getText().replace("\r\n\t\t","")+"L"] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : details}

					elif cells[4].getText().replace("\r\n\t\t","") == "Embedded Project":
						calmarks[cells[2].getText().replace("\r\n\t\t","")+"P"] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : details}

			except:

				br.open("https://academics.vit.ac.in/student/cal_da.asp?sem=FS")

				if cells[2].getText().replace("\r\n\t\t","") not in calmarks.keys():

					calmarks[cells[2].getText().replace("\r\n\t\t","")] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : details}

				else:
					if cells[4].getText().replace("\r\n\t\t","") == "Embedded Lab":
						calmarks[cells[2].getText().replace("\r\n\t\t","")+"L"] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : {}}

					elif cells[4].getText().replace("\r\n\t\t","") == "Embedded Project":
						calmarks[cells[2].getText().replace("\r\n\t\t","")+"P"] = {"course_type" : cells[4].getText().replace("\r\n\t\t",""), "faculty" : cells[5].getText().replace("\r\n\t\t",""), "details" : {}}
		
		return {"status" : "Success" , "attendance_det" : attendance}

	else :
		print "FAIL"
		return {"status" : "Failure"}