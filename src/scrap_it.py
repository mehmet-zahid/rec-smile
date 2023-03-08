import os
import requests
from dotenv import load_dotenv
import webbrowser
import time

load_dotenv()

SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")

SERVICE_SCRAPER_ASYNC = "http://async.scraperapi.com/jobs"
ENDPOINT_SCRAPER = "http://api.scraperapi.com?"
PROXY_SCRAPER = "http://scraperapi:APIKEY@proxy-server.scraperapi.com:8001"
SERVICE_SCRAPER_STRUCTERED_DATA = "https://api.scraperapi.com/structured/"

PRODUCTS = ["https://www.trendyol.com/alfais/4939-usb-3-0-to-ethernet-cevirici-donusturucu-adaptor-gigabit-destekli-p-133387267?boutiqueId=61&merchantId=327407",
            "https://www.trendyol.com/alfais/4939-usb-3-0-to-ethernet-cevirici-donusturucu-adaptor-gigabit-destekli-p-133387267/yorumlar?boutiqueId=61&merchantId=327407"]

req_data = {'apiKey': SCRAPER_API_KEY, 'url': PRODUCTS[1]}

r = requests.post(url = 'https://async.scraperapi.com/jobs', json=req_data).json()
status_url = r["statusUrl"]
print(status_url)

r1 = requests.get(url = status_url).json()
status = r1["status"]

while True:
    if status == "finished":
        webbrowser.open_new_tab(status_url)
        break
    time.sleep(5)

        


