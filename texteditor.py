"""
Simple text editor that can load, create and edit files
"""

import sys
from PyQt5.QtWidgets import QLineEdit, QPushButton, QApplication, QLabel, \
	QTextEdit, QVBoxLayout, QHBoxLayout, QWidget


class Editor(QWidget):
	def __init__(self, parent=None):
		super(Editor, self).__init__(parent)
		# Create widgets
		self.setWindowTitle("Text Editor")

		self.namelabel = QLabel("Filename:")
		self.filename = QLineEdit("")
		self.load = QPushButton("Load")
		self.text = QTextEdit()
		self.save = QPushButton("Save")

		# Create layout and add widgets
		self.layout = QVBoxLayout()
		self.sublayout = QHBoxLayout()
		self.sublayout.addWidget(self.filename)
		self.sublayout.addWidget(self.load)

		self.layout.addWidget(self.namelabel)
		self.layout.addLayout(self.sublayout)
		self.layout.addWidget(self.text)
		self.layout.addWidget(self.save)


		# Set dialog layout
		self.setLayout(self.layout)

		# Add button signal to save slot
		self.save.clicked.connect(self.save_text)
		self.load.clicked.connect(self.load_file)

	def save_text(self):
		with open(self.filename.text(), "w") as file:
			file.write(self.text.toPlainText())

	def load_file(self):
		with open(self.filename.text(), "r") as file:
			self.text.setText(file.read())


if __name__ == '__main__':
	# Create the Qt Application
	app = QApplication(sys.argv)
	# Create and show the Editor
	Editor = Editor()
	Editor.show()
	# Run the main Qt loop
	sys.exit(app.exec_())
