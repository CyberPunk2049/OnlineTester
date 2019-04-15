from app.demonstrator.testparse import TestsRtfdom

domTree = TestsRtfdom()
file = open('tests/files/4quest2picVar1.rtf')
domTree.openString(file.read())
domTree.parse()
