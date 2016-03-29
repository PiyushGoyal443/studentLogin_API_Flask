#importing the required modules
from login import login
from bs4 import BeautifulSoup
import threading

#importing the mechanical browser
import mechanize

#initializing required variables
acad = []
coe = []
research = []

#spotlight class
class Spotlight():

	#constructor for browser initialization
	def __init__(self):

		self.br = mechanize.Browser()
		self.br.set_handle_robots(False)
		self.br.set_handle_equiv(True)
		self.br.set_handle_gzip(True)
		self.br.set_handle_redirect(True)
		self.br.set_handle_referer(True)

	#for getting academic spotlight
	def acadSpotlight(self):

		#opening the academics spotlight page
		self.br.open("https://academics.vit.ac.in/include_spotlight_part01.asp")
		response = self.br.open("https://academics.vit.ac.in/include_spotlight_part01.asp")

		#getting the soup
		soup = BeautifulSoup(response.get_data())
		
		tables = soup.findAll('table')

		#getting the required table
		myTable = tables[0]

		rows = myTable.findChildren(['th','tr'])

		#etracting the data
		for row in rows:

			text = row.find('td').string

			if row.find('a') is not None:

				link = "https://academics.vit.ac.in/"+row.find('a')['href']

			else:

				link = "No_link"

			if text == None:

				print "no text"

			else:

				acad.append({"text": text, "url" : link})

	#for getting COE spotlight
	def coeSpotlight(self):

		#opening the COE soptling page
		self.br.open("https://academics.vit.ac.in/include_spotlight_part02.asp")
		response = self.br.open("https://academics.vit.ac.in/include_spotlight_part02.asp")

		#getting the soup
		soup = BeautifulSoup(response.get_data())
		
		#if tabel is present
		try:

			tables = soup.findAll('table')
			myTable = tables[0]

			rows = myTable.findChildren(['th','tr'])

			#extracting the data
			for row in rows:

				text = row.find('td').string

				if row.find('a') is not None:

					link = "https://academics.vit.ac.in/"+row.find('a')['href'] 

				else:

					link = "No_link"

				if text == None:

					print "no text"

				else:
					coe.append({"text": text, "url" : link})

		#if table is absent
		except IndexError:

			myTable = None

	#for getting Research spotlight
	def researchSpotlight(self):

		#opening the research spotlight
		self.br.open("https://academics.vit.ac.in/include_spotlight_part03.asp")
		response = self.br.open("https://academics.vit.ac.in/include_spotlight_part03.asp")

		#getting the soup
		soup = BeautifulSoup(response.get_data())

		#if table is present
		try:		

			tables = soup.findAll('table')
			myTable = tables[0]

			rows = myTable.findChildren(['th','tr'])

			for row in rows:

				text = row.find('td').string

				if row.find('a') is not None:

					link = "https://academics.vit.ac.in/"+row.find('a')['href'] 

				else:

					link = "No_link"

				if text != None:

					research.append({"text": text, "url" : link})

		#if table is absent
		except IndexError:

			myTable = None

#function to return the scraped spotlight
def getSpotlight():

	#creating the instance of Spotlight
	spotlight = Spotlight()

	#creating the individual threads for each spotlight
	acadThread = threading.Thread(target = spotlight.acadSpotlight())
	coeThread = threading.Thread(target = spotlight.coeSpotlight())
	researchThread = threading.Thread(target = spotlight.researchSpotlight())

	#starting the threads
	acadThread.start()
	coeThread.start()
	researchThread.start()

	#waiting for the threads to complete
	acadThread.join()
	coeThread.join()
	researchThread.join()

	return {"status" : "Success" , "academics" : acad, "COE" : coe , "research" : research}