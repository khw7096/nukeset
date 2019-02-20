#coding:utf8
import nuke
from PySide2.QtWidgets import *

class MakeWrite(QWidget):
	formats = ["2048x1152", "1920x1080", "2048x872"]
	exts = [".exr",".dpx",".tga",".mov"]

	def __init__(self):
		super(MakeWrite, self).__init__()
		self.ok = QPushButton("OK")
		self.cancel = QPushButton("Cancel")
		self.ext = QComboBox()
		self.ext.addItems(self.exts)
		self.fm = QComboBox()
		self.fm.addItems(self.formats)
		self.reformat = QCheckBox("&reformat", self)
		self.reformat.setChecked(True)
		self.slate = QCheckBox("&slate", self)
		self.slate.setChecked(True)

		# event
		self.ok.clicked.connect(self.bt_ok)
		self.fm.currentIndexChanged.connect(self.indexChanged)
		self.cancel.clicked.connect(self.close)

		#set layout
		layout = QGridLayout()
		layout.addWidget(self.reformat, 0, 0)
		layout.addWidget(self.fm, 0, 1)
		layout.addWidget(QLabel("master Ext"), 1, 0)
		layout.addWidget(self.ext, 1, 1)
		layout.addWidget(self.slate, 2, 0)
		layout.addWidget(self.cancel, 3, 0)
		layout.addWidget(self.ok, 3, 1)
		self.setLayout(layout)

	def indexChanged(self):
		self.reformatSize = self.fm.currentText()

	def bt_ok(self):
		print self.fm.currentText()
		print self.ext.currentText()
		print self.reformat.isChecked()
		print self.slate.isChecked()
		self.close()


def main():
	if len(nuke.selectedNodes()) != 1:
		nuke.message("노드를 하나만 선택해주세요.")
		return
	global customApp
	try:
		customApp.close()
	except:
		pass
	customApp = MakeWrite()
	try:
		customApp.show()
	except:
		pass
	tail = nuke.selectedNode()
	reformat = nuke.nodes.Reformat()
	reformat["type"].setValue("to box")
	reformat["box_fixed"].setValue(True)
	reformat["box_width"].setValue(2048)
	reformat["box_height"].setValue(968)
	reformat.setInput(0, tail)
	timecode = nuke.nodes.AddTimeCode()
	timecode["startcode"].setValue("01:00:00:00")
	timecode["useFrame"].setValue(True)
	timecode["frame"].setValue(1001)
	timecode.setInput(0,reformat)
	slate = nuke.nodes.slate()
	slate.setInput(0, timecode)
	write = nuke.nodes.Write()
	write["file_type"].setValue("exr")
	write["file"].setValue("/test/test.####.exr")
	write["create_directories"].setValue(True)
	write.setInput(0,slate)
