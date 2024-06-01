from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to your ChromeDriver
chromedriver_path = 'C:/Users/mrp97/Desktop/Google_Scholar_PDF_Images_Scraper-main/driver/chromedriver.exe'

# Create a Service object
service = Service(executable_path=chromedriver_path)

# Initialize the WebDriver with the service object
driver = webdriver.Chrome(service=service)

try:
    # Open the target URL
    driver.get('https://scholar.google.com/scholar?q=Mobile+Edge+Computing&hl=ar&start=10&as_sdt=0,5')  # Replace with your target URL

    # Your scraping logic here...

    # Check for CAPTCHA presence (simplified check)
    if "captcha" in driver.page_source.lower():
        print("CAPTCHA detected. Please solve it manually.")
        input("Press Enter after solving the CAPTCHA...")

    # Continue scraping after CAPTCHA is solved
    # Your continued scraping logic here...

finally:
    # Ensure the WebDriver is closed properly
    driver.quit()
