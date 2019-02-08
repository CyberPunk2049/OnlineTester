from pyrtfdom.dom import RTFDOM
import re


class TestsRtfdom(RTFDOM):

    def get_text(self, curNode = None, attr = None):

        if attr == None:
            attr = []

        if curNode is None:
            curNode = self.rootNode

        if curNode.nodeType == 'text':
            if isinstance(curNode.value, (bytes, bytearray)):
                nodeValue = '<Binary Data>'
            else:
                nodeValue = curNode.value
            if len(nodeValue) > 0:
                attr.append(nodeValue)
                print(len(attr))

        if curNode.children:
            for child in curNode.children:
                self.get_text(child, attr)


        return attr

    def test_dict(self):
        test_text = self.get_text()
        i, length = 0, len(test_text)
        test = {
            'variant': '',
            'questions': [],
        }

        while i < length:
            if re.match(r'Вариант: №\d{1,2}.', test_text[i]):
                test['variant'] = re.sub(r'[^0-9]', '', test_text[i])
                i += 1
                continue
            if re.match(r'Задание №\d{1,2}', test_text[i]):
                question = {
                    'number': re.findall(r'Задание №(\d{1,2})', test_text[i])[0],
                    'name': test_text[i],
                    'text': test_text[i+1],
                    'answers': [],
                    'answers_bool': []
                }
                answers = re.split(r'\d\)', test_text[i+2])
                for answer in answers[1:]:
                    question['answers'].append(answer)
                test['questions'].append(question)
                i = i + 3
                continue
            if re.match(r'Ответы:', test_text[i]):
                answer_values = re.split(r'#', test_text[i+2])[1:]
                for answer_value in answer_values:
                    value = re.split(r' \(1 б.\)', answer_value)
                    for l in range(0, len(test['questions'][int(value[0])-1]['answers'])):
                        if str(l+1) in re.findall(r'\d', value[1]):
                            test['questions'][int(value[0]) - 1]['answers_bool'].append('True')
                        else:
                            test['questions'][int(value[0]) - 1]['answers_bool'].append('False')
            i += 1

        return test


domTree = TestsRtfdom()
file = open('tests/files/Var39.rtf')
domTree.openString(file.read())
domTree.parse()


