# Social Media Comment Scraper

This project is a Python-based automation tool that extracts post and comment data from **Facebook** and **Instagram** posts and compiles them into a standardized Excel file.

## 📁 Project Structure

```
project-folder/
│
├── date_formatter.py      # Formats various date formats into a standard one
├── excel_merger.py        # Merges new Excel data into a main file
├── facebook.py            # Scrapes Facebook post and comment data
├── instagram.py           # Scrapes Instagram post and comment data (reads post links from Excel)
└── README.md              # Project description and usage instructions
```

## 🚀 Features

- Scrapes posts and comments from **Facebook** and **Instagram**
- Supports **multi-language date formats** (English & Turkish)
- Merges multiple data sources into a **single Excel file**
- Designed for **automated large-scale data collection**

## 🛠️ Dependencies

Install the required Python libraries using pip:

```bash
pip install selenium pandas openpyxl
```

Also, make sure:
- [Google Chrome](https://www.google.com/chrome/) is installed.
- [ChromeDriver](https://chromedriver.chromium.org/downloads) is downloaded and matches your Chrome version, and its path is set correctly.

## ⚙️ Usage

### 1. Facebook Scraping

Edit and run `facebook.py`:

```python
login_to_facebook(driver, "your_username", "your_password")
post_links = ["https://www.facebook.com/post1", "https://www.facebook.com/post2"]
```

Outputs:
- `facebook_comments.xlsx` (raw output)
- Merged into `standart.xlsx`

### 2. Instagram Scraping

Prepare an Excel file (e.g., `posts_data.xlsx`) with a column named **Link** containing post URLs.

Edit and run `instagram.py`:

```python
login_to_instagram(driver, "your_username", "your_password")
excel_file = "posts_data.xlsx"
```

Outputs:
- `posts_data_instagram_comments.xlsx` (raw output)
- Merged into `standart.xlsx`

## 📌 Notes

- Avoid making too many requests in a short period — Facebook/Instagram might block the bot.
- For best results, use a clean Chrome profile and a strong internet connection.

## 📃 License

This project is for educational and personal data analysis purposes only.
