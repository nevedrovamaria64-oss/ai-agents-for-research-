# Post-processor module - enhanced classification and export

from typing import List, Dict
from classifier import NewsClassifier
from logger_config import logger

class NewsPostProcessor:
    """
    Post-processes parsed news items:
    - Applies classifier to group news by topics
    - Handles multi-topic assignment
    - Ensures all news gets categorized (including 'Без категории')
    """

    def __init__(self):
        self.classifier = NewsClassifier()

    def process_news(self, news_items: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Process news items and group by topics.

        Args:
            news_items: List of parsed news dictionaries

        Returns:
            Dict mapping topic -> list of news items in that topic
        """
        news_by_topic = {}
        classified_count = 0
        unclassified_count = 0

        for news in news_items:
            # Extract text for classification
            text = f"{news.get('title', '')} {news.get('content', '')}"
            org_categories = news.get('source_org', '').split(',')

            # Classify
            topics = self.classifier.classify(text, org_categories)

            # If no topics found, assign to default category
            if not topics:
                topics = {'Без категории'}
                unclassified_count += 1
            else:
                classified_count += 1

            # Add to all matching topics
            for topic in topics:
                if topic not in news_by_topic:
                    news_by_topic[topic] = []
                news_by_topic[topic].append(news)

        logger.info(f"Post-processed {len(news_items)} items: {classified_count} classified, {unclassified_count} unclassified")
        logger.info(f"Topics found: {len(news_by_topic)}")

        return news_by_topic

    def get_summary(self, news_by_topic: Dict[str, List[Dict]]) -> Dict:
        """Get summary statistics."""
        return {
            'total_items': sum(len(items) for items in news_by_topic.values()),
            'topics_count': len(news_by_topic),
            'topics': {topic: len(items) for topic, items in news_by_topic.items()}
        }
