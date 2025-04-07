import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time
import os

from marathi_to_english import unit_marathi_to_english,item_marathi_to_english

BASE_URL = "http://www.puneapmc.org/"
LOOKUP_COUNT = 100
FILE_NAME = "output.csv"


def get_links(BASE_URL):

    driver = webdriver.Chrome()

    # Open the website
    driver.get(BASE_URL + "rates.aspx")
    time.sleep(3)  # Give JS time to load data

    # Get page source after JS execution
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Now extract the dynamically loaded content
    anchors = soup.find_all('a')  # Example ID for rate table

    links = []

    for idx,anchor in enumerate(anchors):
        if(anchor.get_text() == "View Rates"):
            links.append(BASE_URL + anchor["href"])

    driver.quit()
    return links

def generateData(link):
    print(f"🔗 Fetching: {link}")
    r = requests.get(link, timeout=10)  # timeout added
    soup = BeautifulSoup(r.content, 'html.parser')
    tables = soup.find_all("table")
    print(f"Found {len(tables)} tables")

    file_exists = os.path.isfile(FILE_NAME)
    is_empty = not file_exists or os.path.getsize(FILE_NAME) == 0

    row_count = 0

    with open(FILE_NAME, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)

        if is_empty:
            writer.writerow(["Code No", "Item", "Unit", "Quantity", "Min", "Max"])

        for table in tables:
            rows = table.find_all("tr")
            for idx,row in enumerate(rows):
                tds = row.find_all("td")
                if len(tds) != 6:
                    continue

                row_data = []
                isvalid = True

                for idx,td in enumerate(tds):
                    strong_tag = td.find("strong")
                    text = strong_tag.get_text(strip=True) if strong_tag else td.get_text(strip=True)


                    if not text:
                        isvalid = False
                        break

                    if(idx == 1):
                        if item_marathi_to_english.get(text):
                            row_data.append(item_marathi_to_english[text])
                        else:
                            row_data.append(text)
                    elif(idx == 2):

                        if unit_marathi_to_english.get(text):
                            row_data.append(unit_marathi_to_english[text])
                        else:
                            row_data.append(text)

                    elif (idx >= 4):
                        row_data.append(text.split(" ")[1].split("/")[0])
                    else:
                        row_data.append(text)

                    if len(row_data) == 6 and isvalid:
                        writer.writerow(row_data)
                        row_count += 1

    print(f"Appended {row_count} rows.\n")

def deleteFile():
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)



deleteFile()

links = get_links(BASE_URL)

for idx, link in enumerate(links):
    if(idx==LOOKUP_COUNT):
        break
    print(idx + 1)
    generateData(links[idx])
    
