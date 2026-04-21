from bs4 import BeautifulSoup
import requests

class SoupClient:
    def __init__(self, **kwargs):
        self.base_url = kwargs.get("base_url")
        self.session = requests.Session()
    def get_soup(self, **kwargs):
        if "base_url" in kwargs:
            url = f"{self.base_url}{kwargs.get("endpoint")}"
        else:
            url = f"{kwargs.get("endpoint")}"
        headers = kwargs.get("headers")
        response = self.session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup