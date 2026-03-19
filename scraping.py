import requests
from bs4 import BeautifulSoup
import sqlite3

response = requests.get("https://www.scrapethissite.com/pages/forms/")
soup = BeautifulSoup(response.content, "html.parser")

conn = sqlite3.connect("hockey.db")
cursor = conn.cursor()

create_sql = """
CREATE TABLE hockey_teams (
    id INTEGER PRIMARY KEY,
    team_name VARCHAR(50),
    year INTEGER,
    wins INTEGER,
    losses INTEGER,
    ot_losses INTEGER,
    win DECIMAL(5,2),
    goals_for INTEGER,
    goals_against INTEGER,
    plus_minus INTEGER
);
"""

sql_text = """
INSERT INTO hockey_teams 
(team_name, year, wins, losses, ot_losses, win, goals_for, goals_against, plus_minus) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

rows = soup.find_all("tr")

cursor.execute(create_sql)
def to_int(x):
    return int(x) if x else None

def to_float(x):
    return float(x) if x else None

for row in rows:
    cols = row.find_all("td")

    if cols:
        data = (
            cols[0].text.strip(),
            to_int(cols[1].text.strip()),
            to_int(cols[2].text.strip()),
            to_int(cols[3].text.strip()),
            to_int(cols[4].text.strip()),
            to_float(cols[5].text.strip()),
            to_int(cols[6].text.strip()),
            to_int(cols[7].text.strip()),
            to_int(cols[8].text.strip()),
        )

        cursor.execute(sql_text, data)

cursor.execute("SELECT * FROM hockey_teams;")
data = cursor.fetchall()
print(data)
conn.commit()
conn.close()