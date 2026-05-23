# Excel loader module - reads organizations from Excel file

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from logger_config import logger

def load_organizations(file_path: str) -> List[Dict[str, Any]]:
    """
    Load organizations from Excel file.
    Expected columns: Название, Сайт, Категории
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return []

        df = pd.read_excel(file_path, sheet_name=0)
        logger.info(f"Loaded {len(df)} organizations from {file_path}")

        organizations = []
        for idx, row in df.iterrows():
            org = {
                'name': str(row.get('Название', 'Unknown')).strip(),
                'url': str(row.get('Сайт', '')).strip(),
                'categories': parse_categories(str(row.get('Категории', ''))),
                'description': str(row.get('Описание', '')).strip(),
            }

            # Only add if URL is valid
            if org['url'] and org['url'].lower() not in ['н/д', 'нет', '']:
                organizations.append(org)

        logger.info(f"Successfully parsed {len(organizations)} organizations with valid URLs")
        return organizations

    except Exception as e:
        logger.error(f"Error loading organizations: {e}")
        return []

def parse_categories(categories_str: str) -> List[str]:
    """Parse comma-separated categories string into list."""
    if not categories_str or categories_str.lower() in ['н/д', 'нет', '']:
        return []

    return [cat.strip() for cat in categories_str.split(',') if cat.strip()]

def validate_url(url: str) -> bool:
    """Check if URL is valid."""
    if not url or url.lower() in ['н/д', 'нет']:
        return False
    return url.startswith('http://') or url.startswith('https://')
