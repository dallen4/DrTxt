import urllib2
import string
import json
import time
#import lxml #http://lxml.de/ Used to parse the html
from lxml import html
import sys
reload(sys)  
sys.setdefaultencoding('Cp1252')

#@author Saad Kothawala

DISEASE_LIST_LINK_BASE = "http://www.mayoclinic.org/diseases-conditions/index?letter="
MAIN_LINK = "http://www.mayoclinic.org"
FILE_NAME = "diseases.txt"

print ("--------------Starting Mayo Clinic Scraper--------------")

startTime = time.time()

diseasesAdded = []

count = 0
for letter in letterH: string.ascii_lowercase:#Go through all the alphabet
	page = urllib2.urlopen(DISEASE_LIST_LINK_BASE + letter).read() #get the html
	tree = html.fromstring(page) #make the html easier to use
	links = tree.xpath('//*[@id="index"]/ol/li/a') #Get all diseases in the listing

	for l in links:
		diseaseName = l.text
		if diseaseName[0].lower() == letter and diseaseName not in diseasesAdded:#to avoid duplicates

			#Seperator
			toWrite = diseaseName + "|";
			count += 1
			print count, ": ", diseaseName
			diseaseLink = MAIN_LINK + l.attrib['href'].replace('definition', 'symptoms')
			remedyLink = MAIN_LINK + l.attrib['href'].replace('definition', 'lifestyle-home-remedies')
			
			diseasePage = urllib2.urlopen(diseaseLink).read()
			remedyPage = urllib2.urlopen(remedyLink).read()
			diseaseTree = html.fromstring(diseasePage)
			remedyTree = html.fromstring(remedyPage)
			symptoms = diseaseTree.xpath('//*[@id="main-content"]/ul[1]/li')
			remedies = remedyTree.xpath('//*[@id="main-content"]/ul[1]/li')
			
			
			flag = 0
			for symptom in symptoms:
				if not "Tweet" in symptom.text_content() and not "Share" in symptom.text_content() and not "Definition" in symptom.text_content() and not "Causes" in symptom.text_content() and not "Lifestyle and home remedies" in symptom.text_content():
					toWrite += (symptom.text_content().replace("\r\n", "").replace("\n", "").replace("\t", "").replace("|", "") + "\t").encode("utf-8")
					flag = 1
					diseasesAdded.append(diseaseName)
			
			#Seperator
			toWrite += "|";

			for remedy in remedies:
				if not "Tweet" in remedy.text_content() and not "Share" in remedy.text_content() and not "Definition" in remedy.text_content() and not "Causes" in remedy.text_content() and not "Symptoms" in remedy.text_content():
					toWrite += (remedy.text_content().replace("\r\n", "").replace("\n", "").replace("\t", "").replace("|", "") + "\t").encode("utf-8")
					flag = 1
					diseasesAdded.append(diseaseName)


			toWrite += "\n";
			toWrite.encode('utf-8')
			if flag is 1:#write only if symptopms present
				obj = open(FILE_NAME, 'ab')
				obj.write(toWrite)
				obj.close
			

print ("--------------Done Running Mayo Clinic Scraper--------------\n")
print "Elements Added: ", count
print "Run Time: ", time.time() - startTime, " seconds\n"


