"""
Calculator
"""

import sys
import re
from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QVBoxLayout, \
	QWidget, QGridLayout, QGroupBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

LINES_TO_SHOW = 4


class Window(QWidget):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)

		self.setWindowTitle("Calculator")

		self.display = QGroupBox(self)
		self.inside_display = QVBoxLayout()

		self.display_font = QFont("Menlo", 16)
		self.display_font.setLetterSpacing(QFont.AbsoluteSpacing, 2)

		self.lines = []
		for i in range(2 * LINES_TO_SHOW + 1):
			self.add_line()
		self.display.setLayout(self.inside_display)

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
		self.add_button("÷", 1, 4)
		self.add_button("+", 2, 3)
		self.add_button("-", 2, 4)
		self.add_button("0", 3, 0)
		self.add_button("(", 3, 1)
		self.add_button(")", 3, 2)
		self.add_button(".", 3, 3)
		self.add_button("=", 3, 4)

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.display)
		self.layout.addLayout(self.grid_layout)

		self.setLayout(self.layout)
		self.setFixedSize(self.sizeHint())


		self.previous_result = None
		self.previous_expressions = []
		self.current_expression = 0
		self.saved_expression = ""

	def add_button(self, button_str, x, y, clicked_str=None):
		if clicked_str is None:
			clicked_str = button_str
		button = QPushButton(button_str)
		self.grid_layout.addWidget(button, x, y)
		button.clicked.connect(lambda: self.button_pressed(clicked_str))

	def add_line(self, equals=None):
		line = QLabel()
		line.setFont(self.display_font)
		line.setLineWidth(2)

		if equals is not None:
			line.setAlignment(Qt.AlignRight)
			line.setText(equals)

		self.lines.append(line)
		self.inside_display.addWidget(line)

	def button_pressed(self, key_str):
		if key_str in ("x", "÷", "+", "-") and len(self.lines[-1].text()) == 0:
			# Check if this is the first key of the line pressed.
			# If it is, add ANS to the beginning
			self.button_pressed("ANS")
		if key_str == "DEL":
			self.delete_pressed()
		elif key_str == "AC":
			self.clear_pressed()
		elif key_str == "=":
			self.equals_pressed()
		elif key_str == "ANS" and self.previous_result is None:
			return
		else:
			self.lines[-1].setText(self.lines[-1].text() + key_str)

	def delete_pressed(self):
		current_line = self.lines[-1].text()
		if current_line.endswith("ANS"):
			to_delete = 3
			# Deletes all 3 characters of ANS
		else:
			to_delete = 1
		self.lines[-1].setText(current_line[:-to_delete])

	def clear_pressed(self):
		self.lines[-1].setText("")

	def equals_pressed(self):
		to_eval = self.lines[-1].text()
		self.previous_expressions.append(to_eval)
		to_eval = to_eval.replace("x", "*").replace("÷", "/")

		try:
			if "()" in to_eval or re.match(".*[^+\-*/(]\(.*", to_eval):
				# Checks if there is a non operator before the opening brackets
				# This avoids it trying to call an int as a function in eval
				raise SyntaxError

			if re.match(".*[^+\-*/(]ANS.*", to_eval) or \
				re.match(".*ANS[^+\-*/)].*", to_eval):
				# Checks if there is a non operator before or after the the ANS
				raise SyntaxError

			to_eval = to_eval.replace("ANS", str(self.previous_result))
			result = eval(to_eval)

			if result >= 10**13:
				raise ValueError

		except SyntaxError:
			result = "SYNTAX ERROR"
		except (ValueError, ZeroDivisionError):
			result = "MATH ERROR"
		else:
			# If it passes
			self.previous_result = result

			# Convert from 5.0 to 5
			if int(result) == result and isinstance(result, float):
				result = int(result)

			result = "=" + str(result)

		self.add_line(result)
		self.add_line()

		self.clear_top()
		self.current_expression = 0

	def clear_top(self):
		while len(self.lines) > 2 * LINES_TO_SHOW + 1:
			self.inside_display.removeWidget(self.lines[0])
			self.lines[0].deleteLater()
			del self.lines[0]

	def load_expression(self, up=True):
		if self.current_expression == 0:
			self.saved_expression = self.lines[-1].text()
		if up:
			if len(self.previous_expressions) < abs(self.current_expression - 1):
				# We have gone as far back as possible
				return
			self.current_expression -= 1
		else:
			if self.current_expression + 1 > 0:
				# We have returned to the original value
				return
			self.current_expression += 1
		if self.current_expression == 0:
			# We have returned to the start
			expression_to_load = self.saved_expression
		else:
			expression_to_load = self.previous_expressions[self.current_expression]
		self.lines[-1].setText(expression_to_load)

	def keyPressEvent(self, QKeyEvent):
		text, key = QKeyEvent.text().lower(), QKeyEvent.key()
		if text in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "x", "÷",
					"+", "-", "(", ")", ".", "="):
			self.button_pressed(text)
		elif text == "*":
			self.button_pressed("x")
		elif text == "/":
			self.button_pressed("÷")
		elif text == "a":
			self.button_pressed("ANS")
		elif key == 16777219:  # DEL
			self.button_pressed("DEL")
		elif key == 16777220:  # Enter
			self.button_pressed("=")
		elif key in (16777235, 16777238):  # Up  or Page Up
			self.load_expression(up=True)
		elif key in (16777237, 16777239):  # Down  or Page Down
			self.load_expression(up=False)
		elif key == 16777216:  # Escape
			app.quit()


if __name__ == '__main__':
	# Create the Qt Application
	app = QApplication(sys.argv)
	# Create and show the form
	form = Window()
	form.show()
	# Run the main Qt loop
	sys.exit(app.exec_())
