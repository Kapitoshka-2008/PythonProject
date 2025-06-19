from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Vacancy:
    """Class for working with job vacancies"""
    title: str
    url: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    description: str
    requirements: str
    company_name: str

    def __post_init__(self):
        """Validate and process data after initialization"""
        if not self.salary_from:
            self.salary_from = 0
        if not self.salary_to:
            self.salary_to = 0

    @property
    def average_salary(self) -> int:
        """Calculate average salary"""
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) // 2
        return self.salary_from or self.salary_to or 0

    def __lt__(self, other: 'Vacancy') -> bool:
        """Compare vacancies by salary"""
        return self.average_salary < other.average_salary

    def __gt__(self, other: 'Vacancy') -> bool:
        """Compare vacancies by salary"""
        return self.average_salary > other.average_salary

    def __eq__(self, other: 'Vacancy') -> bool:
        """Compare vacancies by salary"""
        return self.average_salary == other.average_salary

    @classmethod
    def cast_to_object_list(cls, data: List[Dict[str, Any]]) -> List['Vacancy']:
        """Convert JSON data to list of Vacancy objects"""
        vacancies = []
        for item in data:
            # Handle case when salary is None
            salary = item.get('salary', {}) or {}
            vacancy = cls(
                title=item.get('name', ''),
                url=item.get('alternate_url', ''),
                salary_from=salary.get('from'),
                salary_to=salary.get('to'),
                description=item.get('description', ''),
                requirements=item.get('snippet', {}).get('requirement', ''),
                company_name=item.get('employer', {}).get('name', '')
            )
            vacancies.append(vacancy)
        return vacancies

    def to_dict(self) -> Dict[str, Any]:
        """Convert vacancy to dictionary for storage"""
        return {
            'title': self.title,
            'url': self.url,
            'salary_from': self.salary_from,
            'salary_to': self.salary_to,
            'description': self.description,
            'requirements': self.requirements,
            'company_name': self.company_name
        }
