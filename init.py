#coding:utf8
import nuke
import os

nuke.pluginAddPath("./gizmos", addToSysPath=True)
nuke.pluginAddPath("./images", addToSysPath=True)
nuke.pluginAddPath("./lib", addToSysPath=True)
nuke.pluginAddPath("./scripts", addToSysPath=True)

# View Lut
nukePath = os.environ["NUKE_PATH"]
nuke.ViewerProcess.register("AlexaV3LogC", nuke.createNode, ("Vectorfield", "vfield_file %s/luts/ARRI_LogC2Video_Classic709_davinci3d.cube colorspaceIn AlexaV3LogC" % (nukePath)))

# Format
nuke.addFormat("24 24 nukeIcon")
nuke.addFormat("360 360 kakaoEmoticon")
