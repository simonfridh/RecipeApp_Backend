import requests

def fetch_html(url: str) -> str:
        headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/136.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(url,headers=headers, timeout=10)
        response.raise_for_status() # throws exception if response contains any error codes
        html = response.text
        return html
