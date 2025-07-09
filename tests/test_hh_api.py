import unittest
from unittest.mock import patch, Mock
from src.hh_api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    @patch('src.hh_api.requests.get')
    def test_get_vacancies(self, mock_get):
        # Настраиваем mock для requests.get
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            {"items": [{"id": 1}, {"id": 2}], "pages": 2},
            {"items": [], "pages": 2}
        ]
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("python")
        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0]["id"], 1)
        self.assertEqual(vacancies[1]["id"], 2)

    @patch('src.hh_api.requests.get')
    def test_get_vacancies_api_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        api = HeadHunterAPI()
        vacancies = api.get_vacancies("python")
        self.assertEqual(vacancies, [])


if __name__ == "__main__":
    unittest.main()
