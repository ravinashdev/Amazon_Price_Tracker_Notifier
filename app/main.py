# ---------------------------- IMPORTS ------------------------------- #
# --------------.env file access flat string--------------#
# Allows you to read the .env file
# from dotenv import load_dotenv
# import os
# variable = os.getenv("<ENV VARIABLE>")
# load_dotenv()
# --------.env.json file access for JSON structure--------#
# .env.json file
# import json
# with open('.env.json') as f:
#     config = json.load(f)
# value = config.get('YOUR_KEY')
# --------Dynaconf--------#
# Used to return a printed report for Dynaconf for debugging
# from dynaconf import inspect_settings
# inspect_settings(settings, print_report=True)
import asyncio
import json
import datetime as dt
from core.config import settings
from core.http import HTTPClient
from clients.soup import SoupClient
from clients.notifier import NotifierClient

# ---------------------------- CONSTANTS ------------------------------- #
http = HTTPClient()
notifier = NotifierClient(settings)
soup = SoupClient()
now = dt.datetime.now()
today = f"{now:%A, %B %d, %Y}"
formatted_time = now.strftime("%I:%M %p")

# ---------------------------- GLOBAL VARIABLES ------------------------------- #

# ---------------------------- FUNCTIONS ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #

# Soup Client
#Amazon
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Host": "httpbin.org",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "'Google Chrome';v='147', 'Not.A / Brand';v='8', 'Chromium';v='147'",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "'macOS'",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-69e7cd11-269fdac761ff569e030e1551"
}
amazon_item_url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
amazon_item_page = soup.get_soup(endpoint=amazon_item_url, headers=headers)
# print(amazon_item_page.prettify())

amazon_item_title = amazon_item_page.find("span", id="productTitle").get_text(strip=True)
amazon_item_price_dollar = amazon_item_page.find("span", class_="a-price-whole").get_text(strip=True)
amazon_item_price_cents = amazon_item_page.find("span", class_="a-price-fraction").get_text(strip=True)
amazon_item_price_total = float(amazon_item_price_dollar+amazon_item_price_cents)

body = f"""
{amazon_item_title}

Only:
${amazon_item_price_total:.2f} USD

Link:
{amazon_item_url}
"""


subject=f"Price Alert! \n\tat {formatted_time} \n\ton {today}"
notifier.send_email(body=body,subject=subject)

