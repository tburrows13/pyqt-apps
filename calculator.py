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
	QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QFrame
from PyQt5.QtGui import QFont




class Window(QWidget):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)

		self.display = QLabel(self)

		display_font = QFont("Menlo", 16)
		display_font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
		self.display.setFont(display_font)
		#self.display.setIndent(10)
		self.display.setLineWidth(2)
		self.display.setFrameStyle(QFrame.Panel | QFrame.Raised)
		#self.display.setLineWidth(2)

		self.grid = "7 8 9r" \
					"4 5 6r" \
					"1 2 3r"
		self.grid = [li.split() for li in self.grid.split("r")]

		self.grid_layout = QGridLayout()

		for i, row in enumerate(self.grid):
			for j, column in enumerate(row):
				self.add_button(column, i, j)

		self.add_button("DEL", 0, 3)
		self.add_button("AC", 0, 4)
		self.add_button("x", 1, 3)
		self.add_button("/", 1, 4)
		self.add_button("+", 2, 3)
		self.add_button("-", 2, 4)

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.display)
		self.layout.addLayout(self.grid_layout)

		self.setLayout(self.layout)

	def add_button(self, button_str, x, y, clicked_str=None):
		if clicked_str is None:
			clicked_str = button_str
		button = QPushButton(button_str)
		self.grid_layout.addWidget(button, x, y)
		button.clicked.connect(lambda: self.button_pressed(clicked_str))

	def button_pressed(self, key_str):
		if key_str == "DEL":
			self.display.setText(self.display.text()[:-1])
		elif key_str == "AC":
			self.display.setText("")
		else:
			self.display.setText(self.display.text() + key_str)

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
