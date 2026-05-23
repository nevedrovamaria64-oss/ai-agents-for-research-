# News parser module - extracts news from HTML and RSS

import feedparser
import aiohttp
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from logger_config import logger

class NewsItem:
    def __init__(self, title: str, url: str, content: str, published_date: Optional[datetime],
                 source_org: str, source_url: str):
        self.title = title
        self.url = url
        self.content = content
        self.published_date = published_date or datetime.now()
        self.source_org = source_org
        self.source_url = source_url

    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'url': self.url,
            'content': self.content,
            'published_date': self.published_date.isoformat(),
            'source_org': self.source_org,
            'source_url': self.source_url,
        }

class NewsParser:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def parse_url(self, url: str, org_name: str) -> List[NewsItem]:
        """Parse news from URL (HTML or RSS)."""
        if 'feed' in url.lower() or 'rss' in url.lower():
            return await self._parse_rss(url, org_name)
        else:
            return await self._parse_html(url, org_name)

    async def _parse_rss(self, rss_url: str, org_name: str) -> List[NewsItem]:
        """Parse RSS feed."""
        try:
            feed = feedparser.parse(rss_url)
            news_items = []

            for entry in feed.entries[:20]:  # Limit to 20 items
                title = entry.get('title', 'No title')
                url = entry.get('link', rss_url)
                content = entry.get('summary', '') or entry.get('description', '')
                published_date = self._parse_date(entry.get('published'))

                item = NewsItem(
                    title=title,
                    url=url,
                    content=content,
                    published_date=published_date,
                    source_org=org_name,
                    source_url=rss_url
                )
                news_items.append(item)

            logger.info(f"Parsed {len(news_items)} items from RSS: {rss_url}")
            return news_items

        except Exception as e:
            logger.error(f"Error parsing RSS {rss_url}: {e}")
            return []

    async def _parse_html(self, page_url: str, org_name: str) -> List[NewsItem]:
        """Parse news from HTML page."""
        try:
            html = await self._fetch_html(page_url)
            if not html:
                return []

            soup = BeautifulSoup(html, 'html.parser')
            news_items = []

            # Extended selectors for better coverage
            selectors = [
                'article',
                '.news-item',
                '.post',
                '.article',
                '[class*="news"]',
                '[class*="article"]',
                '[class*="post"]',
                '.entry',
                '.item',
                '.content-item',
                '[class*="card"]',
                '[class*="block"]',
                '.news',
                '.blog-post',
                '.post-item',
                '[class*="news-item"]',
                '[data-type="article"]',
                '[data-type="news"]',
            ]

            found_items = False
            for selector in selectors:
                elements = soup.select(selector)[:30]  # Increased limit to 30

                for element in elements:
                    # Try to extract title
                    title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'a'])
                    if not title_elem:
                        title_elem = element.find(['strong', 'b'])

                    title = title_elem.get_text(strip=True) if title_elem else None
                    if not title or len(title) < 5:
                        continue

                    # Extract URL
                    url_elem = element.find('a')
                    url = None
                    if url_elem and url_elem.get('href'):
                        url = url_elem.get('href')
                        if url.startswith('/'):
                            from urllib.parse import urljoin
                            url = urljoin(page_url, url)
                    else:
                        url = page_url

                    # Extract content/summary
                    content_elem = element.find(['p', 'span', 'div'])
                    content = content_elem.get_text(strip=True)[:500] if content_elem else element.get_text(strip=True)[:500]

                    # Extract date
                    published_date = self._extract_date_from_text(str(element))

                    item = NewsItem(
                        title=title,
                        url=url,
                        content=content,
                        published_date=published_date,
                        source_org=org_name,
                        source_url=page_url
                    )
                    news_items.append(item)

                if news_items:
                    found_items = True
                    break  # Found news, don't try other selectors

            logger.info(f"Parsed {len(news_items)} items from HTML: {page_url}")
            return news_items

        except Exception as e:
            logger.error(f"Error parsing HTML {page_url}: {e}")
            return []

    async def _fetch_html(self, url: str) -> Optional[str]:
        """Fetch HTML content."""
        try:
            if not self.session:
                return None

            async with self.session.get(url, ssl=False, allow_redirects=True) as response:
                if response.status == 200:
                    return await response.text()
                return None

        except Exception as e:
            logger.debug(f"Error fetching {url}: {e}")
            return None

    def _parse_date(self, date_str) -> Optional[datetime]:
        """Parse date string to datetime."""
        if not date_str:
            return None

        try:
            if isinstance(date_str, str):
                return date_parser.parse(date_str)
            else:
                return datetime.fromtimestamp(date_str)
        except:
            return None

    def _extract_date_from_text(self, text: str) -> Optional[datetime]:
        """Extract date from text content."""
        try:
            # Look for common date patterns
            import re
            patterns = [
                r'\d{2}\.\d{2}\.\d{4}',
                r'\d{4}-\d{2}-\d{2}',
                r'\d{2}/\d{2}/\d{4}',
            ]

            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    return date_parser.parse(match.group())

            return None
        except:
            return None
