#!coding:utf8
import nuke
import os
import subprocess
import sys

def browser(path):
	brws = "nautilus"
	if sys.platform == "win32":
		brws = "start"
	elif sys.platform == "darwin":
		brws = "open"
	subprocess.Popen([brws, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#Debug
	"""
	p = subprocess.Popen([brws, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = p.communicate()
	if stderr:
		nuke.tprint(stderr, file=sys.stderr)
	if stdout:
		nuke.tprint(stdout)
	"""

def main():
	focusKnobs = ["file","vfield_file"]
	nodes = nuke.selectedNodes()
	if len(nodes) != 1:
		nuke.message("노드를 하나만 선택해주세요.")
		return
	for knob in focusKnobs:
		if knob in nodes[0].knobs():
			path = nodes[0][knob].value()
			if path == "":
				nuke.message("경로가 비어있습니다.")
				return
			parentPath = os.path.dirname(path)
			if not os.path.exists(parentPath):
				nuke.message("경로가 존재하지 않습니다.")
				return
			browser(parentPath)
			return
	nuke.message("file Knob을 사용하는 노드가 아닙니다.")
