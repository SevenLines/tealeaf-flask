from werkzeug.datastructures import FileStorage

from tests import TestCaseBase

from app.storage import Storage


class TestStorage(TestCaseBase):
    def test_url_should_return_correct_url(self):
        f = FileStorage(open(self.test_image_path))
        file_path = Storage.save(f)
        url = Storage.url(file_path)
        print url
        response = self.client.get(url)
        self.assert200(response)
