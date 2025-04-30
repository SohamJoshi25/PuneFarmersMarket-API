import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

from util.translation import unit_marathi_to_english,item_marathi_to_english

load_dotenv()

def get_links(BASE_URL,start,LOOKUP_COUNT):

    driver = webdriver.Chrome()

    driver.get(BASE_URL + "rates.aspx")
    time.sleep(3) 

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.quit()

    lis = soup.find_all('li')

    links = []

    for idx,li in enumerate(lis):

        if idx < start :
            continue

        if len(links) == LOOKUP_COUNT:
            break

        anchor = li.find('a', string="View Rates")
        if anchor:
            text = li.get_text(separator=' ', strip=True)
            date_part = text.split('-')[0].strip()
            if ',' in date_part:
                date_str = date_part.split(',', 1)[1].strip()
            else:
                date_str = date_part.strip()
            try:
                date_obj = datetime.strptime(date_str, "%d %b, %Y")
                pg_date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                pg_date = None  # or handle error as needed

            links.append({
                "link": BASE_URL + anchor["href"],
                "date": pg_date
            })

    
    return links

def generateData(link,cur,date):
    r = requests.get(link, timeout=10)  # timeout added
    soup = BeautifulSoup(r.content, 'html.parser')
    tables = soup.find_all("table")

    for table in tables:

        rows = table.find_all("tr")

        for idx,row in enumerate(rows):
            tds = row.find_all("td")

            if len(tds) != 6:
                continue

            row_data = []

            for idx,td in enumerate(tds):
                strong_tag = td.find("strong")
                text = strong_tag.get_text(strip=True) if strong_tag else td.get_text(strip=True)

                if not text:
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

                elif (idx == 4 or idx == 5):
                    row_data.append(text.split(" ")[1].split("/")[0])
                else:
                    row_data.append(text)

                if len(row_data) == 6:
                    cur.execute("INSERT INTO rates (date,code, item_name, unit, quantity, minimum, maximum) VALUES (%s,%s, %s, %s, %s, %s, %s)",(date,row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5]))

def init():

    DATABASE_URL = os.environ.get('DATABASE_URL')
    BASE_URL = "http://www.puneapmc.org/"
    LOOKUP_COUNT = 20
    START_COUNT = 0


    if DATABASE_URL == None:
       raise RuntimeError("DATABASE_URL not set in environment")
    else:

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        link_objs = get_links(BASE_URL,START_COUNT,LOOKUP_COUNT)

        print(link_objs)

        for idx, link_obj in enumerate(link_objs):
            print(idx)
            generateData(link_obj['link'],cur,link_obj['date'])
            conn.commit()
        
        print("Ran Successfully")
        cur.close()
        conn.close()
    
    
if __name__ == "__main__" :
    init()


