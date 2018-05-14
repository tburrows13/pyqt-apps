"""
A text editor that autosaves when 5 changes have been made to the text
"""

import sys
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication, QDialog,
							QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget)


class Editor(QWidget):
	def __init__(self, parent=None):
		super(Editor, self).__init__(parent)
		# Create widgets
		self.setWindowTitle("Tom's Text Editor")

		self.namelabel = QLabel("Filename:")
		self.filename = QLineEdit("")
		self.load = QPushButton("Load")
		self.text = QTextEdit()
		self.save = QPushButton("Save")
		self.issaved = QLabel("Saved")

		# Create layout and add widgets
		self.layout = QVBoxLayout()
		self.toplayout = QHBoxLayout()
		self.toplayout.addWidget(self.filename)
		self.toplayout.addWidget(self.load)
		self.bottomlayout = QHBoxLayout()
		self.bottomlayout.addWidget(self.save)
		self.bottomlayout.addWidget(self.issaved)

		self.layout.addWidget(self.namelabel)
		self.layout.addLayout(self.toplayout)
		self.layout.addWidget(self.text)
		self.layout.addLayout(self.bottomlayout)


		# Set dialog layout
		self.setLayout(self.layout)

		# Add button signal to save slot
		self.save.clicked.connect(self.save_text)
		self.load.clicked.connect(self.load_file)
		self.text.textChanged.connect(self.update_label)

		self.save_counter = 5

	def save_text(self):
		with open(self.filename.text(), "w") as file:
			file.write(self.text.toPlainText())
		#self.text.saved.emit()
		self.issaved.setText("Saved")

	def update_label(self):
		self.save_counter += 1
		if self.save_counter > 4:
			self.save_counter = 0
			self.save_text()
		else:
			self.issaved.setText("Not Saved")
	def load_file(self):
		self.save_counter = 5
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