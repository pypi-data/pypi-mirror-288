import requests
from ai12z_api_sdk.ConfigAi import Config

class Ai12zService:
    """
    Ai12z Service class to interact with the Ai12z AI service.
    """
    def __init__(self) -> None:
        config = Config()
        self.base_url = config.getDefaultUrl()
    def health_check(self):

        """
        Check the health status of the Ai12z service.

        Returns:
            dict: A dictionary containing the health status of the service.
        """
        url = f"{self.base_url}/api/healthz"
        response = requests.get(url)
        return response.json()

    def ask_ai(self, query, options):
        """
        Send a query to the Ai12z AI service and retrieve the response.

        Args:
            query (str): The user's query.
            options (Ai12zOptions): Configuration options (including API key, format).

        Returns:
            dict: A dictionary containing the AI's answer.

        Raises:
            Exception: If the API key or query is missing.
        """
        url = f"{self.base_url}/api/askai"
        req_body = {
            "apiKey": options.api_key,
            "query": query,
        }

        if options.format:
            req_body["format"] = options.format

        response = requests.post(url, json=req_body)
        return response.json()

    def search(self, query, options):
        """
        Send a query to the Ai12z AI service for search and retrieve the response.

        Args:
            query (str): The user's query.
            options (Ai12zOptions): Configuration options (including API key, num_docs).

        Returns:
            dict: A dictionary containing the search results.

        Raises:
            Exception: If the API key is missing.
        """
        url = f"{self.base_url}/api/search"
        req_body = {
            "num_docs": options.num_docs if options.num_docs else 10,
            "query": query,
        }

        if options.api_key:
            req_body["apiKey"] = options.api_key

        response = requests.post(url, json=req_body)
        return response.json()

