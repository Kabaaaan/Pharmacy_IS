import requests
from typing import Optional, Dict, Any, Union

class APIClient:
    """
    Универсальный клиент для работы с API
    
    Параметры:
        base_url (str): Базовый URL API
        timeout (int): Таймаут запросов в секундах (по умолчанию 10)
        headers (dict): Заголовки по умолчанию для всех запросов
    """
    def __init__(self, base_url: str, timeout: int = 10, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.headers = headers or {}
        self.session = requests.Session()
        

    def _send_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Optional[Union[Dict[str, Any], str]]:
        """
        Отправка HTTP запроса
        
        Параметры:
            method: HTTP метод (GET, POST, PUT, DELETE и т.д.)
            endpoint: Конечная точка API (например '/users')
            params: Параметры URL
            data: Тело запроса (для form-data)
            json_data: Тело запроса в формате JSON
            headers: Дополнительные заголовки запроса
            
        Возвращает:
            Ответ API в виде словаря или строки, либо None в случае ошибки
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {**self.headers, **(headers or {})}
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            try:
                return response.json()
            except ValueError:
                return response.text
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ошибка при выполнении запроса {method} {url}: {str(e)}")
            return None
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None):
        """GET запрос"""
        return self._send_request('GET', endpoint, params=params, headers=headers)
    
    def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        """POST запрос"""
        return self._send_request('POST', endpoint, data=data, json_data=json_data, headers=headers)
    
    def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        """PUT запрос"""
        return self._send_request('PUT', endpoint, data=data, json_data=json_data, headers=headers)
    
    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None):
        """DELETE запрос"""
        return self._send_request('DELETE', endpoint, headers=headers)
    
    def set_auth_token(self, token: str):
        """Установка токена авторизации"""
        self.headers['Authorization'] = f'Bearer {token}'
    
    def clear_auth_token(self):
        """Удаление токена авторизации"""
        self.headers.pop('Authorization', None)