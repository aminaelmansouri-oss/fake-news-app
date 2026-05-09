import requests
from bs4 import BeautifulSoup


def scrape_article(url: str, timeout: int = 10) -> dict:
    """
    Scrape an article from a URL.
    Returns dict with title, text, and success status.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Remove script/style elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Title
        title = ""
        if soup.find("h1"):
            title = soup.find("h1").get_text(strip=True)
        elif soup.find("title"):
            title = soup.find("title").get_text(strip=True)

        # Article body - try common article containers
        text = ""
        for selector in ["article", "main", '[class*="article"]', '[class*="content"]', "body"]:
            container = soup.select_one(selector)
            if container:
                paragraphs = container.find_all("p")
                text = " ".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30)
                if len(text) > 200:
                    break

        if not text:
            # Fallback: all paragraphs
            paragraphs = soup.find_all("p")
            text = " ".join(p.get_text(strip=True) for p in paragraphs)

        full_text = f"{title} {text}".strip()

        if len(full_text) < 50:
            return {"success": False, "error": "Could not extract meaningful content from this URL."}

        return {
            "success": True,
            "title": title,
            "text": full_text[:5000],  # limit length
            "url": url
        }

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. The website took too long to respond."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Could not connect to the URL. Please check the address."}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP Error: {e.response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"Scraping failed: {str(e)}"}
