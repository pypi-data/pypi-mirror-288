from abc import ABC, abstractmethod
from typing import Dict, Optional
import requests

from deployit.providers.jenkins.utils.config import Config
from deployit.providers.jenkins.utils.errors import JenkinsConnectionError

class HTTPClient(ABC):
    @abstractmethod
    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict:
        """
        Send a GET request.

        Parameters
        ----------
        url : str
            The URL to send the GET request to.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        dict
            The response JSON.
        """
        pass

    @abstractmethod
    def post(self, url: str, headers: Optional[Dict[str, str]] = None, data: Optional[Dict] = None) -> Dict:
        """
        Send a POST request.

        Parameters
        ----------
        url : str
            The URL to send the POST request to.
        headers : dict, optional
            Optional headers to include in the request.
        data : dict, optional
            Data to include in the POST request.

        Returns
        -------
        dict
            The response JSON.
        """
        pass

    @abstractmethod
    def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict:
        """
        Send a DELETE request.

        Parameters
        ----------
        url : str
            The URL to send the DELETE request to.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        dict
            The response JSON.
        """
        pass

    @abstractmethod
    def put(self, url: str, headers: Optional[Dict[str, str]] = None, data: Optional[Dict] = None) -> Dict:
        """
        Send a PUT request.

        Parameters
        ----------
        url : str
            The URL to send the PUT request to.
        headers : dict, optional
            Optional headers to include in the request.
        data : dict, optional
            Data to include in the PUT request.

        Returns
        -------
        dict
            The response JSON.
        """
        pass

class RequestsHTTPClient(HTTPClient):
    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict:
        """
        Send a GET request using the requests library.

        Parameters
        ----------
        url : str
            The URL to send the GET request to.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        dict
            The response JSON.

        Raises
        ------
        JenkinsError
            If the GET request fails.
        """
        try:
            response = requests.get(url, headers=headers, timeout=Config.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise JenkinsConnectionError(f"GET request failed: {e}")

    def post(self, url: str, headers: Optional[Dict[str, str]] = None, data: Optional[Dict] = None) -> Dict:
        """
        Send a POST request using the requests library.

        Parameters
        ----------
        url : str
            The URL to send the POST request to.
        headers : dict, optional
            Optional headers to include in the request.
        data : dict, optional
            Data to include in the POST request.

        Returns
        -------
        dict
            The response JSON.

        Raises
        ------
        JenkinsError
            If the POST request fails.
        """
        try:
            response = requests.post(url, headers=headers, data=data, timeout=Config.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise JenkinsConnectionError(f"POST request failed: {e}")
        
    def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict:
        """
        Send a DELETE request using the requests library.

        Parameters
        ----------
        url : str
            The URL to send the DELETE request to.
        headers : dict, optional
            Optional headers to include in the request.

        Returns
        -------
        dict
            The response JSON.

        Raises
        ------
        JenkinsError
            If the DELETE request fails.
        """
        try:
            response = requests.delete(url, headers=headers, timeout=Config.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise JenkinsConnectionError(f"DELETE request failed: {e}")
        
    
    def put(self, url: str, headers: Optional[Dict[str, str]] = None, data: Optional[Dict] = None) -> Dict:
        """
        Send a PUT request using the requests library.

        Parameters
        ----------
        url : str
            The URL to send the PUT request to.
        headers : dict, optional
            Optional headers to include in the request.
        data : dict, optional
            Data to include in the PUT request.

        Returns
        -------
        dict
            The response JSON.

        Raises
        ------
        JenkinsError
            If the PUT request fails.
        """
        try:
            response = requests.put(url, headers=headers, data=data, timeout=Config.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise JenkinsConnectionError(f"PUT request failed: {e}")

