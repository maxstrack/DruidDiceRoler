import sys
import random
from PyQt5 import QtWidgets, uic

class BeastDiceApp(QtWidgets.QMainWindow):
	def __init__(self):
		super(BeastDiceApp, self).__init__()
		# Load the UI file
		uic.loadUi('mainwindow.ui', self)

		# Connect widgets
		self.nBeastsIn = self.findChild(QtWidgets.QLineEdit, 'nBeastsIn')
		self.rollAll = self.findChild(QtWidgets.QPushButton, 'rollAll')
		self.toHitMod = self.findChild(QtWidgets.QPushButton, 'toHitMod ')

		self.diceNumIn_1 = self.findChild(QtWidgets.QLineEdit, 'diceNumIn')
		self.diceTypeIn_1 = self.findChild(QtWidgets.QLineEdit, 'diceTypeIn')
		self.plusHitIn_1 = self.findChild(QtWidgets.QLineEdit, 'plusHitIn')

		self.diceNumIn_2 = self.findChild(QtWidgets.QLineEdit, 'diceNumIn_2')
		self.diceTypeIn_1 = self.findChild(QtWidgets.QLineEdit, 'diceTypeIn_2')
		self.plusHitIn_2 = self.findChild(QtWidgets.QLineEdit, 'plusHitIn_2')

		self.tableWidget = self.findChild(QtWidgets.QTableWidget, 'tableWidget')

		# Connect button to the roll function
		self.rollAll.clicked.connect(self.generateTable)

	def generateTable(self):
		# Get input values
		try:
			numBeasts = int(self.nBeastsIn.text())
			health = int(self.healthIn.text())

			hitMod = int(self.plusHitIn.text())

			numDice_1 = int(self.diceNumIn.text())
			typeDice_1 = int(self.diceTypeIn.text())
			damageMod_1 = int(self.plusHitIn.text())

			numDice_2 = int(self.diceNumIn_2.text())
			typeDice_2 = int(self.diceTypeIn_2.text())
			damageMod_2 = int(self.plusHitIn_2.text())

		except ValueError:
			QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter valid numbers.")
			return

		# Clear the table
		dispHealth = []
		for i in range(numBeasts):
			if (self.tableWidget.item(i, 1)) :
				dispHealth.append(self.tableWidget.item(i, 1).text())
			else:
				dispHealth.append(health)
				

		self.tableWidget.setRowCount(0)

		# Populate the table with rows for each beast
		for i in range(numBeasts):
			
			# Roll to hit dice
			hitRoll = random.randint(1, 20) + hitMod

			# Roll dice and calculate total
			rolls_1 = [random.randint(1, typeDice_1) for _ in range(numDice_1)]
			total_1 = sum(rolls_1) + damageMod_1

			rolls_2 = [random.randint(1, typeDice_2) for _ in range(numDice_2)]
			total_2 = sum(rolls_2) + damageMod_2

			# Add a row to the table
			rowPosition = self.tableWidget.rowCount()

			self.tableWidget.insertRow(rowPosition)

			# Populate row with data
			self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(f'Beast {i+1}'))
			self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(dispHealth[rowPosition])))
			self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(hitRoll)))

			#self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(", ".join(map(str, rolls))))
			self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(str(total_1)))
			self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(str(total_2)))

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = BeastDiceApp()
	window.show()
	sys.exit(app.exec_())

