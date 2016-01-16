import mechanize, json, datetime 
from bs4 import BeautifulSoup
from CaptchaParser import CaptchaParser
from PIL import Image
from collections import defaultdict
import time
from flask import jsonify
    
#browser initialise
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)

#open website
response = br.open("https://academics.vit.ac.in/student/stud_login.asp")
print br.geturl()
    
#select form
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
reg_no="14BCE0104"    #fill ur data
pwd="gogogogogoogle4"
br["regno"] = str(reg_no)
br["passwd"] = str(pwd)
br["vrfcd"] = str(captcha)
br.method = "POST"

res=br.submit().read()
print br.geturl()
if br.geturl()==("https://academics.vit.ac.in/student/home.asp"):
    print "SUCCESS"

    #getting today's date
    today = time.strftime("%d-%m-%Y")

    #opening the attendance page
    br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=FS")
    response = br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=FS")
    soup = BeautifulSoup(response.get_data())
    
    #selecting the form
    #br.select_form("attn_report")

    #setting the current date
    #br["to_date"] = str(today)

    #br.method = "POST"
    #br.submit()

    br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=FS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })
    response = br.open("https://academics.vit.ac.in/student/attn_report.asp?sem=FS&fmdt=09-Jul-2015&todt=%(to_date)s" % {"to_date" : today })
    soup = BeautifulSoup(response.get_data())

    #extracting tables
    tables = soup.findAll('table')
    myTable = tables[3]
    rows = myTable.findChildren(['th','tr'])
    #initialising some required variables
    attndet = {}

    #extracting data
    for row in rows:

        print row
        """rowdata = {}
        cells = row.findChildren('td')
        j = 0
        print cells
        for cell in cells:

            value = cell.string
            print value
            rowdata[j] = value
            j = j+1

        attndet[rowdata[1].replace("\r\n\t\t","")] = list({})
        i = i+1
    return {"status" : "Success" , "attendance_det" : attndet}"""
