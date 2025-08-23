from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# URLs to capture
urls = [
    "http://127.0.0.1:5000/",      # home page
    "http://127.0.0.1:5000/add"   # add transaction page
]

# Folder to save screenshots
screenshot_folder = "screenshots"
os.makedirs(screenshot_folder, exist_ok=True)

# Chrome options
options = Options()
options.add_argument("--headless")   # run without opening a browser window
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Automatically install and use correct ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for url in urls:
    try:
        driver.get(url)
        time.sleep(2)  # wait for page to load
        filename = url.split("/")[-1] or "home"
        screenshot_path = os.path.join(screenshot_folder, f"{filename}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        print(f"Error capturing {url}: {e}")

driver.quit()
