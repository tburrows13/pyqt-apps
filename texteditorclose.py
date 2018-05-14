"""
A text editor that asks for confirmation before closing, if the file hasn't
been saved already
"""

import sys
from PyQt5.QtWidgets import QLineEdit, QPushButton, QApplication, QDialog, \
	QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget


class ConfirmClose(QDialog):
	def __init__(self, parent=None):
		super(ConfirmClose, self).__init__(parent)
		self.setModal(True)
		self.parent = parent
		self.setWindowTitle("Save?")
		self.question = QLabel("Would you like to save before closing?")

		self.cancel = QPushButton("Cancel")
		self.no = QPushButton("No")
		self.yes = QPushButton("Yes")
		self.yes.setDefault(True)

		self.buttons = QHBoxLayout()
		self.buttons.addWidget(self.cancel)
		self.buttons.addWidget(self.no)
		self.buttons.addWidget(self.yes)

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.question)
		self.layout.addLayout(self.buttons)

		self.setLayout(self.layout)

		self.yes.clicked.connect(parent.save_text)
		self.yes.clicked.connect(parent.close)
		self.yes.clicked.connect(self.close)

		self.no.clicked.connect(parent.close)
		self.no.clicked.connect(self.close)

		self.cancel.clicked.connect(self.cancel_clicked)

	def cancel_clicked(self):
		self.parent.close_widget_open = False
		self.close()


class Editor(QWidget):
	def __init__(self, parent=None):
		super(Editor, self).__init__(parent)
		self.close_widget_open = False
		self.saved = True

		# Create widgets
		self.setWindowTitle("Tom's Text Editor")

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
		self.text.textChanged.connect(self.unset_saved)

	def unset_saved(self):
		self.saved = False

	def save_text(self):
		with open(self.filename.text(), "w") as file:
			file.write(self.text.toPlainText())
		self.saved = True

	def load_file(self):
		try:
			with open(self.filename.text(), "r") as file:
				self.text.setText(file.read())
		except FileNotFoundError:
			pass
		self.saved = True

	def closeEvent(self, event):
		if not self.close_widget_open and not self.saved:
			dialog = ConfirmClose(parent=self)
			dialog.show()
			event.ignore()
			self.close_widget_open = True
		else:
			event.accept()



if __name__ == '__main__':
	# Create the Qt Application
	app = QApplication(sys.argv)
	# Create and show the form
	form = Editor()
	form.show()
	# Run the main Qt loop
	sys.exit(app.exec_())