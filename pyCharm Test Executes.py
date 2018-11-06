from initialFlask import *

from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from readMileageCSV import *


import operator

# myPrintQuery = db.session.query(User, Entry).filter(User.id == Entry.user_id).filter(User.id == 2).all()

myPrintQuery = db.session.query(Entry.locations).filter(Entry.user_id == 2).all()

print(myPrintQuery)




def convertLocationQueryToLocationList(myPrintQuery):
	eachEntryFixed1 = ""
	newList = []
	fixedListFinal = []
	fixedListFinal2 = []

	for eachEntry in myPrintQuery:
		fixedList = []
		fixedList2 = []

		# Removes filler text
		eachEntryFixed1 = str(eachEntry).replace("(", "")
		eachEntryFixed2 = str(eachEntryFixed1).replace(")", "")
		eachEntryFixed3 = str(eachEntryFixed2).replace("\"", "")
		eachEntryFixed4 = str(eachEntryFixed3).replace("", "")
		eachEntryFixed5 = eachEntryFixed4.replace("\'", "")
		eachEntryFixed6 = eachEntryFixed5[:-1]
		eachEntryFixed7 = eachEntryFixed6.replace("[", "")
		eachEntryFixed8 = eachEntryFixed7.replace("]", "")
		eachEntryFixed9 = eachEntryFixed8.split(",")

		# Remove leading whitespace
		for eachitem in eachEntryFixed9:
			fixedList.append(eachitem.lstrip())

		# Remove blank entries
		for eachitem in fixedList:
			if eachitem != '':
				fixedList2.append(eachitem)

		# Add formatted locations to finalized list
		fixedListFinal.append(fixedList2)

	for eachItem in fixedListFinal:
		myString = " -> ".join(eachItem)
		fixedListFinal2.append(myString)


	return fixedListFinal2


print(myPrintQuery)

listOfLocationsTraveled = convertLocationQueryToLocationList(myPrintQuery)

print(listOfLocationsTraveled)

print(len(listOfLocationsTraveled))


