#!/usr/bin/env python3
#Pooja Rathnashyam, ECE 2524
import pymongo

class mongoDB:
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client.db
        self.collection = self.db.collection
        self.list = []
        self.grades = []

    #deletes an assignment from the database
    def deleteAssignment(self, assignmentInfo):
        currentAssignment = self.collection.find_one(assignmentInfo)
        if currentAssignment == None:
            print("Grade doesn't Exist :(")
        else:
            self.db.collection.remove(assignmentInfo)
            print("Grade Successfully Removed!")

    #clears out the database
    def clear(self):
        self.db.collection.drop()

    #adds a class to the database
    def addClass(self, classInfo):
        try:
            self.collection.insert_one(classInfo)
            self.list.append(classInfo['Class'])
        except pymongo.errors.DuplicateKeyError:
            pass
        print(classInfo)

    #adds an assignment to the database
    def addAssignment(self, assignmentInfo):
        try:
            self.collection.insert_one(assignmentInfo)
        except pymongo.errors.DuplicateKeyError:
            pass
        print(assignmentInfo)

    #calculates the final grades
    def calculate(self):
        answer = ""
        length = len(self.list)
        if length == 0:
            return 'No Classes Added Yet :('
        else: # calculate grades for the classes
            for x in self.list:
                currentGrade = 0
                classQuery = { "Class" : x, "Type" : "Grade_Scale"}
                classTemp = self.collection.find_one(classQuery)

                #calculates assignments average
                assignmentQuery = { "Class" : x , "Type" : "Assignment"}
                assignmentTemp = self.collection.find(assignmentQuery)
                assignmentTotal = 0
                numAssignments = 0
                if(assignmentTemp):
                    for y in assignmentTemp:
                        numAssignments += 1
                        assignmentTotal += int(y['Grade'])
                    if(numAssignments != 0):
                        assignmentTotal = assignmentTotal/(numAssignments*100)

                #calculates projects average
                projectQuery = { "Class" : x , "Type" : "Project"}
                projectTemp = self.collection.find(projectQuery)
                projectTotal = 0
                numProjects = 0
                if(projectTemp):
                    for y in projectTemp:
                        numProjects += 1
                        projectTotal += int(y['Grade'])
                    if(numProjects != 0):
                        projectTotal = projectTotal/(numProjects*100)

                #calculates attendance average
                attendanceQuery = { "Class" : x , "Type" : "Attendance"}
                attendanceTemp = self.collection.find(attendanceQuery)
                attendanceTotal = 0
                numAttendances = 0
                if(attendanceTemp):
                    for y in attendanceTemp:
                        numAttendances += 1
                        attendanceTotal += int(y['Grade'])
                    if(numAttendances != 0):
                        attendanceTotal = attendanceTotal/(numAttendances*100)

                #calculates quiz average
                quizQuery = { "Class" : x , "Type" : "Quiz"}
                quizTemp = self.collection.find(quizQuery)
                quizTotal = 0
                numQuizzes = 0
                if(quizTemp):
                    for y in quizTemp:
                        numQuizzes += 1
                        quizTotal += int(y['Grade'])
                    if(numQuizzes != 0):
                        quizTotal = quizTotal/(numQuizzes*100)

                #calculates bonus average
                bonusQuery = { "Class" : x , "Type" : "Bonus"}
                bonusTemp = self.collection.find(bonusQuery)
                bonusTotal = 0
                if(bonusTemp):
                    for y in bonusTemp:
                        bonusTotal += int(y['Grade'])

                #calculates final avarage
                finalQuery = { "Class" : x , "Type" : "Final"}
                finalTemp = self.collection.find(finalQuery)
                finalTotal = 0
                numFinals = 0
                if(finalTemp):
                    for y in finalTemp:
                        numFinals += 1
                        finalTotal += int(y['Grade'])
                    if(numFinals != 0):
                        finalTotal = finalTotal/(numFinals*100)

                #calculates the final grades
                currentGrade += (classTemp['Assignment_Scale']*assignmentTotal)
                currentGrade += (classTemp['Project_Scale']*projectTotal)
                currentGrade += (classTemp['Attendance_Scale']*attendanceTotal)
                currentGrade += (classTemp['Quiz_Scale']*quizTotal)
                currentGrade += (classTemp['Final_Scale']*finalTotal)
                currentGrade += (bonusTotal)

                tempAnswer = "{}:{} \n".format(x, currentGrade)
                answer += tempAnswer
            return answer
