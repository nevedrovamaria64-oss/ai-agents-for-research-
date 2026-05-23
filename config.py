# News Agent - Configuration Module

import os
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "news_output"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Excel file
ORGANIZATIONS_FILE = DATA_DIR / "organizations.xlsx"

# Global categories/topics
GLOBAL_TOPICS = {
    "Мониторинг инфраструктуры": ["трубопровод", "инспекция", "ROV", "мониторинг", "инфраструктура", "диагностика", "обслуживание", "техническое", "контроль", "система мониторинга"],
    "Чрезвычайные ситуации": ["спасение", "ПСР", "аварийно", "чрезвычайн", "спасательн", "катастроф", "авария", "инцидент", "чс"],
    "Энергетический сектор": ["газ", "нефть", "энергия", "ТЭК", "добыча", "шельф", "углеводород", "топливо", "энергоносител"],
    "Наука и образование": ["исследования", "учебное", "научно", "университет", "институт", "образование", "разработка", "инновация", "технология"],
    "Безопасность": ["безопасность", "оборон", "защита", "военн", "боевой", "безопасности", "охран"],
    "Экология и мониторинг": ["экология", "окружающая среда", "мониторинг", "акватория", "загрязнение", "воды", "окружающ"],
    "Связь и телекоммуникации": ["связь", "навигация", "телеком", "коммуникация", "сигнал", "спутник"],
    "Транспорт и логистика": ["логистик", "транспорт", "судост", "верфь", "доставка", "корабль", "судно", "грузоперевозка"],
    "Аквакультура и рыболовство": ["рыболовство", "аквакультур", "рыб", "морепродукт", "аквакультура"],
    "Новости": ["новост", "событи", "объявлени", "информаци", "сообщени", "пресс", "анонс", "данн"],
}

# Parser settings
REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# News source patterns - expanded for better discovery
NEWS_PATTERNS = [
    "/news",
    "/press",
    "/media",
    "/blog",
    "/novosti",
    "/press-center",
    "/news-and-events",
    "/publications",
    "?page=news",
    "/articles",
    "/updates",
    "/events",
    "/posts",
    "/статьи",
    "/новости",
    "/пресс-центр",
    "/блог",
    "/интервью",
    "/репортажи",
    "/события",
    "/обновления",
    "/медиа-центр",
    "/news-archive",
    "/all-news",
    "/latest-news",
    "/company/news",
    "/about/news",
    "/press-release",
    "/announcement",
    "/news-details",
]

RSS_PATTERNS = [
    "/feed",
    "/rss",
    "/news.rss",
    "/feed.xml",
    "/rss.xml",
]

# Logging
LOG_FILE = LOGS_DIR / "news_agent.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Scheduling
SCHEDULE_INTERVAL = "daily"  # "daily", "weekly", or "manual"
SCHEDULE_TIME = "09:00"  # HH:MM format

# Output file format
OUTPUT_FORMAT = "markdown"  # "markdown", "txt", or "json"
