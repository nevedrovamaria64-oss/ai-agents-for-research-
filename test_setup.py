"""
Quick verification script - checks if all dependencies are installed correctly
Run this: python test_setup.py
"""

import sys
from pathlib import Path

print("\n" + "="*80)
print("NEWS AGENT - SETUP VERIFICATION")
print("="*80 + "\n")

# Test 1: Python version
print("[1] Python version:")
print(f"    ✓ {sys.version}\n")

if sys.version_info < (3, 10):
    print("    ⚠️  WARNING: Requires Python 3.10+")

# Test 2: Check required modules
print("[2] Checking required modules...")
modules_to_check = {
    'pandas': 'Data loading',
    'openpyxl': 'Excel reading',
    'aiohttp': 'Async HTTP',
    'beautifulsoup4': 'HTML parsing',
    'feedparser': 'RSS parsing',
    'requests': 'HTTP requests',
    'dateutil': 'Date parsing',
}

failed = []
for module, description in modules_to_check.items():
    try:
        __import__(module)
        print(f"    ✓ {module:<20} - {description}")
    except ImportError:
        print(f"    ✗ {module:<20} - {description} (NOT INSTALLED)")
        failed.append(module)

print()

# Test 3: Project structure
print("[3] Project structure:")
required_files = [
    'config.py',
    'logger_config.py',
    'excel_loader.py',
    'url_utils.py',
    'crawler.py',
    'news_parser.py',
    'classifier.py',
    'file_exporter.py',
    'main.py',
    'requirements.txt',
]

for file in required_files:
    path = Path(file)
    if path.exists():
        print(f"    ✓ {file}")
    else:
        print(f"    ✗ {file} (MISSING)")

print()

# Test 4: Project directories
print("[4] Project directories:")
required_dirs = ['data', 'logs', 'news_output']

for dir_name in required_dirs:
    path = Path(dir_name)
    if path.exists():
        print(f"    ✓ {dir_name}/")
    else:
        print(f"    ℹ {dir_name}/ (will be created)")
        path.mkdir(exist_ok=True)

print()

# Test 5: Data file
print("[5] Data file (organizations.xlsx):")
data_file = Path('data') / 'organizations.xlsx'
if data_file.exists():
    print(f"    ✓ Found: {data_file}")
    try:
        import pandas as pd
        df = pd.read_excel(data_file)
        print(f"    ✓ Rows: {len(df)}")
        print(f"    ✓ Columns: {list(df.columns)}")
    except Exception as e:
        print(f"    ✗ Error reading file: {e}")
else:
    print(f"    ℹ {data_file} not found")
    print(f"    → Please create this file with organizations data")

print()

# Test 6: Import project modules
print("[6] Testing project module imports...")
try:
    import config
    print("    ✓ config imported")
except Exception as e:
    print(f"    ✗ config import failed: {e}")

try:
    import logger_config
    print("    ✓ logger_config imported")
except Exception as e:
    print(f"    ✗ logger_config import failed: {e}")

try:
    import excel_loader
    print("    ✓ excel_loader imported")
except Exception as e:
    print(f"    ✗ excel_loader import failed: {e}")

try:
    import classifier
    print("    ✓ classifier imported")
except Exception as e:
    print(f"    ✗ classifier import failed: {e}")

print()

# Final summary
print("="*80)
if failed:
    print(f"⚠️  INSTALLATION INCOMPLETE: {len(failed)} module(s) missing\n")
    print("Install missing modules:")
    print(f"pip install {' '.join(failed)}\n")
else:
    print("✅ ALL SYSTEMS READY!\n")
    print("Next steps:")
    print("1. Place organizations.xlsx in the 'data' folder")
    print("2. Run: python main.py\n")

print("="*80 + "\n")
