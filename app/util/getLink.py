import datetime

async def getLink(cursor, connection):
    cursor.execute("SELECT date, rate FROM rateMaster ORDER BY date DESC LIMIT 1;")
    date, rate = cursor.fetchone()
    print(date)
    print(rate)
    print(datetime.date.today())

    if date != datetime.date.today():
        rate += 1
        date = datetime.date.today()
        # Insert both rate and date
        cursor.execute(
            "INSERT INTO rateMaster (rate, date) VALUES (%s, %s);",
            (rate, date)
        )

        return f"http://www.puneapmc.org/history.aspx?id=Rates{rate}", date, True
    
    return f"http://www.puneapmc.org/history.aspx?id=Rates{rate}", date, False
