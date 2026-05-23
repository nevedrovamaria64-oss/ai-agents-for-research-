#!/usr/bin/env python3
"""
Quick checklist - verify your system is ready to go!
Run: python checklist.py
"""

import sys
from pathlib import Path

def check_item(condition, success_msg, fail_msg):
    if condition:
        print(f"  ✅ {success_msg}")
        return True
    else:
        print(f"  ❌ {fail_msg}")
        return False

print("\n" + "="*70)
print("  🎯 NEWS AGENT - READINESS CHECKLIST")
print("="*70 + "\n")

all_good = True

# Check 1: Files
print("📋 Project Files:")
required_files = [
    'main.py', 'config.py', 'excel_loader.py', 'crawler.py',
    'news_parser.py', 'classifier.py', 'file_exporter.py',
    'requirements.txt', 'START_HERE.md'
]

file_count = 0
for f in required_files:
    if Path(f).exists():
        file_count += 1

all_good &= check_item(
    file_count >= 8,
    f"All core files present ({file_count}/9)",
    f"Missing files ({file_count}/9)"
)

# Check 2: Python
print("\n🐍 Python Installation:")
all_good &= check_item(
    sys.version_info >= (3, 10),
    f"Python {sys.version_info.major}.{sys.version_info.minor}+ installed",
    f"Python 3.10+ required (found {sys.version_info.major}.{sys.version_info.minor})"
)

# Check 3: Key Packages
print("\n📦 Required Packages:")
packages = {
    'pandas': 'Data loading',
    'openpyxl': 'Excel reading',
    'aiohttp': 'Async HTTP',
    'bs4': 'HTML parsing',
}

packages_ok = True
for pkg, desc in packages.items():
    try:
        __import__(pkg)
        print(f"  ✅ {pkg:<15} - {desc}")
    except ImportError:
        print(f"  ❌ {pkg:<15} - {desc} (NOT INSTALLED)")
        packages_ok = False

all_good &= packages_ok

# Check 4: Directories
print("\n📁 Project Directories:")
dirs = ['data', 'logs', 'news_output']
for d in dirs:
    p = Path(d)
    if not p.exists():
        p.mkdir(exist_ok=True)
    status = "exists" if p.is_dir() else "missing"
    print(f"  ✅ {d}/ ({status})")

# Check 5: Data
print("\n📊 Sample Data:")
data_file = Path('data/organizations.xlsx')
if data_file.exists():
    all_good &= check_item(
        True,
        f"organizations.xlsx exists ({data_file.stat().st_size} bytes)",
        "organizations.xlsx missing"
    )
else:
    all_good &= check_item(
        False,
        "organizations.xlsx exists",
        "organizations.xlsx not yet created (run: python create_sample_data.py)"
    )

# Summary
print("\n" + "="*70)
if all_good and packages_ok:
    print("✅ SYSTEM READY TO GO!")
    print("\nNext steps:")
    print("  1. python create_sample_data.py")
    print("  2. python main.py")
elif not packages_ok:
    print("⚠️  PACKAGES MISSING")
    print("\nFix with:")
    print("  pip install -r requirements.txt")
else:
    print("⚠️  SOME ITEMS INCOMPLETE")
    print("\nCheck documentation:")
    print("  - START_HERE.md")
    print("  - README.md")

print("="*70 + "\n")
