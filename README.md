# Sentiment Analysis System for Product Reviews

## Project Overview
A comprehensive system for analyzing sentiment in product reviews, featuring:
- Hotel reviews scraping from Booking.com
- General sentiment analysis for reviews
- Target-specific sentiment analysis
- User-friendly GUI interfaces

## Features
- Hotels Scraper: Automated tool for collecting hotel reviews and ratings
- Review Determiner: General sentiment analysis for any review text
- Target Review Analyzer: Analyzes sentiment towards specific aspects/targets in reviews
- Main GUI: Unified interface to access all tools

## Setup Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. Clone the repository:
```bash
git clone [repository-url]
cd fyp-1
```

2. Install required packages:
```bash
pip install nltk playwright pandas openpyxl tkinter matplotlib
```

3. Install Playwright browsers:
```bash
python -m playwright install chromium
```

4. Download required NLTK data:
```python
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### Running the Application

1. Start the main application:
```bash
python SentimentAnalysis/main.py
```

2. From the main menu, you can access:
   - Hotels Scraper: For collecting hotel reviews
   - Review Determiner: For general sentiment analysis
   - Target Review Analyzer: For analyzing specific aspects

### Troubleshooting

- If you encounter NLTK resource errors, run the NLTK downloads manually using the Python commands in step 4
- For Playwright issues, try reinstalling the browsers using `playwright install`
- Ensure all Python packages are up to date using `pip install --upgrade [package-name]`

