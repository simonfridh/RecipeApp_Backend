import requests
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

class HTMLFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "RecipeOptimizer/1.0",
            "Accept-Language": "en-US,en;q=0.9",
        })

    def fetch(self, url: str) -> str:
        self._check_robotstxt(url)
        response = self.session.get(url, timeout=10)
        response.raise_for_status() # throws exception if response contains any error codes
        html = response.text
        return html

    # Robots.txt is a file commonly found on websites that tells web scrapers or other bots if they are allowed
    # to visit certain pages on their website. Here i check if the website disallows access to the url that was
    # given by the user.
    def _check_robotstxt(self, url: str):
        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + "://" + parsed_url.netloc
        robots_url = base_url + "/robots.txt"

        robots_response = self.session.get(robots_url, timeout=10)
        if robots_response.status_code == 404: #No robots.txt found
            return
        if robots_response.status_code != 200:
            raise PermissionError("could not access robots.txt") #Robots.txt exists but access was blocked

        robot_file_parser = RobotFileParser()
        robot_file_parser.parse(robots_response.text.splitlines())
        if not robot_file_parser.can_fetch("RecipeOptimizer", url):
            raise PermissionError("Website has blocked access in robots.txt")

        return