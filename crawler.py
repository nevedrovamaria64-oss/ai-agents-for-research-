# Crawler module - finds news sources on websites

import aiohttp
import asyncio
from typing import List, Optional, Set
from bs4 import BeautifulSoup
import feedparser
from urllib.parse import urljoin, urlparse
from logger_config import logger
from url_utils import normalize_url, build_absolute_url, extract_urls_from_html, is_news_url
from config import NEWS_PATTERNS, RSS_PATTERNS, REQUEST_TIMEOUT

class NewsCrawler:
    def __init__(self):
        self.session = None
        self.timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        # Extended patterns for news discovery
        self.extended_news_patterns = NEWS_PATTERNS + [
            "/blog",
            "/posts",
            "/статьи",
            "/новости",
            "/пресс",
            "/события",
            "/интервью",
            "/репортаж",
            "?page=news",
            "?page=blog",
            "?type=news",
            "/index.php",
        ]
        # CMS-specific API endpoints
        self.cms_apis = [
            "/wp-json/wp/v2/posts",  # WordPress
            "/api/posts",
            "/api/news",
            "/api/articles",
            "/graphql",
        ]

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def find_news_sources(self, org_url: str, org_name: str) -> List[str]:
        """
        Find news pages on website.
        Returns list of URLs with potential news.
        """
        normalized_url = normalize_url(org_url)
        if not normalized_url:
            logger.warning(f"Invalid URL for {org_name}: {org_url}")
            return []

        logger.info(f"Crawling {org_name} ({normalized_url})...")

        news_sources: Set[str] = set()

        # 1. Auto-discover RSS feeds from HTML headers
        rss_feeds = await self._discover_rss_feeds(normalized_url)
        news_sources.update(rss_feeds)

        # 2. Check for standard RSS patterns
        standard_rss = await self._find_rss_feeds(normalized_url)
        news_sources.update(standard_rss)

        # 3. Parse sitemap for news sections
        sitemap_urls = await self._parse_sitemap(normalized_url)
        news_sources.update(sitemap_urls)

        # 4. Check for CMS API endpoints
        cms_endpoints = await self._find_cms_endpoints(normalized_url)
        news_sources.update(cms_endpoints)

        # 5. Find news pages by crawling site
        news_pages = await self._find_news_pages(normalized_url)
        news_sources.update(news_pages)

        logger.info(f"Found {len(news_sources)} news sources for {org_name}")
        return list(news_sources)[:20]  # Limit to 20 sources

    async def _discover_rss_feeds(self, base_url: str) -> Set[str]:
        """Auto-discover RSS feeds from HTML link tags."""
        feeds: Set[str] = set()
        try:
            html = await self._fetch_html(base_url)
            if not html:
                return feeds

            soup = BeautifulSoup(html, 'html.parser')

            # Look for RSS/Atom link tags in <head>
            rss_links = soup.find_all('link', attrs={
                'rel': lambda x: x and ('alternate' in x.lower() or 'feed' in x.lower()),
                'type': lambda x: x and ('rss' in x.lower() or 'atom' in x.lower() or 'feed' in x.lower())
            })

            for link in rss_links:
                href = link.get('href')
                if href:
                    feed_url = urljoin(base_url, href)
                    feeds.add(feed_url)
                    logger.debug(f"Auto-discovered RSS: {feed_url}")

        except Exception as e:
            logger.debug(f"Error discovering RSS feeds from {base_url}: {e}")

        return feeds

    async def _parse_sitemap(self, base_url: str) -> Set[str]:
        """Parse sitemap.xml for potential news sections."""
        urls: Set[str] = set()
        try:
            # Try common sitemap locations
            sitemap_urls = [
                urljoin(base_url, '/sitemap.xml'),
                urljoin(base_url, '/sitemap_index.xml'),
                urljoin(base_url, '/sitemap-news.xml'),
            ]

            for sitemap_url in sitemap_urls:
                content = await self._fetch_html(sitemap_url)
                if not content:
                    continue

                soup = BeautifulSoup(content, 'xml')

                # Extract URLs from sitemap
                for loc in soup.find_all('loc'):
                    url = loc.get_text()
                    # Check if URL contains news-related keywords
                    if any(keyword in url.lower() for keyword in ['news', 'blog', 'press', 'article', 'post', 'новост', 'статья', 'пресс']):
                        urls.add(url)
                        logger.debug(f"Found in sitemap: {url}")

        except Exception as e:
            logger.debug(f"Error parsing sitemap for {base_url}: {e}")

        return urls

    async def _find_cms_endpoints(self, base_url: str) -> Set[str]:
        """Check for CMS-specific API endpoints."""
        endpoints: Set[str] = set()

        for api_path in self.cms_apis:
            api_url = urljoin(base_url, api_path)
            if await self._url_exists(api_url):
                endpoints.add(api_url)
                logger.debug(f"Found CMS endpoint: {api_url}")

        return endpoints

    async def _find_rss_feeds(self, base_url: str) -> Set[str]:
        """Find RSS feed URLs using standard patterns."""
        feeds: Set[str] = set()
        for pattern in RSS_PATTERNS:
            feed_url = base_url.rstrip('/') + pattern
            if await self._url_exists(feed_url):
                feeds.add(feed_url)
                logger.debug(f"Found RSS feed: {feed_url}")

        return feeds

    async def _find_news_pages(self, base_url: str) -> Set[str]:
        """Find news pages by checking extended patterns."""
        urls: Set[str] = set()
        try:
            html = await self._fetch_html(base_url)
            if not html:
                return urls

            soup = BeautifulSoup(html, 'html.parser')
            page_urls = extract_urls_from_html(html, base_url)

            # Filter news URLs
            for url in page_urls:
                if any(pattern in url.lower() for pattern in self.extended_news_patterns):
                    urls.add(url)
                    logger.debug(f"Found news pattern: {url}")

            # Also check direct patterns
            base_parts = urlparse(base_url)
            for pattern in self.extended_news_patterns:
                pattern_url = f"{base_parts.scheme}://{base_parts.netloc}{pattern}"
                if await self._url_exists(pattern_url):
                    urls.add(pattern_url)
                    logger.debug(f"Found news page: {pattern_url}")

        except Exception as e:
            logger.debug(f"Error finding news pages on {base_url}: {e}")

        return urls

    async def _fetch_html(self, url: str) -> Optional[str]:
        """Fetch HTML content from URL."""
        try:
            if not self.session:
                raise RuntimeError("Session not initialized")

            async with self.session.get(url, allow_redirects=True, ssl=False) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.debug(f"HTTP {response.status} for {url}")
                    return None

        except asyncio.TimeoutError:
            logger.warning(f"Timeout fetching {url}")
            return None
        except Exception as e:
            logger.debug(f"Error fetching {url}: {e}")
            return None

    async def _url_exists(self, url: str) -> bool:
        """Check if URL is accessible."""
        try:
            if not self.session:
                return False

            async with self.session.head(url, allow_redirects=True, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as response:
                return response.status < 400

        except:
            return False

