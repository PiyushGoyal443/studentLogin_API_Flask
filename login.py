def login(reg_no="",pwd=""):

	#importing the required modules
	from bs4 import BeautifulSoup
	from CaptchaParser import CaptchaParser
	from PIL import Image
	import mechanize
	import os

    #handeling browser and browser initialisation
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)

	#opening website
	response = br.open("https://academics.vit.ac.in/student/stud_login.asp")
	#print br.geturl()

	#selecting the login form
	br.select_form("stud_login")

	#extracting captcha url
	soup = BeautifulSoup(response.get_data())
	img = soup.find('img', id='imgCaptcha')
	#print img['src']

	#retrieving captcha image
	br.retrieve("https://academics.vit.ac.in/student/"+img['src'], reg_no+".bmp")
	print "captcha retrieved"

	#opening the image
	img = Image.open(reg_no+".bmp")

	#parsing the image and getting its string value
	parser = CaptchaParser()
	captcha = parser.getCaptcha(img)
	print str(captcha)

	os.remove(reg_no+".bmp")

	#filling form
	br["regno"] = str(reg_no)
	br["passwd"] = str(pwd)
	br["vrfcd"] = str(captcha)

	#submitting the values and signing in
	br.method = "POST"
	response = br.submit()

	#during the time of rivera
	try:

		br.open("https://academics.vit.ac.in/student/stud_home.asp")
		br.select_form("stud_riviera")
		br.submit(label = "Skip Now")
		print "Login_Sucess"

	#for normal login
	except:

		print "Login_Sucess"
		
	return br
