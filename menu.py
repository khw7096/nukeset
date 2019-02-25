import nuke
import nukescripts
import checkenv
import openfile
import makewrite
import nklibrary

tb = nuke.toolbar("Nodes")
m = tb.addMenu("Lazypic", icon="lazypic_logo.png")
m.addMenu("Draw")
m.addCommand("Draw/timecode_burnin", "nuke.createNode('timecode_burnin')")
m.addCommand("Draw/slate", "nuke.createNode('slate')")

mb = menubar.addMenu("Lazypic")
mb.addCommand("Issue_and_Bugs", "nukescripts.start('https://github.com/lazypic/nuke/issues')")
mb.addCommand("-","","")
mb.addCommand("StartPerformanceTimers", "nuke.startPerformanceTimers()")
mb.addCommand("StopPerformanceTimers", "nuke.stopPerformanceTimers()")
mb.addCommand("-","","")
mb.addCommand("CheckENV", "checkenv.main()")
mb.addCommand("OpenFile", "reload(openfile);openfile.main()", "F8", shortcutContext=2)
mb.addCommand("MakeWrite", "reload(makewrite);makewrite.main()", "F10", shortcutContext=2)
mb.addCommand("Nklibrary", "reload(nklibrary);nklibrary.main()")
