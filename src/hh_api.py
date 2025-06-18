import requests
from typing import List, Dict, Any
from .abstract_classes import VacancyAPI

class HeadHunterAPI(VacancyAPI):
    """Class for working with HeadHunter API"""
    
    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Get vacancies from HeadHunter API
        
        Args:
            search_query: Search query string
            
        Returns:
            List of vacancy dictionaries
        """
        params = {
            "text": search_query,
            "area": 1,  # 1 is for Russia
            "per_page": 100,
            "page": 0
        }
        
        vacancies = []
        while True:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            if response.status_code != 200:
                break
                
            data = response.json()
            if not data.get("items"):
                break
                
            vacancies.extend(data["items"])
            
            if params["page"] >= data["pages"] - 1:
                break
                
            params["page"] += 1
            
        return vacancies 