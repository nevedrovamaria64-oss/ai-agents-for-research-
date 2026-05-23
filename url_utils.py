# URL utilities module

import re
from urllib.parse import urljoin, urlparse
from typing import Optional
from logger_config import logger

def normalize_url(url: str) -> Optional[str]:
    """
    Normalize URL: add https:// if needed, remove trailing slash.
    Returns None if URL is invalid.
    """
    if not url:
        return None

    url = url.strip()

    # Add https:// if no protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # Remove trailing slashes
    url = url.rstrip('/')

    # Validate
    try:
        result = urlparse(url)
        if result.scheme in ['http', 'https'] and result.netloc:
            return url
    except Exception as e:
        logger.debug(f"Invalid URL {url}: {e}")

    return None

def get_domain(url: str) -> Optional[str]:
    """Extract domain from URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return None

def build_absolute_url(base_url: str, relative_url: str) -> Optional[str]:
    """Convert relative URL to absolute."""
    try:
        return urljoin(base_url, relative_url)
    except:
        return None

def is_news_url(url: str, patterns: list) -> bool:
    """Check if URL matches news patterns."""
    url_lower = url.lower()
    return any(pattern.lower() in url_lower for pattern in patterns)

def extract_urls_from_html(html: str, base_url: str) -> list:
    """Extract all URLs from HTML content."""
    # Simple regex pattern for URLs
    url_pattern = r'href=["\']((?:https?://|/)[^\s"\'<>]+)["\']'
    matches = re.findall(url_pattern, html, re.IGNORECASE)

    urls = []
    for match in matches:
        absolute_url = build_absolute_url(base_url, match)
        if absolute_url:
            urls.append(absolute_url)

    return list(set(urls))  # Remove duplicates
