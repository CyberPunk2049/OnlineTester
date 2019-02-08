from flask import session
from app.database import db
from pyrtfdom.dom import RTFDOM
import re
from app.demonstrator.models import Test, Question, Answer


class TestsRtfdom(RTFDOM):
    # Наследуемый класс, расширяемый методами для обработки тестов
    def get_text(self, curNode=None, attr=None):
        # Медот для получения всех текстовых полей теста списком

        if attr == None:
            attr = []

        if curNode is None:
            curNode = self.rootNode

        if curNode.nodeType == 'text':
            nodeValue = curNode.value
            if len(nodeValue) > 0:
                attr.append(nodeValue)

        if curNode.children:
            for child in curNode.children:
                self.get_text(child, attr)

        return attr

    def test_dict(self):
        # Метод для объединения списка текстовых полей в словарь
        #
        # Пример вывода:
        #
        # {
        #    'variant': '12',
        #    'questions': [
        #        {
        #            'name': 'Задание №33   Регуляция пищеварения',
        #            'text': 'Главными  регуляторными механизмами  пищеварении в толстой кишке являются: ',
        #            'answers': ['гуморальные', 'нервные', 'местные'],
        #            'answers_bool': ['False', 'False', 'True']
        #        },
        #        {
        #            'name': 'Задание №32   Регуляция пищеварения',
        #            'text': 'Выделение какого из перечисленных веществ подавляется низким значением рН в'
        #                    ' полости желудка:',
        #            'answers': ['ГИП', 'соматостатина', 'секретина', 'ХЦК ', 'гастрина'],
        #            'answers_bool': ['False', 'False', 'False', 'False', 'True']}
        #                ]
        # }

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
                            test['questions'][int(value[0]) - 1]['answers_bool'].append(bool(1))
                        else:
                            test['questions'][int(value[0]) - 1]['answers_bool'].append(bool(0))
                i = i + 3
                continue
            i += 1

        return test

    def add_to_database(self, test_theme, test_special, test_num, test_datetime):
        # Добавляет тест из словаря в базу данных
        # TODO: Переписать тест для одного коммита
        test_dict = self.test_dict()

        test_model = Test(
            theme_id=test_theme.id,
            special_id=test_special.id,
            subject_id=session['subject'],
            num=test_num,
            variant=int(test_dict['variant']),
            datetime=test_datetime
        )
        db.session.add(test_model)
        db.session.commit()
        test_id = db.session.query(db.func.max(Test.id)).scalar()
        for question in test_dict['questions']:
            question_model = Question(
                test_id=test_id,
                num=int(question['number']),
                name=question['name'],
                text=question['text']
            )
            db.session.add(question_model)
            db.session.commit()
            question_id = db.session.query(db.func.max(Question.id)).scalar()
            for i, answer in enumerate(question['answers']):
                answer_model = Answer(
                    question_id=question_id,
                    num=i+1,
                    text=answer,
                    value=question['answers_bool'][i]
                )
                db.session.add(answer_model)
            db.session.commit()

