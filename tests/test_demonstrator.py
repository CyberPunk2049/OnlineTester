from io import BytesIO
from itertools import product


class TestUpload(object):

    def test_correct_upload(self, client, client_auth):
        # Загрузка файлов в демонстраторе должна происходить корректно
        # TODO: После успешной загрузки файлов должно происходить перенаправление на страницу предварительного просмотра

        client_auth.login()
        data = {
            'variant1': (BytesIO(b'asdfasdfweqrfdas'), 'Var22.rtf'),
            'variant2': (BytesIO(b'asdfasdfweqrfdas'), 'Var39.rtf'),
        }
        response = client.post('/demonstrator/upload/', data=data, content_type='multipart/form-data')
        assert response.status_code == 200

    def test_incorrect_extensions(self, client, client_auth):
        # Загружаемые файлы должны иметь расширение .rtf, в противном случае возвращать на окно загрузки,
        # с указанием ошибки
        client_auth.login()
        error = u'Загружаемые файлы должны иметь расширение .rtf'

        ext = ['.rtf', '.pdf', 'asd', '0']
        combinations = product(ext, ext)

        for (ext1, ext2) in combinations:

            data = {
                'num': '1',
                'theme': '1',
                'special': '1',
                'variant1': (BytesIO(b'asdfasdfweqrfdas'), 'Var22'+ext1),
                'variant2': (BytesIO(b'asdfasdfweqrfdas'), 'Var39'+ext2),

            }
            if (ext1, ext2) != ('.rtf', '.rtf'):
                response = client.post('/demonstrator/upload/', data=data, content_type='multipart/form-data')
                assert response.status_code == 200 and bytes(error, encoding='utf-8') in response.data

    def test_incorrect_file(self, client, client_auth):
        # Загружаемые файлы должны иметь структуру теста для корректной загрузки в базу данных, в противном случае
        # возвращать на окно загрузки с указанием ошибки
        pass
