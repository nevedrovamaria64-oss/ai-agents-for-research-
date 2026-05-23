# Classifier module - categorizes news by topics

from typing import List, Set
from logger_config import logger
from config import GLOBAL_TOPICS

class NewsClassifier:
    def __init__(self, global_topics: dict = None):
        """Initialize classifier with topic keywords."""
        self.global_topics = global_topics or GLOBAL_TOPICS
        self.keyword_index = self._build_keyword_index()

    def _build_keyword_index(self) -> dict:
        """Build index of keywords to topics."""
        index = {}
        for topic, keywords in self.global_topics.items():
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower not in index:
                    index[keyword_lower] = []
                index[keyword_lower].append(topic)
        return index

    def classify(self, text: str, org_categories: List[str] = None) -> Set[str]:
        """
        Classify news by topics using keyword matching.

        Args:
            text: News title + content
            org_categories: Organization's categories from Excel (for boosting relevance)

        Returns:
            Set of relevant topics
        """
        if not text:
            return set()

        text_lower = text.lower()
        matched_topics = set()

        # Match by keywords
        for keyword, topics in self.keyword_index.items():
            if keyword in text_lower:
                matched_topics.update(topics)

        # If org has specific categories, filter or boost results
        if org_categories:
            org_cats_lower = [cat.lower() for cat in org_categories]
            # Give priority to org's own categories
            for topic in list(matched_topics):
                topic_lower = topic.lower()
                for org_cat in org_cats_lower:
                    if org_cat in topic_lower or topic_lower in org_cat:
                        # Keep this topic
                        break

        logger.debug(f"Classified text into {len(matched_topics)} topics: {matched_topics}")
        return matched_topics

    def get_available_topics(self) -> List[str]:
        """Return list of all available topics."""
        return list(self.global_topics.keys())

    def add_custom_keywords(self, topic: str, keywords: List[str]):
        """Add custom keywords for a topic."""
        if topic not in self.global_topics:
            self.global_topics[topic] = []

        self.global_topics[topic].extend(keywords)
        self.keyword_index = self._build_keyword_index()
        logger.info(f"Added {len(keywords)} keywords to topic '{topic}'")
