# 🚀 START HERE - Complete Setup Guide

## Your News Agent is Ready

You have a complete, production-ready news monitoring system. Follow these steps:

---

## ⚡ QUICKSTART (5 minutes)

### Step 1: Open Command Prompt

- Press `Win + R`
- Type: `cmd`
- Press Enter

### Step 2: Navigate to project

```bash
cd "c:\моя\ИИ-агент маринет"
```

### Step 3: Run automatic installer

```bash
install.bat
```

This will:

- ✅ Check Python installation
- ✅ Install all 30+ dependencies
- ✅ Create necessary folders
- ✅ Verify everything works

**Wait 2-5 minutes for installation to complete...**

### Step 4: Create sample data

After installation completes, run:

```bash
python create_sample_data.py
```

This creates `data/organizations.xlsx` with 10 test organizations ready to crawl.

### Step 5: Start the agent

```bash
python main.py
```

**That's it! The agent will:**

1. Load 10 test organizations
2. Crawl their websites for news
3. Parse RSS feeds and HTML pages
4. Classify news by topic
5. Save results to `news_output/`

---

## 📊 Expected Output

```bash
================================================================================
NEWS AGENT STARTED
================================================================================
Step 1: Loading organizations...
✓ Loaded 10 organizations

Step 2: Crawling and parsing news...
  Processing: 3Д-Технологии.РУ
  Processing: АКВАИР ИНЖИНИРИНГ
  ...

Step 3: Exporting news by topics...
  Мониторинг инфраструктуры: 15 items
  Энергетический сектор: 8 items
  Наука и образование: 12 items
  ...

================================================================================
REPORT
================================================================================
Organizations processed: 10
News sources found: 24
News items parsed: 45
Topics found: 7
Duration: 2 minutes, 30 seconds
================================================================================
NEWS AGENT COMPLETED
================================================================================
```

---

## 📁 Results Location

After completion, open this folder:

```bash
c:\моя\ИИ-агент маринет\news_output\
```

You'll see:

```bash
news_output/
├── Мониторинг инфраструктуры/
│   ├── 2026-05-21_3D-Технологии_Новая_система.md
│   ├── 2026-05-21_АКВАИР_Тестирование.md
│   └── ... (more files)
├── Энергетический сектор/
│   ├── 2026-05-21_Газпром_Проект.md
│   └── ...
├── Наука и образование/
│   ├── 2026-05-21_МГТУ_Исследования.md
│   └── ...
└── index.json (full index of all news)
```

Each file contains formatted news with metadata.

---

## 🔧 Troubleshooting

### ❌ "python: command not found"

**Solution:**

1. Download Python 3.10+ from <https://www.python.org/downloads/>
2. Run installer
3. ⭐ **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install"
5. Restart computer
6. Try again

### ❌ "install.bat doesn't work"

**Solution:** Run manually:

```bash
pip install -r requirements.txt
python create_sample_data.py
python main.py
```

### ❌ Installation is slow

This is normal! First-time installation downloads ~100MB of packages.

### ❌ No news found on websites

Some websites use JavaScript. Currently, the agent supports:

- ✅ Static HTML pages
- ✅ RSS feeds
- ❌ JavaScript-heavy sites (need Selenium)

---

## 📚 Documentation Files

Read these for more info:

| File | Purpose |

|------|---------|
| `README.md` | Full documentation |
| `SETUP_GUIDE.md` | Detailed setup guide |
| `config.py` | All settings (can be customized) |
| `logs/news_agent.log` | Execution logs |

---

## 🎯 Next Steps

### Want to add your own organizations?

1. Edit `data/organizations.xlsx`:
   - Add rows with: Название | Сайт | Категории
   - Example: `MyCompany | https://mycompany.ru | Мониторинг инфраструктуры, Энергетика`

2. Run again: `python main.py`

### Want to customize topics?

Edit `config.py`:

```python
GLOBAL_TOPICS = {
    "My Topic": ["keyword1", "keyword2"],
    # ... add your own
}
```

### Want to schedule daily runs?

Edit `config.py`:

```python
SCHEDULE_INTERVAL = "daily"  # or "weekly"
SCHEDULE_TIME = "09:00"      # Run at 9 AM
```

---

## 💡 Pro Tips

1. **Test with 5 organizations first** - makes debugging easier
2. **Check logs** - `logs/news_agent.log` has all details
3. **Monitor output** - `news_output/` folder grows as news is found
4. **Use test_setup.py** - verify installation anytime: `python test_setup.py`

---

## 🎁 What You Have

✅ **Fully functional news crawler**
✅ **Automatic HTML + RSS parsing**
✅ **Smart topic classification**
✅ **Organized file output**
✅ **Complete logging system**
✅ **Production-ready code**
✅ **Full documentation**
✅ **Sample data included**

---

## ✨ You're All Set

**Time to run:**

```bash
install.bat
python create_sample_data.py
python main.py
```

**Questions?** Check the documentation or logs.

**Ready to start?** 🚀

---

**Next command to run:**

```bash
install.bat
```
