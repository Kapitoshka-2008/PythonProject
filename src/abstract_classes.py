from abc import ABC, abstractmethod
from typing import List, Dict, Any


class VacancyAPI(ABC):
    """Abstract class for working with job vacancy APIs"""

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """Get vacancies from the API based on search query"""
        pass


class Storage(ABC):
    """Abstract class for storing vacancy data"""

    @abstractmethod
    def add_vacancy(self, vacancy: 'Vacancy') -> None:
        """Add a vacancy to storage"""
        pass

    @abstractmethod
    def get_vacancies(self, **criteria) -> List['Vacancy']:
        """Get vacancies from storage based on criteria"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: 'Vacancy') -> None:
        """Delete a vacancy from storage"""
        pass
