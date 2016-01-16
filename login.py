def login(reg_no="",pwd=""):

	from bs4 import BeautifulSoup
	from CaptchaParser import CaptchaParser
	from PIL import Image
	import json, mechanize, datetime


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
	print img['src']

	#retrieving captcha image
	br.retrieve("https://academics.vit.ac.in/student/"+img['src'], "captcha_student.bmp")
	print "captcha retrieved"
	img = Image.open("captcha_student.bmp")
	parser = CaptchaParser()
	captcha = parser.getCaptcha(img)
	print str(captcha)

	#fill form
	br["regno"] = str(reg_no)
	br["passwd"] = str(pwd)
	br["vrfcd"] = str(captcha)

	#submitting the values and signing in
	br.method = "POST"
	br.submit()
	return br
