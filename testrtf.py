from app.demonstrator.testparse import TestsRtfdom

domTree = TestsRtfdom()
file = open('tests/files/Test(withsub).rtf')
domTree.openString(file.read())
domTree.parse()
