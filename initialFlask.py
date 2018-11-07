from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from readMileageCSV import *

import datetime
import operator

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mileage.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employeeID = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    entry = db.relationship('Entry', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.employeeID}', '{self.email}')"

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_entered = db.Column(db.String, nullable=False)
    locations = db.Column(db.Text, nullable=False)
    milesDriven = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Entry('{self.id}', '{self.date_entered}', '{self.locations}', '{self.milesDriven}', '{self.user_id}')"

    def __showMyGuts__(self):
        return f"Entry('{self.id}', '{self.date_entered}', '{self.locations}', '{self.milesDriven}', '{self.user_id}')"

@app.route('/')
def index():
    bobby = "Word!^^!"
    return render_template("home.html", bobby=bobby)

@app.route('/mileage')
def mileageForm():
    return render_template("mileage.html", locationList = findAllLocations())

# Initialize list to record locations traveled
listOfLocationsTraveled = []

@app.route("/success", methods=["post"])
def mileageSubmission():
    name2 = request.form.get("name1")
    empID2 = request.form.get("empID1")
    date2 = request.form.get("date1")
    locationOne = request.form.get("location1")
    locationTwo = request.form.get("location2")
    locationThree = request.form.get("location3")
    locationFour = request.form.get("location4")
    locationFive = request.form.get("location5")
    valueList = [name2, empID2, date2, locationOne, locationTwo, locationThree, locationFour, locationFive]

    locationList1 = [locationOne, locationTwo, locationThree, locationFour, locationFive]

    distanceTraveled = calculateTotalDisance(locationList1)



    if name2 == "":
        return render_template("error.html", error = "No name")
    return render_template("mileageSuccess.html", name3=name2, empID3=empID2, date3=date2, locationList=locationList1, distance=distanceTraveled)


@app.route('/viewDatabase')
def viewMyDatabase():
    userTable = User.query.all()
    userEntry = Entry.query.all()
    return render_template("viewDatabase.html", myUsers=userTable, myEntries=userEntry, QueryOneTwoThree=1)

@app.route('/<dummy2>')
def fallback(dummy2):
    return render_template("home.html", dummyy1 = "THIS IS A DUMMY ROUTE!! STOP GETTING TRICKED")

@app.route('/calculator', methods=["get", "post"])
def calculatron():
    firstNumber = request.form.get("firstNum")
    secondNumber = request.form.get("secondNum")
    whatToDo = request.form.get("operator")
    resultOfCalculation = 0
    testCalc = 0
    return render_template("calculator.html", calculatedResult = resultOfCalculation, firstNumEntered = firstNumber, secondNumEntered = secondNumber, operatorEntered = whatToDo, testCalc1 = testCalc)

@app.route('/createUser', methods=["post"])
def addUserToDatabase():
    empID9 = request.form.get("myEmpID")
    email9 = request.form.get("myEmail")
    password9 = request.form.get("myPassword")

    addUser = User(employeeID=empID9, email=email9, password=password9)

    db.session.add(addUser)
    db.session.commit()

    return render_template("userAddSuccess.html", empID8=empID9, email8=email9, password8=password9)

@app.route('/createUser', methods=["get"])
def renderCreateUser():
    return render_template("createUser.html")

@app.route('/addEntry', methods=["post"])
def renderEntryToDatabase():
    locationList = []
    location_1 = request.form.get("locationOne")
    location_2 = request.form.get("locationTwo")
    location_3 = request.form.get("locationThree")
    location_4 = request.form.get("locationFour")
    location_5 = request.form.get("locationFive")
    entryDate = request.form.get("dateOne")
    locationList.append(location_1)
    locationList.append(location_2)
    locationList.append(location_3)
    locationList.append(location_4)
    locationList.append(location_5)

    locationListAsString = str(locationList)

    milesDriven = calculateTotalDisance(locationList)
    userID9 = request.form.get("grab_user_ID")

    addEntry = Entry(locations=locationListAsString, milesDriven=milesDriven, user_id=userID9, date_entered=entryDate)

    db.session.add(addEntry)
    db.session.commit()

    return render_template("addEntrySuccess.html", userID8=userID9, locationsWent=locationListAsString, milesDriven=milesDriven, entryDate=entryDate)

