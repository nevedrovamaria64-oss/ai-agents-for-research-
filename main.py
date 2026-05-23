# Main orchestration module

import asyncio
from pathlib import Path
from datetime import datetime
from collections import defaultdict

from logger_config import logger
from config import ORGANIZATIONS_FILE, OUTPUT_DIR
from excel_loader import load_organizations
from crawler import NewsCrawler
from news_parser import NewsParser
from post_processor import NewsPostProcessor
from file_exporter import FileExporter

async def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("NEWS AGENT STARTED")
    logger.info("=" * 80)

    start_time = datetime.now()

    # Step 1: Load organizations
    logger.info("Step 1: Loading organizations...")
    organizations = load_organizations(ORGANIZATIONS_FILE)

    if not organizations:
        logger.error("No organizations loaded. Check organizations.xlsx")
        return

    logger.info(f"✓ Loaded {len(organizations)} organizations")

    # Step 2: Initialize components
    post_processor = NewsPostProcessor()
    exporter = FileExporter(OUTPUT_DIR)
    all_news = []
    stats = defaultdict(int)

    # Step 3: Crawl and parse news
    logger.info("Step 2: Crawling and parsing news...")

    async with NewsCrawler() as crawler, NewsParser() as parser:
        for org in organizations:  # Process all organizations
            org_name = org['name']
            org_url = org['url']
            org_categories = org['categories']

            logger.info(f"\n  Processing: {org_name}")

            try:
                # Find news sources
                news_urls = await crawler.find_news_sources(org_url, org_name)
                stats['urls_found'] += len(news_urls)

                if not news_urls:
                    logger.warning(f"    No news sources found for {org_name}")
                    continue

                # Parse each news source
                for news_url in news_urls:
                    try:
                        news_items = await parser.parse_url(news_url, org_name)
                        stats['news_parsed'] += len(news_items)

                        for item in news_items:
                            news_dict = item.to_dict()
                            all_news.append(news_dict)
                            stats['news_total'] += 1

                    except Exception as e:
                        logger.error(f"    Error parsing {news_url}: {e}")

            except Exception as e:
                logger.error(f"  Error processing {org_name}: {e}")

    logger.info(f"\n✓ Parsed {stats['news_total']} news items")

    # Step 4: Post-process and classify
    logger.info("Step 3: Post-processing and classifying news...")
    news_by_topic = post_processor.process_news(all_news)

    # Step 5: Export by topic
    logger.info("Step 4: Exporting news by topics...")

    for topic, news_list in sorted(news_by_topic.items()):
        logger.info(f"  {topic}: {len(news_list)} items")
        exporter.export_news(news_list, topic)
        stats[f'topic_{topic}'] = len(news_list)

    # Save index
    exporter.save_index()

    # Step 6: Report
    logger.info("\n" + "=" * 80)
    logger.info("REPORT")
    logger.info("=" * 80)
    logger.info(f"Organizations processed: {len(organizations)}")
    logger.info(f"News sources found: {stats['urls_found']}")
    logger.info(f"News items parsed: {stats['news_total']}")
    logger.info(f"Topics found: {len(news_by_topic)}")
    logger.info(f"Output directory: {OUTPUT_DIR}")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f"Duration: {duration:.2f} seconds")
    logger.info("=" * 80)
    logger.info("NEWS AGENT COMPLETED")
    logger.info("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
