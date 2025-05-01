# FarmersMarket-WebScraper

A simple, daily-updated API that scrapes local farmer market product prices and quantities from a government website and exposes the data via a REST API using FastAPI.

---

## 🌾 Project Overview

- **Automated Scraping**: Collects prices and quantities of products from local pune farmer markets every day.
- **Live Data Exposure**: Makes fresh data available through a RESTful FastAPI backend.
- **Open API**: Easily integrate real-time market data into your own applications or dashboards.
- **Product Translation**: Translated Product Names from local language marathi to english.
- **Hosted Demo**: [Live API on Render](https://localfarmermarket.onrender.com/)

---

## 🚀 How to Use the API

### Base URL
https://localfarmermarket.onrender.com/

### Example Endpoints

| Endpoint              | Description                                                      |
|-----------------------|------------------------------------------------------------------|
| `/docs`               | Interactive API docs (FasiAPI selfmade)                          |
| `/rates   `           | Get all market products with price & quantity                    |
| `/refresh`            | Manually trigger a data refresh (Used for Cron Job)              |

### Sample Usage

**GET https://localfarmermarket.onrender.com/rates/?order_by=code&order=ASC&limit=10&offset=10**

[
  {
    "code": 1001,
    "quantity": 11970,
    "unit": "Quintal",
    "date": "2025-04-27",
    "minimum": 500,
    "maximum": 1500,
    "item_name": "Onion"
  },
  {
    "code": 1001,
    "quantity": 9607,
    "unit": "Quintal",
    "date": "2025-04-29",
    "minimum": 500,
    "maximum": 1500,
    "item_name": "Onion"
  },
  {
    "code": 1001,
    "quantity": 6368,
    "unit": "Quintal",
    "date": "2025-04-23",
    "minimum": 700,
    "maximum": 1500,
    "item_name": "Onion"
  },
  {
    "code": 1001,
    "quantity": 7969,
    "unit": "Quintal",
    "date": "2025-04-28",
    "minimum": 400,
    "maximum": 1400,
    "item_name": "Onion"
  },
  {
    "code": 1001,
    "quantity": 10534,
    "unit": "Quintal",
    "date": "2025-04-18",
    "minimum": 700,
    "maximum": 1500,
    "item_name": "Onion"
  }
]

<br>
<br>
<img src="https://raw.githubusercontent.com/SohamJoshi25/FarmersMarket-WebScraper/refs/heads/main/public/image.png" alt="Farmer market Portal" width="500">
<br>
<br>
<img src="https://raw.githubusercontent.com/SohamJoshi25/FarmersMarket-WebScraper/refs/heads/main/public/market1.png" alt="Farmer Market Prices" width="500">
<br>
<br>
<img src="https://raw.githubusercontent.com/SohamJoshi25/FarmersMarket-WebScraper/refs/heads/main/public/market2.png" alt="Postman" width="500">
<br>
<br>
