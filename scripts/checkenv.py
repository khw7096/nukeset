#coding:utf8
import os
from PySide2.QtWidgets import *

class CheckEnv(QWidget):
	layout = QVBoxLayout()
	def __init__(self):
		super(CheckEnv, self).__init__()
		self.setLayout(self.layout)
		self.setEnv()

	def setEnv(self):
		envs = ["USER","OCIO","NUKE_PATH","NUKE_FONT_PATH"]
		for e in envs:
			self.layout.addWidget(QLabel("$%s : %s" % (e, os.environ.get(e,""))))

def main():
	global customApp
	try:
		customApp.close()
	except:
		pass
	customApp = CheckEnv()
	try:
		customApp.show()
	except:
		pass
