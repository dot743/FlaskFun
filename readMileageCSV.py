# Import csv functions
import csv

# Open file
mileageFile = open('District_Mileage_Chart.csv')

# Reads file as a csv
mileageReader = csv.reader(mileageFile)

# Inputs data from file into list
mileageData = list(mileageReader)

# Test Values
location1 = 'Anaheim Hills'
location2 = 'Anaheim Hills'
locationList = ['Anaheim Hills', 'California', 'Cambridge', ""]

# Finds row number of location
def rowLocationValue(locationName):
	rowNumber = 0
	for eachRow in mileageData:
		if eachRow[0] == locationName:
			# print("The row location of {} is: {}".format(locationName, rowNumber))
			return rowNumber
		else:
			rowNumber += 1
	return 1000

# Finds column number of location
def columnLocationValue(locationName):
	columnNumber = 0
	for eachColumn in mileageData[0]:
		if eachColumn == locationName:
			# print("The column location of {} is: {}".format(locationName, columnNumber))
			return columnNumber
		else:
			columnNumber += 1
	return 1000

print("")
print("")

# Calculate distance between two locations
def mileageDistance(locationOne, locationTwo):
	sourceRow = rowLocationValue(locationOne)
	destinationColumn = columnLocationValue(locationTwo)

	if locationTwo == '':
		return 0.0
	if mileageData[sourceRow][destinationColumn] == '':
		return 0.0
	else:
		return float(mileageData[sourceRow][destinationColumn])

# Calculate total distance between a list of locations
def calculateTotalDisance(locationList):
	totalDistance= 0
	try:
		for i in range(len(locationList)):
			totalDistance += mileageDistance(locationList[i], locationList[i+1])
	except IndexError:
		pass
	return round(totalDistance,1)

# print("The total distance between these locations: {} is: {}".format(locationList, calculateTotalDisance(locationList)))

def findAllLocations():
	allLocations = []
	for eachLocation in mileageData[0]:
		allLocations.append(eachLocation)
	return allLocations

