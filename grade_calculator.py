#!/usr/bin/env python3
#Pooja Rathnashyam, ECE 2524
import sys
import mongoDB
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Calculator:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.mongo = mongoDB.mongoDB()
        self.mongo.clear()

        #this box adds a class
        self.firstBox = QGroupBox("Add Class and Set Scale")
        self.layout = QFormLayout()
        self.className = QLineEdit()
        self.assignmentScale = QLineEdit()
        self.projectScale = QLineEdit()
        self.attendanceScale = QLineEdit()
        self.quizScale = QLineEdit()
        self.finalScale = QLineEdit()
        self.addClass = QPushButton("Add Class!")
        self.layout.addRow(QLabel("Class:"), self.className)
        self.layout.addRow(QLabel("Assignments %:"), self.assignmentScale)
        self.layout.addRow(QLabel("Project %:"), self.projectScale)
        self.layout.addRow(QLabel("Attendance %:"), self.attendanceScale)
        self.layout.addRow(QLabel("Quiz %:"), self.quizScale)
        self.layout.addRow(QLabel("Final %:"), self.finalScale)
        self.layout.addRow(self.addClass)
        self.firstBox.setLayout(self.layout)
        self.addClass.clicked.connect(lambda: self.class_button_clicked())

        #this box adds an assignment
        self.second = QGridLayout()
        self.secondA = QGroupBox("Grade Type")
        self.secondB = QGroupBox("Actual Grade")
        self.secondALayout = QGridLayout()
        self.secondBLayout = QFormLayout()
        self.assignment = QRadioButton("Assignment")
        self.project = QRadioButton("Project")
        self.attendance = QRadioButton("Attendance")
        self.quiz = QRadioButton("Quiz")
        self.bonus = QRadioButton("Bonus")
        self.final = QRadioButton("Final")
        self.group = QButtonGroup()
        self.group.addButton(self.assignment)
        self.group.addButton(self.project)
        self.group.addButton(self.attendance)
        self.group.addButton(self.quiz)
        self.group.addButton(self.bonus)
        self.group.addButton(self.final)
        self.secondALayout.addWidget(self.assignment)
        self.secondALayout.addWidget(self.project)
        self.secondALayout.addWidget(self.attendance)
        self.secondALayout.addWidget(self.quiz)
        self.secondALayout.addWidget(self.bonus)
        self.secondALayout.addWidget(self.final)
        self.secondA.setLayout(self.secondALayout)

        self.calculate = QPushButton('Add Grade!')
        self.remove = QPushButton('Delete Grade!')
        self.grade = QLineEdit()
        self.classForGrade = QLineEdit()
        self.secondBLayout.addRow(QLabel("Class: "), self.classForGrade)
        self.secondBLayout.addRow(QLabel("Grade (%) : "), self.grade)
        self.secondBLayout.addRow(self.calculate)
        self.secondBLayout.addRow(self.remove)
        self.calculate.clicked.connect(lambda: self.grade_button_clicked())
        self.remove.clicked.connect(lambda: self.delete_button_clicked())
        self.secondB.setLayout(self.secondBLayout)

        self.second.addWidget(self.secondA, 0, 0)
        self.second.addWidget(self.secondB, 0, 1)

        #this box shows your final grades
        self.third = QGridLayout()
        self.alert = QMessageBox()
        self.grades = QPushButton('Calculate!')
        self.third.addWidget(self.grades)
        self.grades.clicked.connect(lambda: self.grade_update())

        #set the groupboxs
        self.secondBox = QGroupBox("Add/Delete Grade")
        self.thirdBox = QGroupBox("Final Grades")
        self.secondBox.setLayout(self.second)
        self.thirdBox.setLayout(self.third)

        #put it all together
        self.grid = QGridLayout()
        self.grid.addWidget(self.firstBox, 0, 0);
        self.grid.addWidget(self.secondBox, 1, 0);
        self.grid.addWidget(self.thirdBox, 2, 0);
        self.window.setLayout(self.grid)
        self.window.resize(450, 300)
        self.window.show()
        self.app.exec_()

    def class_button_clicked(self):
        classBox = self.className.text()
        assignmentScaleBox = int(self.assignmentScale.text())
        projectScaleBox = int(self.projectScale.text())
        attendanceScaleBox = int(self.attendanceScale.text())
        quizScaleBox = int(self.quizScale.text())
        finalScaleBox = int(self.finalScale.text())
        self.className.setText("")
        self.assignmentScale.setText("")
        self.projectScale.setText("")
        self.attendanceScale.setText("")
        self.quizScale.setText("")
        self.finalScale.setText("")
        myquery = {"Class" : classBox, "Type" : "Grade_Scale", "Assignment_Scale" : assignmentScaleBox,
        "Project_Scale" : projectScaleBox, "Attendance_Scale" : attendanceScaleBox,
        "Quiz_Scale" : quizScaleBox, "Final_Scale" : finalScaleBox}
        self.mongo.addClass(myquery)

    def grade_button_clicked(self):
        gradeBox = self.grade.text()
        gradeForClassBox = self.classForGrade.text()
        self.grade.setText("")
        self.classForGrade.setText("")
        if(self.assignment.isChecked()):
            self.group.setExclusive(False)
            self.assignment.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Assignment" , "Grade" : gradeBox}
            self.mongo.addAssignment(myquery)
        elif (self.project.isChecked()):
            self.group.setExclusive(False)
            self.project.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Project" , "Grade" : gradeBox}
            self.mongo.addAssignment(myquery)
        elif (self.attendance.isChecked()):
            self.group.setExclusive(False)
            self.attendance.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Attendance" , "Grade" : gradeBox}
            self.mongo.addAssignment(myquery)
        elif (self.quiz.isChecked()):
            self.group.setExclusive(False)
            self.quiz.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Quiz" , "Grade" : gradeBox}
            self.mongo.addAssignment(myquery)
        elif (self.bonus.isChecked()):
            self.group.setExclusive(False)
            self.bonus.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Bonus" , "Grade" : gradeBox}
            self.mongo.addAssignment(myquery)
        else: #final must be checked
            self.group.setExclusive(False)
            self.final.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Final" , "Grade" : gradeBox}
            self.mongo.addAssignment(myquery)

    def delete_button_clicked(self):
        gradeBox = self.grade.text()
        gradeForClassBox = self.classForGrade.text()
        self.grade.setText("")
        self.classForGrade.setText("")
        if(self.assignment.isChecked()):
            self.group.setExclusive(False)
            self.assignment.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Assignment" , "Grade" : gradeBox}
            self.mongo.deleteAssignment(myquery)
        elif (self.project.isChecked()):
            self.group.setExclusive(False)
            self.project.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Project" , "Grade" : gradeBox}
            self.mongo.deleteAssignment(myquery)
        elif (self.attendance.isChecked()):
            self.group.setExclusive(False)
            self.attendance.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Attendance" , "Grade" : gradeBox}
            self.mongo.deleteAssignment(myquery)
        elif (self.quiz.isChecked()):
            self.group.setExclusive(False)
            self.quiz.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Quiz" , "Grade" : gradeBox}
            self.mongo.deleteAssignment(myquery)
        elif (self.bonus.isChecked()):
            self.group.setExclusive(False)
            self.bonus.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Bonus" , "Grade" : gradeBox}
            self.mongo.deleteAssignment(myquery)
        else: #final must be checked
            self.group.setExclusive(False)
            self.final.setChecked(False)
            self.group.setExclusive(True)
            myquery = {"Class" : gradeForClassBox, "Type" : "Final" , "Grade" : gradeBox}
            self.mongo.deleteAssignment(myquery)

    def grade_update(self):
        answer = self.mongo.calculate()
        self.alert.setText(answer)
        self.alert.exec_()

if __name__ == '__main__':
    calc = Calculator()
