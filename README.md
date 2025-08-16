# **Swecha Web Scraper**

This project extracts <p> (paragraph) text from any given website URL and saves the results into:

Individual .txt files inside the scraped_data/ folder

A SQLite database (scraped_data.db) for centralized storage

It also includes error handling and automatic file naming based on the website domain.

# **Setup**
1. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate   # On Windows
# source venv/bin/activate   # On Mac/Linux

# **Install dependencies**
pip install -r requirements.txt

# **Usage**

Run the scraper with a website URL:

python scraper_swaraj.py <website_url>

# **Example**
python scraper_swaraj.py https://www.python.org/


✅ Extracted 12 paragraph(s)
✅ Saved to scraped_data/www-python-org.txt
✅ Inserted into scraped_data.db

# **Output Details**

Text Files → Saved in scraped_data/ folder. Each run creates a new file with the website’s domain name.

Database → All extracted text is inserted into scraped_data.db for easy querying.

# **Example Run**
python scraper_swaraj.py https://www.india.gov.in/


# **Output:**

Extracted 7 paragraphs.
Saved to: scraped_data/www-india-gov-in.txt
Inserted into database: scraped_data.db

# **License**

This project is created for Swecha tasks and educational purposes.