#coding:utf8
import nuke
import os
import pathapi
from PySide2.QtWidgets import *

class MakeWrite(QWidget):
	def __init__(self):
		super(MakeWrite, self).__init__()
		self.ok = QPushButton("OK")
		self.cancel = QPushButton("Cancel")
		self.ext = QComboBox()
		self.ext.addItems([".exr",".dpx",".jpg",".png",".mov"])
		self.formats = QComboBox()
		self.formats.addItems(["2048x1152", "1920x1080", "2048x872"])
		self.reformat = QCheckBox("&reformat", self)
		self.reformat.setChecked(True)
		self.slate = QCheckBox("&slate", self)
		self.slate.setChecked(True)
		self.addtimecode = QCheckBox("&AddTimecode", self)
		self.addtimecode.setChecked(False)
		self.startframe = QLineEdit(str(int(nuke.Root()["first_frame"].value())))
		self.starttimecode = QLineEdit("00:00:00:00")

		# 이벤트 설정
		self.ok.clicked.connect(self.pushOK)
		self.cancel.clicked.connect(self.close)

		# Layout 설정
		layout = QGridLayout()
		layout.addWidget(self.reformat, 0, 0)
		layout.addWidget(self.formats, 0, 1)
		layout.addWidget(self.addtimecode, 1, 0)
		layout.addWidget(self.startframe, 1, 1)
		layout.addWidget(self.starttimecode, 1, 2)
		layout.addWidget(self.slate, 2, 0)
		layout.addWidget(QLabel("Ext"), 3, 0)
		layout.addWidget(self.ext, 3, 1)
		layout.addWidget(self.cancel, 4, 1)
		layout.addWidget(self.ok, 4, 2)
		self.setLayout(layout)

		# node list
		self.linkOrder = []
		self.seqname = ""
		self.shotname = ""
		self.taskname = ""
		self.ver = 1

	def genReformat(self):
		reformat = nuke.nodes.Reformat()
		reformat["type"].setValue("to box")
		reformat["box_fixed"].setValue(True)
		width, height = self.formats.currentText().split("x")
		reformat["box_width"].setValue(int(width))
		reformat["box_height"].setValue(int(height))
		self.linkOrder.append(reformat)
	
	def genAddTimecode(self):
		addTimecode = nuke.nodes.AddTimeCode()
		addTimecode["startcode"].setValue(str(self.starttimecode.text()))
		addTimecode["useFrame"].setValue(True)
		addTimecode["frame"].setValue(int(self.startframe.text()))
		self.linkOrder.append(addTimecode)

	def genSlate(self):
		p = nuke.root().name()
		seq, err = pathapi.seq(p)
		if err:
			nuke.message(err)
		shot, err = pathapi.shot(p)
		if err:
			nuke.message(err)
		task, err = pathapi.task(p)
		if err:
			nuke.message(err)
		ver, err = pathapi.ver(p)
		if err:
			nuke.message(err)
		slate = nuke.nodes.slate()
		slate["vendor"].setValue("lazypic")
		slate["user"].setValue(os.getenv("USER"))
		slate["memo"].setValue(" ")
		slate["shot"].setValue(seq+"_"+shot)
		slate["task"].setValue(task)
		slate["version"].setValue(ver)
		self.linkOrder.append(slate)

	def genWrite(self):
		write = nuke.nodes.Write()
		dirname, basename = os.path.split(nuke.root().name())
		filename, notuse = os.path.splitext(basename)
		ext = str(self.ext.currentText())
		write["file_type"].setValue(ext[1:])
		write["file"].setValue("%s/out/%s/%s.####%s" % (dirname, filename, filename, ext))
		write["create_directories"].setValue(True)
		self.linkOrder.append(write)

	def linkNodes(self):
		"""
		linkOrder 노드 순서대로 노드를 연결,생성한다.
		"""
		tail = nuke.selectedNode()
		for n in self.linkOrder:
			n.setInput(0, tail)
			tail = n

	def pushOK(self):
		"""
		OK 버튼을 누르면 노드를 생성한다.
		"""
		if self.reformat.isChecked():
			self.genReformat()
		if self.addtimecode.isChecked():
			self.genAddTimecode()
		if self.slate.isChecked():
			self.genSlate()
		self.genWrite()
		self.linkNodes()
		self.close()

def main():
	if nuke.root().name() == "Root":
		nuke.message("파일이 저장되지 않았습니다.")
		return

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
