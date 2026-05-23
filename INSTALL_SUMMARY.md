# 📦 NEWS AGENT - ПОЛНАЯ УСТАНОВКА

## ✅ ЧТО БЫЛО СОЗДАНО (14 файлов)

```bash
c:\моя\ИИ-агент маринет\
│
├── 🔧 ЯДРО ПРИЛОЖЕНИЯ
│   ├── main.py                 - Главная оркестрация всех этапов
│   ├── config.py               - Конфигурация (темы, паттерны)
│   └── logger_config.py        - Система логирования
│
├── 📚 МОДУЛИ ОБРАБОТКИ
│   ├── excel_loader.py         - Загрузка организаций из Excel
│   ├── url_utils.py            - Нормализация и валидация URL
│   ├── crawler.py              - Поиск новостных источников (RSS, /news)
│   ├── news_parser.py          - Парсинг новостей из HTML и RSS
│   ├── classifier.py           - Классификация по темам
│   └── file_exporter.py        - Сохранение организованных по темам
│
├── 🚀 УСТАНОВКА И ЗАПУСК
│   ├── requirements.txt        - Все зависимости (pip install)
│   ├── setup.bat               - Автоматическая установка (Windows)
│   ├── setup.sh                - Установка для Linux/macOS
│   ├── test_setup.py           - Проверка корректности установки
│   └── SETUP_GUIDE.md          - Пошаговая инструкция
│
├── 📖 ДОКУМЕНТАЦИЯ
│   ├── README.md               - Полная документация проекта
│   └── INSTALL_SUMMARY.md      - Этот файл
│
└── 📂 ПАПКИ (будут созданы автоматически)
    ├── data/                   - Исходные данные (Excel)
    ├── news_output/            - Результаты парсинга
    └── logs/                   - Логи выполнения
```

---

## 🎯 БЫСТРЫЙ СТАРТ (3 ШАГА)

### Шаг 1️⃣: Установка (выполнить один раз)

**Windows (рекомендуется):**

```python
cd "c:\моя\ИИ-агент маринет"
setup.bat
```

**Linux/macOS:**

```bash
cd "/your/path/news_agent"
bash setup.sh
```

**Вручную:**

```bash
pip install -r requirements.txt
```

### Шаг 2️⃣: Добавить данные

Создать файл `data/organizations.xlsx` с организациями (колонки: Название, Сайт, Категории)

### Шаг 3️⃣: Запустить

```bash
python main.py
```

## Шаг 1: Установка зависимостей

---

## 📋 ПОЛНАЯ ИНСТРУКЦИЯ

### 1️⃣ Установка Python

**Если Python НЕ установлен:**

- Скачать с <https://www.python.org/downloads/> (версия 3.10+)
- **ВАЖНО**: отметить "Add Python to PATH"
- Перезагрузить компьютер

**Проверка:**

```bash
python --version
pip --version
```

---

### 2️⃣ Установка зависимостей

Откройте **Command Prompt (cmd.exe)**:

```bash
cd "c:\моя\ИИ-агент маринет"
```

**Вариант A (автоматический):**

```bash
setup.bat
```

**Вариант B (вручную):**

```bash
pip install -r requirements.txt
```

**Проверка установки:**

```bash
python test_setup.py
```

Должно вывести: `✅ ALL SYSTEMS READY!`

---

### 3️⃣ Подготовка данных

