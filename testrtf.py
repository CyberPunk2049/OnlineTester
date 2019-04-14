from app.demonstrator.testparse import TestsRtfdom

domTree = TestsRtfdom()
file = open('tests/files/graphicsfromsv.rtf')
domTree.openString(file.read())
domTree.parse()
