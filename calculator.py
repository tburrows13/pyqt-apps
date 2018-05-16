"""
Calculator

[Display]
789DA
456x%
123+-
00.==
"""

import sys
from PyQt5.QtWidgets import QLineEdit, QPushButton, QApplication, QDialog, \
	QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout


class Window(QWidget):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)

		self.grid = "7 8 9r" \
					"4 5 6r" \
					"1 2 3r"
		self.grid = [li.split() for li in self.grid.split("r")]

		self.layout = QGridLayout()

		for i, row in enumerate(self.grid):
			for j, column in enumerate(row):
				self.layout.addWidget(QPushButton(column), i, j)

		delete = QPushButton("DEL")
		self.layout.addWidget(delete, 0, 3)
		clear = QPushButton("AC")
		self.layout.addWidget(clear, 0, 4)
		mul = QPushButton("x")
		self.layout.addWidget(mul, 1, 3)
		div = QPushButton("/")
		self.layout.addWidget(div, 1, 4)
		add = QPushButton("+")
		self.layout.addWidget(add, 2, 3)
		sub = QPushButton("-")
		self.layout.addWidget(sub, 2, 4)
		sub.clicked.connect(self.subtract)
		sub.clicked.connect(self.pressed)

		self.setLayout(self.layout)

	def subtract(self):
		print("Sub")

	def pressed(self):
		print("Button pressed")


if __name__ == '__main__':
	# Create the Qt Application
	app = QApplication(sys.argv)
	# Create and show the form
	form = Window()
	form.show()
	# Run the main Qt loop
	sys.exit(app.exec_())