1. Откройте Excel (или LibreOffice Calc)
2. Создайте файл с таблицей организаций:
   - Колонка 1: **Название** (текст)
   - Колонка 2: **Сайт** (URL, начиная с https://)
   - Колонка 3: **Категории** (текст, через запятую)

Пример:

```bash
Название                  | Сайт                    | Категории
3Д-Технологии             | https://3d-tech.ru      | Мониторинг инфраструктуры
АКВАИР                    | https://aquairy.ru      | Мониторинг, Чрезвычайные
Газпром добыча            | https://gazprom.ru      | Энергетический сектор
```

1. Сохраните как **`data/organizations.xlsx`**

---

### 4️⃣ Запуск агента

```bash
python main.py
```

**Ожидаемый вывод:**

```bash
================================================================================
NEWS AGENT STARTED
================================================================================
Step 1: Loading organizations...
✓ Loaded 3 organizations
Step 2: Crawling and parsing news...
  Processing: 3Д-Технологии
    Scanning https://3d-tech.ru...
    Found RSS feed: https://3d-tech.ru/feed
  Processing: АКВАИР
    ...
Step 3: Exporting news by topics...
  Мониторинг инфраструктуры: 12 items
  Энергетический сектор: 5 items
  Наука и образование: 3 items

================================================================================
REPORT
================================================================================
Organizations processed: 3
News sources found: 8
News items parsed: 20
Topics found: 5
Output directory: c:\...\news_output
Duration: 45.23 seconds
================================================================================
NEWS AGENT COMPLETED
================================================================================
```

---

### 5️⃣ Результаты

Результаты сохранены в `news_output/`:

```bash
news_output/
├── Мониторинг инфраструктуры/
│   ├── 2026-05-21_3D-Технологии_Успешный_тест.md
│   ├── 2026-05-21_АКВАИР_Новые_системы.md
│   └── 2026-05-21_Газпром_Инспекция.md
├── Энергетический сектор/
│   ├── 2026-05-21_Газпром_Добыча_начата.md
│   └── 2026-05-21_Новатэк_Проект.md
├── Наука и образование/
│   └── 2026-05-21_МГТУ_Лекция.md
└── index.json (полный индекс всех новостей)
```

**Каждый файл содержит:**

```markdown
# Заголовок новости

**Дата:** 2026-05-21
**Организация:** 3Д-Технологии.РУ
**Источник:** https://3d-tech.ru/news/page1
**Ссылка на новость:** https://3d-tech.ru/news/123

---

## Содержание

Полный текст новости...
```

---

## 🔍 ПРОВЕРКА УСТАНОВКИ

Запустите тест:

```bash
python test_setup.py
```

**Должно показать:**

```bash
[1] Python version:
    ✓ Python 3.10.x (version)

[2] Checking required modules...
    ✓ pandas               - Data loading
    ✓ openpyxl            - Excel reading
    ✓ aiohttp             - Async HTTP
    ✓ beautifulsoup4      - HTML parsing
    ... (все ✓)

[3] Project structure:
    ✓ config.py
    ✓ main.py
    ... (все файлы)

✅ ALL SYSTEMS READY!
```

---

## 📊 ИСПОЛЬЗУЕМЫЕ БИБЛИОТЕКИ

| Библиотека | Версия | Назначение |

|-----------|--------|-----------|
| pandas | 2.0.3 | Чтение Excel |
| openpyxl | 3.1.2 | Работа с XLSX |
| aiohttp | 3.8.5 | Асинхронные HTTP-запросы |
| beautifulsoup4 | 4.12.2 | Парсинг HTML |
| feedparser | 6.0.10 | Парсинг RSS |
| requests | 2.31.0 | HTTP-запросы |
| python-dateutil | 2.8.2 | Парсинг дат |
| ... и другие | ... | ... |

Всего: ~30 библиотек

---

## ⚠️ ТИПИЧНЫЕ ОШИБКИ

### ❌ "python: command not found"

**Решение:**

- Установить Python с <https://www.python.org/downloads/>
- При установке отметить ✅ "Add Python to PATH"
- Перезагрузить компьютер

### ❌ "ModuleNotFoundError: No module named 'pandas'"

**Решение:**

```bash
pip install pandas openpyxl aiohttp beautifulsoup4 feedparser
```

### ❌ "File not found: organizations.xlsx"

**Решение:**

- Создать файл `data/organizations.xlsx`
- Убедиться, что папка `data/` существует
- Проверить путь в `config.py`

### ❌ Агент работает слишком медленно

**Это нормально!** Для 100+ организаций может работать 5-10 минут:

- Делает HTTP-запросы к каждому сайту
- Парсит HTML
- Классифицирует новости
- Сохраняет файлы

---

## 🚀 ДАЛЬНЕЙШИЕ УЛУЧШЕНИЯ

После базовой установки можно добавить:

1. **Веб-интерфейс** (FastAPI)

   ```bash
   pip install fastapi uvicorn
   # Затем создать web_app.py
   ```

2. **Автоматические запуски** (APScheduler)

   ```bash
   pip install APScheduler
   # Добавить scheduler.py
   ```

3. **ML-классификация** (Transformers)

   ```bash
   pip install transformers torch
   # Более точная классификация новостей
   ```

4. **База данных** (SQLite)
   - Хранить историю новостей
   - Отслеживать дубликаты

---

## 📞 ПОМОЩЬ

- Смотрите **README.md** для полной документации
- Смотрите **logs/news_agent.log** для деталей ошибок
- Отредактируйте **config.py** для настроек

---

## ✨ ВСЁ ГОТОВО

Теперь можно:

1. ✅ Добавить `organizations.xlsx` в папку `data/`
2. ✅ Запустить `python main.py`
3. ✅ Получить новости в `news_output/`
