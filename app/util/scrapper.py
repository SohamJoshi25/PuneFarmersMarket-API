import requests
from bs4 import BeautifulSoup

from app.util.translation import unit_marathi_to_english,item_marathi_to_english

def scrapeData(link,cursor,date):
    r = requests.get(link, timeout=10)
    soup = BeautifulSoup(r.content, 'html.parser')
    tables = soup.find_all("table")

    if len(tables) == 0:
        return "Database Not Updated"

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
                    if date == None :
                        cursor.execute("INSERT INTO rates (code, item_name, unit, quantity, minimum, maximum) VALUES (%s,%s, %s, %s, %s, %s)",(row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5]))
                    else:
                        cursor.execute("INSERT INTO rates (date,code, item_name, unit, quantity, minimum, maximum) VALUES (%s,%s, %s, %s, %s, %s, %s)",(date,row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5]))
    

