from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd


driver = webdriver.Chrome()
base_url = "https://www.nba.com/stats/players/"
stat_types =["traditional", "advanced"]
seasons = [
    "2024-25", "2023-24", "2022-23", "2021-22", "2020-21", "2019-20", "2018-19",
    "2017-18", "2016-17", "2015-16", "2014-15", "2013-14", "2012-13", "2011-12",
    "2010-11", "2009-10", "2008-09", "2007-08", "2006-07", "2005-06", "2004-05",
    "2003-04", "2002-03", "2001-02", "2000-01", "1999-00", "1998-99", "1997-98",
    "1996-97"
]
html = {}
extension_url = base_url + stat_types[0]

def get_seasons_html():
    driver.get(extension_url)
    #Accept page cookies 
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()
    time.sleep(1)
   
    seaons_type_select = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/section[1]/div/div/div[2]/label/div/select')))
    seaons_type_select.click()
    select = Select(seaons_type_select)
    select.select_by_visible_text("Regular Season")
    for season in seasons:
        season_select = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[1]/div/div/div[1]/label/div/select')))
        season_select.click()
        select = Select(season_select)
        select.select_by_value(season)
        time.sleep(2)
        select_element = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select')))
        select_element.click()
        select = Select(select_element)
        select.select_by_visible_text("All")
        time.sleep(2)
        html[season] = driver.page_source
    driver.quit()
    return html

def create_players_csv():
    all_players = []
    headers = []
    for season, html in html.items():
        doc = BeautifulSoup(html, "html.parser")
        table = doc.find("table", {"class": "Crom_table__p1iZz"})

        if  len(headers) == 0:
            all = [th.text.strip() for th in table.find('thead').find_all('th')]
            headers = [header for header in all if 'RANK' not in header][1:]
        
        table_body = table.find('tbody')
        for tr in table_body.find_all('tr'):
            player_item = []
            all_cols = tr.find_all('td')
            player_name = all_cols[1].find('a').string
            player_team = all_cols[2].find('a').string
            player_item.append(player_name)
            player_item.append(player_team)
            cols = all_cols[3:]
            for i in range(len(cols)):
                if len(cols[i].find_all('a')) > 0:
                    text = cols[i].find('a').string
                else:
                    text = cols[i].string
                player_item.append(text)
            player_item.append(season)
            all_players.append(player_item)

    headers.append("Season")
    print(all_players)
    print(headers)

    df = pd.DataFrame(all_players, columns=headers)
    df.to_csv('players.csv')

year_to_season = {
    "2025": "2024-25",
    "2024": "2023-24",
    "2023": "2022-23",
    "2022": "2021-22",
    "2021": "2020-21",
    "2020": "2019-20",
    "2019": "2018-19",
    "2018": "2017-18",
    "2017": "2016-17",
    "2016": "2015-16",
    "2015": "2014-15",
    "2014": "2013-14",
    "2013": "2012-13",
    "2012": "2011-12",
    "2011": "2010-11",
    "2010": "2009-10",
    "2009": "2008-09",
    "2008": "2007-08",
    "2007": "2006-07",
    "2006": "2005-06",
    "2005": "2004-05",
    "2004": "2003-04",
    "2003": "2002-03",
    "2002": "2001-02",
    "2001": "2000-01",
    "2000": "1999-00",
    "1999": "1998-99",
    "1998": "1997-98",
    "1997": "1996-97"
}


def get_award_winners():
    url = "https://www.espn.com/nba/history/awards/_/id"
    stat_id_map = {
        "MVP": 33,
        "DPOY": 39,
        "ROTY": 35,
        "6MOTY": 40,
    }
    pages = []
    for stat, id in stat_id_map.items():
        new_url = f'{url}/{id}'
        driver.get(new_url)
        pages.append((stat, driver.page_source))

    driver.quit()
    awards = []
    for award,page in pages:
        doc = BeautifulSoup(page, "html.parser")
        table = doc.find("table")
        rows = table.find_all("tr", {"class": "oddrow"})
        for row in rows:
            cols = row.find_all("td")
            if cols[0].string not in year_to_season.keys():
                break
            awards.append([award,year_to_season[cols[0].string],cols[1].string])
    print(awards)
    return awards

awards = get_award_winners()
df = pd.read_csv("players.csv")
stats = ["MVP",
        "DPOY",
        "ROTY",
        "6MOTY"]
for stat in stats:
    df[stat] = df.apply(lambda row: int ([stat,row['Season'], row['Player']] in awards), axis=1)
df.to_csv("../players_with_awards.csv", index=False)