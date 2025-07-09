import unittest
from main import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies
from src.vacancy import Vacancy


class TestMainFunctions(unittest.TestCase):
    def setUp(self):
        self.vacancies = [
            Vacancy("Python Dev", "url1", 100, 200, "desc python", "python", "comp"),
            Vacancy("Java Dev", "url2", 150, 250, "desc java", "java", "comp"),
            Vacancy("Go Dev", "url3", 200, 300, "desc go", "go", "comp"),
        ]

    def test_filter_vacancies(self):
        filtered = filter_vacancies(self.vacancies, ["python"])
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "Python Dev")
        # Без фильтра
        filtered = filter_vacancies(self.vacancies, [])
        self.assertEqual(len(filtered), 3)

    def test_get_vacancies_by_salary(self):
        ranged = get_vacancies_by_salary(self.vacancies, "120-220")
        self.assertEqual(len(ranged), 2)
        titles = {v.title for v in ranged}
        self.assertIn("Python Dev", titles)
        self.assertIn("Java Dev", titles)
        # Некорректный диапазон
        ranged = get_vacancies_by_salary(self.vacancies, "bad-range")
        self.assertEqual(len(ranged), 3)

    def test_sort_vacancies(self):
        sorted_vac = sort_vacancies(self.vacancies)
        self.assertEqual(sorted_vac[0].title, "Go Dev")
        self.assertEqual(sorted_vac[-1].title, "Python Dev")

    def test_get_top_vacancies(self):
        sorted_vac = sort_vacancies(self.vacancies)
        top = get_top_vacancies(sorted_vac, 2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0].title, "Go Dev")
        self.assertEqual(top[1].title, "Java Dev")


if __name__ == "__main__":
    unittest.main()
