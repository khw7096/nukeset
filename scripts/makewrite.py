#coding:utf8
import nuke
from PySide2.QtWidgets import *

class MakeWrite(QWidget):

	def __init__(self):
		super(MakeWrite, self).__init__()
		self.ok = QPushButton("OK")
		self.cancel = QPushButton("Cancel")
		self.ext = QComboBox()
		self.exts = [".exr",".dpx",".tga",".mov"]
		self.ext.addItems(self.exts)
		self.fm = QComboBox()
		self.formats = ["2048x1152", "1920x1080", "2048x872"]
		self.fm.addItems(self.formats)
		self.reformat = QCheckBox("&reformat", self)
		self.reformat.setChecked(True)
		self.slate = QCheckBox("&slate", self)
		self.slate.setChecked(True)
		self.addtimecode = QCheckBox("&AddTimecode", self)
		self.addtimecode.setChecked(False)
		self.startframe = QLineEdit(str(int(nuke.Root()["first_frame"].value())))
		self.starttimecode = QLineEdit("00:00:00:00")

		# event
		self.ok.clicked.connect(self.bt_ok)
		self.cancel.clicked.connect(self.close)

		#set layout
		layout = QGridLayout()
		layout.addWidget(self.reformat, 0, 0)
		layout.addWidget(self.fm, 0, 1)
		layout.addWidget(self.addtimecode, 1, 0)
		layout.addWidget(self.startframe, 1, 1)
		layout.addWidget(self.starttimecode, 1, 2)
		layout.addWidget(self.slate, 2, 0)
		layout.addWidget(QLabel("Ext"), 3, 0)
		layout.addWidget(self.ext, 3, 1)
		layout.addWidget(self.cancel, 4, 0)
		layout.addWidget(self.ok, 4, 1)
		self.setLayout(layout)

	def bt_ok(self):
		tail = nuke.selectedNode()
		linkOrder = []
		if self.reformat.isChecked():
			reformat = nuke.nodes.Reformat()
			reformat["type"].setValue("to box")
			reformat["box_fixed"].setValue(True)
			width, height = self.fm.currentText().split("x")
			reformat["box_width"].setValue(int(width))
			reformat["box_height"].setValue(int(height))
			linkOrder.append(reformat)
		if self.addtimecode.isChecked():
			timecode = nuke.nodes.AddTimeCode()
			timecode["startcode"].setValue(str(self.starttimecode.text()))
			timecode["useFrame"].setValue(True)
			timecode["frame"].setValue(int(self.startframe.text()))
			linkOrder.append(timecode)
		if self.slate.isChecked():
			slate = nuke.nodes.slate()
			linkOrder.append(slate)
		write = nuke.nodes.Write()
		ext = str(self.ext.currentText())
		write["file_type"].setValue(ext[1:])
		write["file"].setValue("/test/test.####" + ext)
		write["create_directories"].setValue(True)
		linkOrder.append(write)
		for n in linkOrder:
			n.setInput(0, tail)
			tail = n
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
