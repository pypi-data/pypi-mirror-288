from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from typing import List, Optional
from pydantic import BaseModel

class TorrentGalaxyContext(BaseModel):
    cookies: Optional[List[dict]]
    screenshot_bytes: Optional[bytes]
    url: str
    headless: bool = True
    domain: str
    torrent_id: str
    wait_seconds: int
    

def get_request_context(headless: bool = True, 
                        domain: str = "torrentgalaxy.to", 
                        torrent_id: str = "16100045",
                        wait_seconds: int = 10) -> TorrentGalaxyContext:
    # Set up Chrome options for headless mode
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--no-sandbox")

    # Specify the path to the ChromeDriver binary
    chrome_driver_path = "/usr/local/bin/chromedriver"

    # Initialize the WebDriver with the headless option
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

    # Navigate to the URL
    url = f"https://{domain}/torrent/{torrent_id}"
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(wait_seconds)
    
    # Take a screenshot and get the image bytes
    driver.maximize_window()
    screenshot_bytes = driver.get_screenshot_as_png()

    # Retrieve cookies
    cookies = driver.get_cookies()

    # Close the WebDriver
    driver.quit()
    
    return TorrentGalaxyContext(
        cookies=cookies,
        screenshot_bytes=screenshot_bytes,
        url=url,
        headless=headless,
        domain=domain,
        torrent_id=torrent_id,
        wait_seconds=wait_seconds
    )