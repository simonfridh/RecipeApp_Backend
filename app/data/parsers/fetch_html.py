import requests
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

def fetch_html(url: str) -> str:
        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + "://" + parsed_url.netloc
        robots_url = base_url + "/robots.txt"

        headers = {
            "User-Agent": "RecipeOptimizer/1.0",
            "Accept-Language": "en-US,en;q=0.9",
        }

        # Robots.txt is a file commonly found on websites that tells web scrapers or other bots if they are allowed
        # to visit certain pages on their website. Here i check if the website disallows access to the url that was
        # given by the user.
        robots_response = requests.get(robots_url, headers=headers, timeout=10)
        if robots_response.status_code == 200:
            robot_file_parser = RobotFileParser()
            robot_file_parser.parse(robots_response.text.splitlines())
            if not robot_file_parser.can_fetch("RecipeOptimizer", url):
                raise PermissionError("Website has blocked access in robots.txt")
        elif robots_response.status_code == 404: pass
        else: raise PermissionError("could not access robots.txt")

        response = requests.get(url,headers=headers, timeout=10)
        response.raise_for_status() # throws exception if response contains any error codes
        html = response.text
        return html
