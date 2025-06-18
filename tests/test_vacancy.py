import unittest
from src.vacancy import Vacancy

class TestVacancy(unittest.TestCase):
    def setUp(self):
        self.vacancy1 = Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/1",
            salary_from=100000,
            salary_to=150000,
            description="Python developer position",
            requirements="Python, Django",
            company_name="Test Company"
        )
        
        self.vacancy2 = Vacancy(
            title="Senior Python Developer",
            url="https://hh.ru/vacancy/2",
            salary_from=200000,
            salary_to=250000,
            description="Senior Python developer position",
            requirements="Python, Django, Flask",
            company_name="Test Company 2"
        )
        
        self.vacancy3 = Vacancy(
            title="Junior Python Developer",
            url="https://hh.ru/vacancy/3",
            salary_from=None,
            salary_to=None,
            description="Junior Python developer position",
            requirements="Python basics",
            company_name="Test Company 3"
        )
    
    def test_salary_comparison(self):
        """Test salary comparison between vacancies"""
        self.assertLess(self.vacancy1, self.vacancy2)
        self.assertGreater(self.vacancy2, self.vacancy1)
        self.assertEqual(self.vacancy1, self.vacancy1)
    
    def test_average_salary(self):
        """Test average salary calculation"""
        self.assertEqual(self.vacancy1.average_salary, 125000)
        self.assertEqual(self.vacancy2.average_salary, 225000)
        self.assertEqual(self.vacancy3.average_salary, 0)
    
    def test_cast_to_object_list(self):
        """Test conversion from JSON to Vacancy objects"""
        json_data = [{
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/1",
            "salary": {"from": 100000, "to": 150000},
            "description": "Python developer position",
            "snippet": {"requirement": "Python, Django"},
            "employer": {"name": "Test Company"}
        }]
        
        vacancies = Vacancy.cast_to_object_list(json_data)
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].title, "Python Developer")
        self.assertEqual(vacancies[0].salary_from, 100000)
        self.assertEqual(vacancies[0].salary_to, 150000)

if __name__ == '__main__':
    unittest.main() 