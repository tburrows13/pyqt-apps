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

		self.grid = "7 8 9 D Ar" \
					"4 5 6 x %r" \
					"1 2 3 + -r" \
					"0 0 . = =r"
		self.grid = [li.split() for li in self.grid.split("r")]

		self.layout = QGridLayout()

		for i, row in enumerate(self.grid):
			for j, column in enumerate(row):
				self.layout.addWidget(str(column), i, j)

		self.setLayout(self.layout)



if __name__ == '__main__':
	# Create the Qt Application
	app = QApplication(sys.argv)
	# Create and show the form
	form = Window()
	form.show()
	# Run the main Qt loop
	sys.exit(app.exec_())
