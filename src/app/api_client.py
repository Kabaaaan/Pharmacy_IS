import requests
from typing import Optional, List, Dict
from datetime import date

class ApiClient:
    BASE_URL = "http://localhost:8000/api/v1"
    
    @classmethod
    def get_all_suppliers(cls) -> List[Dict]:
        response = requests.get(f"{cls.BASE_URL}/supplier")
        response.raise_for_status()
        return response.json()
    

