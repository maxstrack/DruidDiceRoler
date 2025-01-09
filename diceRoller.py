import sys
import random
import qdarkgraystyle
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QSplitter


class DruidDiceRoller(QtWidgets.QMainWindow):
	def __init__(self):
		super(DruidDiceRoller, self).__init__()
		# Load the UI file
		uic.loadUi('mainwindow.ui', self)

		# Connect widgets
		self.nBeastsIn = self.findChild(QtWidgets.QLineEdit, 'nBeastsIn')
		self.toHit = self.findChild(QtWidgets.QLineEdit, 'toHitMod')
		self.rollAll = self.findChild(QtWidgets.QPushButton, 'rollAll')
		self.reset = self.findChild(QtWidgets.QPushButton, 'reset')

		self.diceWidget = self.findChild(QtWidgets.QVBoxLayout, 'diceContainer')
		self.addDiceRow()

		self.addDice = self.findChild(QtWidgets.QPushButton, 'addDice')

		self.tableWidget = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
		splitter = self.findChild(QtWidgets.QSplitter, 'splitter')
		splitter.setSizes([1, 1000])

		# Connect button to the roll function
		self.rollAll.clicked.connect(self.generateTable)
		self.addDice.clicked.connect(self.addDiceRow)


		self.reset.clicked.connect(self.resetTable)

	def resetTable(self):
		self.tableWidget.setRowCount(0)
		self.tableWidget.setColumnCount(4)
	
	def addDiceRow(self):
		# Create widgets for a new dice set
		diceNumIn = QtWidgets.QLineEdit(self)
		diceTypeIn = QtWidgets.QLineEdit(self)
		plusHitIn = QtWidgets.QLineEdit(self)
		removeButton = QtWidgets.QPushButton("Remove", self)

		# Add them to a layout for visual organization
		widget = QtWidgets.QWidget()
		rowLayout = QtWidgets.QHBoxLayout(widget)
		rowLayout.setSpacing(2)
		rowLayout.setContentsMargins(2, 2, 2, 2)
		rowLayout.addWidget(removeButton)
		rowLayout.addWidget(QtWidgets.QLabel("Number of Dice:"))
		rowLayout.addWidget(diceNumIn)
		rowLayout.addWidget(QtWidgets.QLabel("Dice Type:"))
		rowLayout.addWidget(diceTypeIn)
		rowLayout.addWidget(QtWidgets.QLabel("Damage Modifier:"))
		rowLayout.addWidget(plusHitIn)

		# Add to the main container
		if not hasattr(self, 'diceContainerLayout'):
			# Create and set the layout for the dice container if not already done
			self.diceContainerLayout = QtWidgets.QVBoxLayout()
			self.diceContainerLayout.setSpacing(0)
			self.diceContainerLayout.setContentsMargins(0, 0, 0, 0)
			self.diceWidget.addLayout(self.diceContainerLayout)
			self.diceWidgets = [] 

		# Add the new row to the container layout
		self.diceContainerLayout.addWidget(widget)
		self.diceWidgets.append((diceNumIn, diceTypeIn, plusHitIn))

		removeButton.clicked.connect(lambda: self.removeDiceRow(widget))

	def removeDiceRow(self, row_widget):
		# Ensure the container layout exists
		if hasattr(self, 'diceContainerLayout'):
			self.diceContainerLayout.removeWidget(row_widget)

			self.diceWidgets = [
				widgets for widgets in self.diceWidgets if widgets[0].parent() != row_widget
			]

			row_widget.setParent(None)
			row_widget.deleteLater()

	def generateTable(self):
		# Get input values
		try:
			numBeasts = int(self.nBeastsIn.text())
			health = int(self.healthIn.text())

			hitMod = int(self.toHit.text())


		except ValueError:
			QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter valid numbers.")
			return

		# Get dice sets
		diceSets = []
		for diceNumIn, diceTypeIn, plusHitIn in self.diceWidgets:
			try:
				diceSets.append({
					"numDice": int(diceNumIn.text()),
					"typeDice": int(diceTypeIn.text()),
					"damageMod": int(plusHitIn.text())
				})
			except ValueError:
				QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter valid numbers for all dice sets.")
				return

		# Clear the table
		dispHealth = []
		for i in range(numBeasts):
			if (self.tableWidget.item(i, 1)) :
				tmpHealth =  self.tableWidget.item(i, 1).text()
				tmpName = self.tableWidget.item(i, 0).text()
				dispHealth.append((tmpName,tmpHealth))
			else:
				dispHealth.append((f'Beast {i+1}', health))
				

		self.tableWidget.setRowCount(0)
		self.tableWidget.setColumnCount(4+ len(diceSets))
		#self.tableWidget.setHorizontalHeaderLabels(["Name", "Health", "To Hit", "Total Damage"])

		# Populate the table with rows for each beast
		for i in range(numBeasts):
			
			# Roll to hit dice
			hitRoll = random.randint(1, 20) + hitMod

			# Add a row to the table
			rowPosition = self.tableWidget.rowCount()

			self.tableWidget.insertRow(rowPosition)

			# Populate row with data
			self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(dispHealth[rowPosition][0])))
			self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(dispHealth[rowPosition][1])))
			self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(hitRoll)))


			totalDamage = 0
			for j, diceSet in enumerate(diceSets):
				rolls = [random.randint(1, diceSet["typeDice"]) for _ in range(diceSet["numDice"])]
				total = sum(rolls) + diceSet["damageMod"]
				totalDamage += total
				column = j+4
				self.tableWidget.setItem(rowPosition, column, QtWidgets.QTableWidgetItem(str(total)))
				header = self.tableWidget.horizontalHeaderItem(column)
				name = "damage "+str(j+1)
				if header:
					header.setText(name)
				else:
					self.tableWidget.setHorizontalHeaderItem(column, QtWidgets.QTableWidgetItem(name))

				self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(str(totalDamage)))

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = DruidDiceRoller()

	window.show()
	app.setStyleSheet(qdarkgraystyle.load_stylesheet())

	sys.exit(app.exec_())

