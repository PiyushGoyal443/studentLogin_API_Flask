from login import login
from bs4 import BeautifulSoup

def get_courses(reg_no = "", pwd = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		br.open("https://academics.vit.ac.in/student/coursepage_view.asp?sem=FS")
		response = br.open("https://academics.vit.ac.in/student/coursepage_view.asp?sem=FS")
		soup = BeautifulSoup(response.get_data())

		br.select_form("coursepage_view")

		#print br.read()
		forms = soup.findAll("select")

		#print forms[0]
		options = forms[0].findAll("option")
		options = options[1:]
		course= {}

		for o in options:
			course[o['value']] = o.getText()

		return {"status" : "Success_level_1" , "courses" : course}

	else :
		print "FAIL"
		return {"status" : "Failure_level_1"}

#########################################################################################################################################################

def get_slot(reg_no = "", pwd = "", coursekey = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		br.open("https://academics.vit.ac.in/student/coursepage_view.asp?sem=FS&crs=%(key)s&slt=&fac=" % {"key" : coursekey})
		response = br.open("https://academics.vit.ac.in/student/coursepage_view.asp?sem=FS&crs=%(key)s&slt=&fac=" % {"key" : coursekey})
		soup = BeautifulSoup(response.get_data())

		br.select_form("coursepage_view")

		#print br.read()
		forms = soup.findAll("select")

		#print forms[1]
		options = forms[1].findAll("option")
		options = options[1:]
		slot = {}

		for o in options:
			slot[o['value']] = o.getText()

		return {"status" : "Success_level_2" , "slot" : slot}

	else :
		print "FAIL"
		return {"status" : "Failure_level_2"}

#########################################################################################################################################################

def get_faculty(reg_no = "", pwd = "", coursekey = "", slotkey = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		br.open("https://academics.vit.ac.in/student/coursepage_view.asp?sem=FS&crs=%(ckey)s&slt=%(skey)s&fac=" % {"ckey" : coursekey, "skey": slotkey})
		response = br.open("https://academics.vit.ac.in/student/coursepage_view.asp?sem=FS&crs=%(key)s&slt=%(skey)s&fac=" % {"key" : coursekey, "skey" : slotkey})
		soup = BeautifulSoup(response.get_data())
		
		br.select_form("coursepage_view")

		#print br.read()
		forms = soup.findAll("select")

		#print forms[1]
		options = forms[2].findAll("option")
		options = options[1:]
		
		slot = {}

		for o in options:
			slot[o['value']] = o.getText()

		return {"status" : "Success_level_2" , "slot" : slot}

	else :
		print "FAIL"
		return {"status" : "Failure_level_2"}

#########################################################################################################################################################

def get_data(reg_no = "", pwd = "", coursekey = "", slotkey = "", fackey = ""):

	br = login(reg_no,pwd)

	print br.geturl()

	if br.geturl() == ("https://academics.vit.ac.in/student/home.asp"):
		print "SUCCESS"

		def select_form(form):
			return form.attrs.get('action', None) == 'coursepage_view3.asp'

		br.open("https://academics.vit.ac.in/student/coursepage_view.asp?sem=FS&crs=%(ckey)s&slt=%(skey)s&fac=%(fkey)s" % {"ckey" : coursekey, "skey": slotkey, "fkey" : fackey})
		response = br.open("https://academics.vit.ac.in/student/coursepage_view.asp?sem=FS&crs=%(key)s&slt=%(skey)s&fac=%(fkey)s" % {"key" : coursekey, "skey" : slotkey, "fkey" : fackey})
		soup = BeautifulSoup(response.get_data())

		#form = soup.find("form",)
		br.select_form(predicate = select_form)
		res = br.submit()

		print br.geturl()

		soup = BeautifulSoup(res.get_data())

		#extracting data
		links = soup.findAll('a')
		href = []
		for l in links:
			href.append(l['href'])

		return {"status" : "Success_finally" , "uploads" : href}

	else :
		print "FAIL"
		return {"status" : "Failure_end"}
