# File exporter module - saves news organized by topics

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from logger_config import logger
from config import OUTPUT_DIR, OUTPUT_FORMAT

class FileExporter:
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)
        self.index = {}

    def export_news(self, news_items: List[Dict], topic: str):
        """Save news items to file organized by topic."""
        if not news_items:
            return

        # Create topic directory
        topic_dir = self.output_dir / self._sanitize_filename(topic)
        topic_dir.mkdir(exist_ok=True)

        for news in news_items:
            filename = self._generate_filename(news, topic)
            filepath = topic_dir / filename

            if OUTPUT_FORMAT == 'markdown':
                content = self._format_markdown(news)
            elif OUTPUT_FORMAT == 'json':
                content = json.dumps(news, ensure_ascii=False, indent=2)
            else:
                content = self._format_text(news)

            try:
                filepath.write_text(content, encoding='utf-8')
                logger.debug(f"Saved: {filepath}")

                # Update index
                self._update_index(filepath, news, topic)

            except Exception as e:
                logger.error(f"Error saving {filepath}: {e}")

    def _generate_filenametimestamp = datetime.now().isoformat().replace(':', '-')  # '2026-05-22T15-31-30.636680'
filename = f"{timestamp}_{org_name}_{title}.md"

        # Sanitize
        org_safe = self._sanitize_filename(org)
        title_safe = self._sanitize_filename(title)

        if OUTPUT_FORMAT == 'json':
            ext = 'json'
        else:
            ext = 'md' if OUTPUT_FORMAT == 'markdown' else 'txt'

        return f"{date}_{org_safe}_{title_safe}.{ext}"

    def _sanitize_filename(self, filename: str) -> str:
        """Remove invalid filename characters."""
        import re
        # Keep only alphanumeric, spaces, hyphens, underscores
        sanitized = re.sub(r'[^\w\s\-]', '', filename)
        sanitized = re.sub(r'[\s]+', '_', sanitized)
        return sanitized[:50]

    def _format_markdown(self, news: Dict) -> str:
        """Format news as Markdown."""
        date = news.get('published_date', '')
        org = news.get('source_org', 'Unknown')
        title = news.get('title', 'No title')
        url = news.get('url', '#')
        source_url = news.get('source_url', '#')
        content = news.get('content', '')

        return f"""# {title}

**Дата:** {date}
**Организация:** {org}
**Источник:** [{source_url}]({source_url})
**Ссылка на новость:** [{url}]({url})

---

## Содержание

{content}
"""

    def _format_text(self, news: Dict) -> str:
        """Format news as plain text."""
        date = news.get('published_date', '')
        org = news.get('source_org', 'Unknown')
        title = news.get('title', 'No title')
        url = news.get('url', '#')
        content = news.get('content', '')

        return f"""НОВОСТЬ
{'='*80}

Заголовок: {title}
Дата: {date}
Организация: {org}
Источник: {url}

{'-'*80}

{content}
"""

    def _update_index(self, filepath: Path, news: Dict, topic: str):
        """Update central index file."""
        relative_path = filepath.relative_to(self.output_dir)

        entry = {
            'path': str(relative_path),
            'topic': topic,
            'title': news.get('title', ''),
            'date': news.get('published_date', ''),
            'org': news.get('source_org', ''),
            'url': news.get('url', ''),
        }

        self.index[str(filepath)] = entry

    def save_index(self):
        """Save central index as JSON."""
        index_file = self.output_dir / 'index.json'
        try:
            index_file.write_text(
                json.dumps(self.index, ensure_ascii=False, indent=2, default=str),
                encoding='utf-8'
            )
            logger.info(f"Saved index: {index_file}")
        except Exception as e:
            logger.error(f"Error saving index: {e}")

    def create_topic_summary(self, topic: str, count: int):
        """Create summary file for topic."""
        summary_file = self.output_dir / _("{}_summary.txt".format(self._sanitize_filename(topic)))
        try:
            summary_file.write_text(
                f"Тема: {topic}\nНайдено новостей: {count}\nДата обновления: {datetime.now().isoformat()}\n",
                encoding='utf-8'
            )
        except Exception as e:
            logger.error(f"Error creating summary: {e}")
