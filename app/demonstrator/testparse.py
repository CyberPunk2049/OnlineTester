from flask import session, current_app
from app.database import db
from pyrtfdom.dom import RTFDOM
import re
from app.demonstrator.models import Test, Question, Answer
import datetime
import os


class TestsRtfdom(RTFDOM):
    # Наследуемый класс, расширяемый методами для обработки тестов

    def get_text(self, cur_node=None, text_array=None, image_dict=None):
        # Медот для получения всех текстовых полей теста списком
        if text_array is None:
            text_array = []

        if image_dict is None:
            image_dict = {}

        if cur_node is None:
            cur_node = self.rootNode

        if cur_node.nodeType == 'img':
            for text in reversed(text_array):
                if re.match(r'Задание №\d{1,2}', text):
                    image_dict[str((re.findall(r'Задание №(\d{1,2})', text)[0]))] = cur_node.value
                    break

        if cur_node.nodeType == 'text':
            node_value = cur_node.value
            if len(node_value) > 0:
                if re.search(r'\d\)', node_value) and re.match(r'\d\)', node_value) is None:
                    values = re.split(r'\d\)', node_value, maxsplit=1)
                    text_array.append(values[0])
                    text_array.append(cur_node.value[len(values[0]):])
                else:
                    text_array.append(node_value)

        if cur_node.children:
            for child in cur_node.children:
                self.get_text(child, text_array, image_dict)

        return [text_array, image_dict]

    def test_dict_version_1(self):
        # Метод для объединения списка текстовых полей в словарь(старая версия тестов)
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

        [test_text, test_images] = self.get_text()
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
                    'text': test_text[i + 1],
                    'img_path': '',
                    'answers': [],
                    'answers_bool': []
                }
                answers = re.split(r'\d\)', test_text[i + 2])
                for answer in answers[1:]:
                    question['answers'].append(answer)
                test['questions'].append(question)
                i = i + 3
                continue
            if re.match(r'Ответы:', test_text[i]):
                answer_values = re.split(r'#', test_text[i + 2])[1:]
                for answer_value in answer_values:
                    value = re.split(r' \(1 б.\)', answer_value)
                    for l in range(0, len(test['questions'][int(value[0]) - 1]['answers'])):
                        if str(l + 1) in re.findall(r'\d', value[1]):
                            test['questions'][int(value[0]) - 1]['answers_bool'].append(bool(1))
                        else:
                            test['questions'][int(value[0]) - 1]['answers_bool'].append(bool(0))
                i = i + 3
                continue
            i += 1

        return test

    def test_dict_version_0(self):
        # Метод для объединения списка текстовых полей в словарь(новая версия тестов)
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

        [test_text, test_images] = self.get_text()
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
                    'text': test_text[i + 1],
                    'img_path': '',
                    'answers': [],
                    'answers_bool': []
                }
                if str(question['number']) in test_images.keys():
                    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') \
                               + str(test['variant']) + str(question['number']) + '.png'
                    question['img_path'] = filename

                    with open(os.path.join(current_app.root_path, current_app.config['MEDIA_FOLDER'],
                                           question['img_path']), 'bw') as img:
                        img.write(test_images[str(question['number'])])
                answers = re.split(r'\d\)', test_text[i + 2])
                for answer in answers[1:]:
                    question['answers'].append(answer)
                test['questions'].append(question)
                i = i + 3
                continue
            if re.match(r'Ответы:', test_text[i]):
                answer_values = re.split(r'#', test_text[i + 1])[1:]
                for answer_value in answer_values:
                    value = re.split(r' \(1 б.\)', answer_value)
                    for l in range(0, len(test['questions'][int(value[0]) - 1]['answers'])):
                        if str(l + 1) in re.findall(r'\d', value[1]):
                            test['questions'][int(value[0]) - 1]['answers_bool'].append(bool(1))
                        else:
                            test['questions'][int(value[0]) - 1]['answers_bool'].append(bool(0))
                i = i + 3
                continue
            i += 1

        return test

    def version_selection(self, test_version):
        # Определяет версию теста для загрузки вызывает нужный загрузчик словаря
        if test_version == 0:
            return self.test_dict_version_0()
        elif test_version == 1:
            return self.test_dict_version_1()

    def add_to_database(self, test_theme, test_special, test_num, test_datetime, test_version):
        # Добавляет тест из словаря в базу данных
        # TODO: Переписать тест для одного коммита
        test_dict = self.version_selection(test_version)

        test_model = Test(
            theme_id=test_theme.id,
            special_id=test_special.id,
            subject_id=session['subject'],
            num=test_num,
            variant=int(test_dict['variant']),
            datetime=test_datetime,
        )
        db.session.add(test_model)
        #db.session.commit()
        test_id = db.session.query(db.func.max(Test.id)).scalar()
        for question in test_dict['questions']:
            question_model = Question(
                test_id=test_id,
                num=int(question['number']),
                name=question['name'],
                text=question['text'],
                img_path=question['img_path']
            )
            db.session.add(question_model)
            #db.session.commit()
            question_id = db.session.query(db.func.max(Question.id)).scalar()
            for i, answer in enumerate(question['answers']):
                answer_model = Answer(
                    question_id=question_id,
                    num=i + 1,
                    text=answer,
                    value=question['answers_bool'][i]
                )
                db.session.add(answer_model)
            db.session.commit()
