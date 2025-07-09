import unittest
import os
import json
from src.json_storage import JSONSaver
from src.vacancy import Vacancy


class TestJSONSaver(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_vacancies.json'
        # Удаляем файл, если он остался от предыдущих запусков
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.saver = JSONSaver(filename=self.test_file)
        self.vacancy = Vacancy(
            title="Python Dev",
            url="url1",
            salary_from=100,
            salary_to=200,
            description="desc python",
            requirements="python",
            company_name="comp"
        )

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_and_get_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        vacancies = self.saver.get_vacancies()
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].title, "Python Dev")

    def test_no_duplicate_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        self.saver.add_vacancy(self.vacancy)
        vacancies = self.saver.get_vacancies()
        self.assertEqual(len(vacancies), 1)

    def test_delete_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        self.saver.delete_vacancy(self.vacancy)
        vacancies = self.saver.get_vacancies()
        self.assertEqual(len(vacancies), 0)

    def test_get_vacancies_with_criteria(self):
        self.saver.add_vacancy(self.vacancy)
        result = self.saver.get_vacancies(title="Python Dev")
        self.assertEqual(len(result), 1)
        result = self.saver.get_vacancies(title="Not exist")
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
