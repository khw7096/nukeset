#coding:utf8
import nuke

def main():
	tails = nuke.selectedNodes()
	if len(tails) == 0:
		nuke.message("노드를 선택해주세요.")
		return
	for tail in tails:
		write = nuke.nodes.Write()
		write.setInput(0,tail)
