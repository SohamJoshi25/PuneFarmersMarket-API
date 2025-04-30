import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

unit_marathi_to_english = {
    'क्विंटल': 'Quintal',
    'शेकडा': 'Per Hundred',
    '१० किलो': '10 Kg',
    '२५ किलो': '25 Kg',
    '२ किलो': '2 Kg',
    '५० किलो': '50 Kg',
    '१०० किलो': '100 Kg',
    '१ किलो': '1 Kg',
    'बंडल': 'Bundle',
    'गड़ी': 'Bunch',
    'नगास': 'Per Piece',
}

item_marathi_to_english  = {
    'कांदा': 'Onion',
    'बटाटा': 'Potato',
    'लसूण': 'Garlic',
    'आले': 'Ginger',
    'भेंडी': 'Ladyfinger',
    'गवार': 'Cluster Beans',
    'टोमॅटो': 'Tomato',
    'मटार': 'Peas',
    'घेवडा': 'Ridge Gourd',
    'दोडका': 'Tinda',
    'हि.मिरची': 'Green Chilli',
    'दुधीभोपळा': 'Bottle Gourd',
    'भु. शेंग': 'Roasted Peanuts',
    'काकडी': 'Cucumber',
    'कारली': 'Bitter Gourd',
    'डांगर': 'Yam',
    'गाजर': 'Carrot',
    'पापडी': 'Snake Gourd',
    'पडवळ': 'Pointed Gourd',
    'फ्लॉवर': 'Cauliflower',
    'कोबी': 'Cabbage',
    'वांगी': 'Brinjal',
    'ढोबळी': 'Pumpkin',
    'सुरण': 'Elephant Foot Yam',
    'तोंडली': 'Ivy Gourd',
    'बीट': 'Beetroot',
    'कोहळा': 'Ash Gourd',
    'पावटा': 'Parwal',
    'वाल': 'Field Beans',
    'वालवर': 'Hyacinth Beans',
    'शेवगा': 'Drumstick',
    'कैरी': 'Raw Mango',
    'ढेमसा': 'Chow Chow',
    'नवलकोल': 'Kohlrabi',
    'डबलबी': 'Double Beans',
    'चवळी': 'Amaranth Leaves',
    'रताळी': 'Taro',
    'फणस': 'Jackfruit',
    'परवल': 'Pointed Gourd',
    'घोसाळी': 'Zucchini',
    'कडीपत्ता': 'Curry Leaves',
    'केळी': 'Banana',
    'डिंग्री': 'Tindora',
    'आरवी': 'Colocasia',
    'भावनगरी': 'Bhawanagri Chilli',
    'मोगरी': 'Radish Pods',
    'लाल व पिवळी ढाेबळी': 'Red and Yellow Pumpkin',
    'बेझील': 'Basil',
    'ब्रोकाेली': 'Broccoli',
    'पाेकचाय': 'Bok Choy',
    'लोलो': 'Lollo Lettuce',
    'चायना काेबी': 'Chinese Cabbage',
    'लाल काेबी': 'Red Cabbage',
    'आवाकडु': 'Avocado',
    'बेबी काॅर्न': 'Baby Corn',
    'झुकुणी': 'Zucchini',
    'चेरी टॅामेटो': 'Cherry Tomato',
    'सॅलड': 'Lettuce',
    'सॅलरी': 'Celery',
    'मशरुम': 'Mushroom',
    'कमल काकडी': 'Lotus Root',
    'लाल मुळा': 'Radish',
    'राेमन': 'Romaine Lettuce',
    'लिफी': 'Leeks',
    'चायना काकडी': 'Chinese Cucumber',
    'चायना लसुण': 'Chinese Garlic',
    'शतावरी': 'Asparagus',
    'लेमन ग्ास': 'Lemon Grass',
    'सिमसम': 'Sesame',
    'कोथिंबीर': 'Coriander',
    'मेथी': 'Fenugreek',
    'शेपू': 'Dill',
    'कांदापात': 'Spring Onion',
    'पालक': 'Spinach',
    'मुळा': 'Radish',
    'चवळी पाला': 'Amaranth Leaves',
    'करडई': 'Mustard',
    'राजगिरा': 'Amaranth',
    'ह. गड़ी': 'Green Garlic',
    'पुदीना': 'Mint',
    'नारळ': 'Coconut',
    'मकाकणिस': 'Poppy Seeds',
    'चाकवत': 'Chia Seeds',
    'अंबाडी': 'Roselle',
    'चुका': 'Chia',
    'देठ': 'Fennel Stalks',
    'माठ': 'Sago',
    'मोहरी': 'Fenugreek Seeds',
    'चंदनबटवा': 'Sandwich Tree',
    'आईसबर्ग': 'Iceberg Lettuce',
    'लिंबू': 'Lemon',
    'पेरु': 'Guava',
    'टरबूज': 'Watermelon',
    'पीअर': 'Pear',
    'पिच': 'Peach',
    'प्लम': 'Plum',
    'रामफळ': 'Pomegranate',
    'सफरचंद - फ्युजी': 'Apple - Fuji',
    'सफरचंद-फ्युजी': 'Apple - Fuji',
    'संञा': 'Jamun',
    'अननस': 'Pineapple',
    'सिताफळ': 'Custard Apple',
    'अंजीर': 'Fig',
    'स्ट्रॉबेरी': 'Strawberry',
    'बोर': 'Jujube',
    'चेरी': 'Cherry',
    'चिक्कू': 'Sapodilla',
    'डाळींब-नं.१': 'Pomegranate - No.1',
    'सफरचंद-सिमला': 'Apple - Shimla',
    'नासपती': 'Pear',
    'जांभूऴ': 'Jamun',
    'कलिगङ': 'Karonda',
    'लीची': 'Litchi',
    'विलायची': 'Star Fruit',
    'करवंद': 'Karonda',
    'आवळा': 'Amla',
    'कवट': 'Wood Apple',
    'मोसंबी': 'Sweet Lime',
    'कोकम': 'Kokum',
    'जदाऴू': 'Cashew Apple',
    'मॉसंबी': 'Mosambi',
    'नासपाती': 'Pear',
    'पपई': 'Papaya',
    'डाळींब-गणेश': 'Pomegranate - Ganesh',
    'डाळींब-भगवा': 'Pomegranate - Bhagwa',
    'डाळींब-नं.२': 'Pomegranate - No.2',
    'आरक्ता': 'Blood Orange',
    'सफरचंद-डेलीशयस': 'Apple - Delicious',
    'सफरचंद-वॉशिंग्टन': 'Apple - Washington',
    'आंबा-हापूस': 'Mango - Alphonso',
    'आंबा-बेगलोर': 'Mango - Bangalore',
    'आंबा-तोतापूरी': 'Mango - Totapuri',
    'द्राक्ष - तासगांव': 'Grapes - Tasgaon',
    'आंबा-रायवळ': 'Mango - Rajapuri',
    'द्राक्ष -बेंगलोर': 'Grapes - Bangalore',
    'आंबा-लालबाग': 'Mango - Lalbagh',
    'द्राक्ष - शरद': 'Grapes - Sharad',
    'आंबा-बदाम': 'Mango - Badami',
    'द्राक्ष - सिडलेस': 'Grapes - Seedless',
    'आंबा - पायरी': 'Mango - Pairi',
    'आंबा - नीलम': 'Mango - Neelam',
    'आंबा - मलगॉबा': 'Mango - Malgova',
    'आंबा - केशर': 'Mango - Keshar',
    'लाल मिरची-गावरानघाटी': 'Red Chilli - Gowran',
    'लाल मिरची- गावरानशेवाळा': 'Red Chilli - Gowran Shevala',
    'तान्दुऴ-बासमति': 'Rice - Basmati',
    'तांन्दुऴ-बासमति-दुबर': 'Rice - Basmati Dubar',
    'तांन्दुऴ-मोगरा': 'Rice - Mogara',
    'तांन्दुऴकणी': 'Rice Flakes',
    'तांन्दुऴ-आंबेमोह्रर': 'Rice - Ambemohar',
    'तांन्दुऴ-कोलम': 'Rice - Kolam',
    'तांन्दुऴ-चिन्नर': 'Rice - Chinnar',
    'तांन्दुऴ - डॅश': 'Rice - Dass',
    'तांन्दुऴ - उकडा': 'Rice - Ukada',
    'तांन्दुऴ - मसूरी': 'Rice - Masuri',
    'तांन्दुऴ - इंद्रायणी': 'Rice - Indrayani',
    'गहू - २२१८९': 'Wheat - 2189',
    'गहू - लोकवन': 'Wheat - Lokwan',
    'गहू - पंजाब कल्याणसोना': 'Wheat - Punjab Kalyan Sona',
    'गहू - गुजरात विनाट': 'Wheat - Gujarat Vinat',
    'गहू - गुजरात तुकडी': 'Wheat - Gujarat Tukdi',
    'गहू -  सिंहोर': 'Wheat - Sinhor',
    'मका - पिवळा': 'Maize - Yellow',
    'ज्वारी - मालदांडी नं १': 'Sorghum - Maldandi No.1',
    'ज्वारी - मालदांडी नं २': 'Sorghum - Maldandi No.2',
    'ज्वारी - वसंत नं ५': 'Sorghum - Vasant No.5',
    'ज्वारी -  वसंत नं ९': 'Sorghum - Vasant No.9',
    'ज्वारी - दुरी': 'Sorghum - Duri',
    'बाज्ररी - गावरान': 'Pearl Millet - Gowran',
    'बाज्ररी - संकरीत': 'Pearl Millet - Hybrid',
    'बाज्ररी - महिको नं ९१०': 'Pearl Millet - Mahico No.910',
    'लालमिरची': 'Red Chilli',
    'वाटाणा-हिरवा': 'Peas - Green',
    'वाटाणा-पांढरा': 'Peas - White',
    'वाटाणा': 'Peas',
    'मसूर': 'Lentil',
    'मसूरडाळ': 'Lentil Dal',
    'धना-इंदौर': 'Coriander - Indore',
    'धना-गावरान': 'Coriander - Gowran',
    'हरभरा - चाफ़ा': 'Chickpeas - Chafa',
    'हरभरा - संकरीत': 'Chickpeas - Hybrid',
    'हरभरा - गरडा': 'Chickpeas - Garbanzo',
    'हरबरा डाळ': 'Chickpea Dal',
    'उडीद': 'Black Gram',
    'उडीद डाळ': 'Black Gram Dal',
    'मका - तांबडा': 'Maize - Red',
    'मका - पांढरा': 'Maize - White',
    'चिंच - जुनी': 'Tamarind - Old',
    'चिंच - नवी': 'Tamarind - New',
    'शेंगदाणा - घुंगरू': 'Peanut - Gunguru',
    'शेंगदाणा - जाड़ा': 'Peanut - Jara',
    'शेंगदाणा - स्पॅनिश': 'Peanut - Spanish',
    'हऴद - राजापुरी': 'Turmeric - Rajapuri',
    'हऴद - सांगली': 'Turmeric - Sangli',
    'हऴद - हरगुङ (पुरंदर)': 'Turmeric - Hargun (Purandar)',
    'हऴद - कवठा': 'Turmeric - Kavtha',
    'मूग - हिरवा': 'Green Gram',
    'मूग - पॉलिश': 'Polished Green Gram',
    'मूगदाऴ': 'Green Gram Dal',
    'हुलगा': 'Horse Gram',
    'चवऴी': 'Cowpea',
    'तूर': 'Pigeon Pea',
    'तूरदाऴ': 'Pigeon Pea Dal',
    'नाचणी': 'Finger Millet',
    'गुऴ - पिवऴा नं.१': 'Jaggery - Type 1',
    'गुऴ - पिवऴा नं.२': 'Jaggery - Type 2',
    'गुऴ - लाल': 'Red Jaggery',
    'गुऴ - लाल-काऴा': 'Red-Brown Jaggery',
    'गुऴ - बॉक्स': 'Box Jaggery',
    'लालमिरची-ब्याड्गी': 'Red Chilli - Byadgi',
    'लालमिरची-गुंटूर': 'Red Chilli - Guntur',
    'लालमिरची-नंदुरबार': 'Red Chilli - Nandurbar',
    'लालमिरची-खुडवाब्याड्गी': 'Red Chilli - Kuda Byadgi',
    'लालमिरची-खुडवागुंटूर': 'Red Chilli - Kuda Guntur',
    'लालमिरची-सीड-ईडो५': 'Red Chilli - Seed IDO5',
    'लालमिरची-अंकुर': 'Red Chilli - Sprouted',
    'काजू': 'Cashew',
    'बदाम': 'Almond',
    'खारीक': 'Dry Coconut',
    'पिस्ता': 'Pistachio',
    'आक्रोड': 'Walnut',
    'बेदाणे': 'Raisins',
    'काळे बेदाणे': 'Black Raisins',
    'अंजीररोल': 'Fig Roll',
    'खजूर': 'Dates',
    'जर्दाळू': 'Apricot',
    'खोबरा गोटा वाटी': 'Grated Coconut',
    'दालचिनी': 'Cinnamon',
    'लवंग': 'Cloves',
    'मिरी': 'Pepper',
    'खसखस': 'Poppy Seeds',
    'हळद पावडर': 'Turmeric Powder',
    'मैदा': 'Refined Flour',
    'गव्हाचे पीठ (आटा)': 'Wheat Flour',
    'साखर': 'Sugar',
    'साबुदाना': 'Tapioca Pearls',
    'मोगरा': 'Jasmine',
    'काकडा': 'Marigold',
    'जुई': 'Jasmine',
    'चमेली': 'Jasmine',
    'गुलछडी': 'Tube Rose',
    'झेंडू': 'Marigold',
    'तुळजापूरी': 'Holy Basil',
    'तेरडा': 'Crape Jasmine',
    'बिजली': 'Lightning',
    'चांदणी': 'Moonlight',
    'शेवंतीपांढरी': 'White Chrysanthemum',
    'शेवंती पिवळी': 'Yellow Chrysanthemum',
    'अस्टर': 'Aster',
    'गलांड्या': 'Galanda',
    'लिली': 'Lily',
    'गुलाब': 'Rose',
    'गुलाब गेंलीटर': 'Rose Garland',
    'गुलछडी काडी': 'Tube Rose Stick',
    'आस्टर टाकळी': 'Aster Leaves',
    'गोल्डन डी. जे.': 'Golden D.J.',
    'ग्लॅडीओ साधा': 'Gladiolus Plain',
    'ग्लॅडीओ रंगीत': 'Gladiolus Colored',
    'लास्पर': 'Larkspur',
    'ब्लु स्टार': 'Blue Star',
    'कॅन्टप': 'Cantap',
    'लेस': 'Lace',
    'टॅटस': 'Tats',
    'जिप्सी': 'Gypsy',
    'शेरनी': 'Lioness',
    'कोंबडा': 'Cock',
    'जरबेरा': 'Gerbera',
    'कर्नेशन': 'Carnation',
    'डच गुलाब': 'Dutch Rose',
    'अबोली': 'Aboli',
    'चाफा': 'Portia Tree',
    'जास्वंदी': 'Hibiscus',
    'जिना': 'Zinnia',
    'लिलीयम': 'Lilium',
    'ऑकिड': 'Orchid',
    'ऍथोरिम': 'Anthurium',
    'ग्रास': 'Grass',
    'पत्ता': 'Leaf',
    'विड्याची पाने': 'Betel Leaves'
}






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
    LOOKUP_COUNT = 1
    START_COUNT = 0


    if DATABASE_URL == None:
       raise RuntimeError("DATABASE_URL not set in environment")
    else:

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        link_objs = get_links(BASE_URL,START_COUNT,LOOKUP_COUNT)

        for idx, link_obj in enumerate(link_objs):
            print(idx)
            generateData(link_obj['link'],cur,link_obj['date'])
            conn.commit()
        
        print("Ran Successfully")
        cur.close()
        conn.close()
    
    
if __name__ == "__main__" :
    init()