@app.route('/addEntry', methods=["get"])
def renderEntryPage():
    return render_template("addEntry.html", locationList = findAllLocations())

@app.route('/queryUsers')
def queryUsers():
    return render_template("QueryUsers.html")

@app.route('/queryStuff', methods=["post"])
def queryStuff():
    queryVar = request.form.get("queryUserOrEntry")
    if queryVar == "users":
        return render_template("viewDatabase.html", queryUserOrEntry = 'User')
    if queryVar == "entries":
        return render_template("viewDatabase.html", queryUserOrEntry = 'Entry')

@app.route('/queryForReals', methods=["post"])
def queryForReals():
    userID = request.form.get("myUserID")
    empID = request.form.get("myEmpID")
    myEmail = request.form.get("myEmail")
    queryVar = request.form.get("queryUserOrEntry")
    if queryVar == "users":
        if userID != "":
            myUserQuery = User.query.filter_by(employeeID = userID).all()
            return render_template("viewDatabase.html", myUsers=myUserQuery, QueryOneTwoThree = 2, clean = 1)
        if empID != "":
            myUserQuery = User.query.filter_by(employeeID = empID).all()
            return render_template("viewDatabase.html", myUsers=myUserQuery, QueryOneTwoThree = 2, clean = 1)
        if myEmail != "":
            myUserQuery = User.query.filter_by(email = myEmail).all()
            return render_template("viewDatabase.html", myEntries=myUserQuery, QueryOneTwoThree = 2, clean = 1)
    if queryVar == "entries":
        if userID != "":
            mySecondQuery = db.session.query(User, Entry).filter(User.id == Entry.user_id).filter(User.id == userID).all()
            return render_template("viewDatabase.html", myUsers=mySecondQuery, QueryOneTwoThree = 3, clean = 1)
        if empID != "":
            mySecondQuery = db.session.query(User, Entry).filter(User.id == Entry.user_id).filter(User.employeeID == empID).all()
            return render_template("viewDatabase.html", myUsers=mySecondQuery, QueryOneTwoThree = 3, clean = 1)
        if myEmail != "":
            mySecondQuery = db.session.query(User, Entry).filter(User.id == Entry.user_id).filter(User.email == myEmail).all()
            return render_template("viewDatabase.html", myEntries=mySecondQuery, QueryOneTwoThree = 3, clean = 1)

@app.route('/cleanUpForPrinting', methods=["post"])
def clean_Up():
    userID = request.form.get("myUserID")
    empID = request.form.get("myEmpID")
    myEmail = request.form.get("myEmail")

    myLocationPrintQuery = db.session.query(Entry.locations).filter(Entry.user_id == userID).all()
    # myPrintQuery = db.session.query(User, Entry).filter(User.id == Entry.user_id).filter(User.id == userID).all()
    myDatePrintQuery = db.session.query(Entry.date_entered).filter(Entry.user_id == userID).all()
    myMilesPrintQuery = db.session.query(Entry.milesDriven).filter(Entry.user_id == userID).all()


    listOfLocationsTraveled = convertLocationQueryToLocationList(myLocationPrintQuery)

    listOfDates = convertDateQueryToDateList(myDatePrintQuery)

    listOfMilesDriven = convertMilesQueryToMilesList(myMilesPrintQuery)

    numberOfEntries = len(listOfLocationsTraveled)

    for i in range(len(myDatePrintQuery)):
        print("Entry #{}".format(i) + str(myDatePrintQuery[i]) + " and " + str(myMilesPrintQuery[i]))

    return render_template("printMileage.html", hideOptions=1, printThis=myLocationPrintQuery, entries=numberOfEntries, locations=listOfLocationsTraveled, dates=listOfDates, miles=listOfMilesDriven)

@app.route('/cleanUpForPrinting', methods=["get"])
def printMileage():
    return render_template("printMileage.html")


@app.route('/birthday')
def tansbday():
    tan = datetime.datetime.now()
    # superDay = tan.month == 10 and tan.day == 28
    superDay = 6
    return render_template("defaultValuePage.html", variable1=tan)

if __name__ == "__main__":
    app.run()
