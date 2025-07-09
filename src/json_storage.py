import json
import os
from typing import List, Dict, Any
from .abstract_classes import Storage
from .vacancy import Vacancy


class JSONSaver(Storage):
    """Class for saving vacancies to JSON file"""

    def __init__(self, filename: str = "vacancies.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create file if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _read_vacancies(self) -> List[Dict[str, Any]]:
        """Read vacancies from file"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Write vacancies to file"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Add vacancy to storage, avoiding duplicates by url"""
        vacancies = self._read_vacancies()
        # Проверка на дублирование по url
        if any(v.get('url') == vacancy.url for v in vacancies):
            return  # Не добавлять дубликат
        vacancies.append(vacancy.to_dict())
        self._write_vacancies(vacancies)

    def get_vacancies(self, **criteria) -> List[Vacancy]:
        """Get vacancies from storage based on criteria"""
        vacancies = self._read_vacancies()
        result = []

        for vacancy_dict in vacancies:
            matches = True
            for key, value in criteria.items():
                if key not in vacancy_dict or vacancy_dict[key] != value:
                    matches = False
                    break

            if matches:
                result.append(Vacancy(
                    title=vacancy_dict['title'],
                    url=vacancy_dict['url'],
                    salary_from=vacancy_dict['salary_from'],
                    salary_to=vacancy_dict['salary_to'],
                    description=vacancy_dict['description'],
                    requirements=vacancy_dict['requirements'],
                    company_name=vacancy_dict['company_name']
                ))

        return result

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Delete vacancy from storage"""
        vacancies = self._read_vacancies()
        vacancies = [v for v in vacancies if v['url'] != vacancy.url]
        self._write_vacancies(vacancies)
