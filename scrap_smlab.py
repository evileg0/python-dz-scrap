from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import sqlite3


def scrap_smlab():
    conn = sqlite3.connect('moex_db.db')
    cursor = conn.cursor()
    options = Options()

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://smart-lab.ru/q/index_stocks/IMOEX/"
    driver.get(url=url)
    wait = WebDriverWait(driver, 10)
    table_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "main__table")))

    l_rbl = driver.find_element(By.CSS_SELECTOR, "[class=flex-table__l-table]")
    l_lst = l_rbl.find_elements(By.CSS_SELECTOR, "[class=trades-table__name]")
    names = [element.text for element in l_lst]
    tickers = [element.find_element(By.TAG_NAME, "a").get_property('href').split('/')[-1] for element in l_lst]

    df = pd.DataFrame({'name': names})
    df['ticker'] = tickers

    r_rbl = driver.find_element(By.CSS_SELECTOR, "[class=flex-table__r-tbody]")
    r_lst = r_rbl.find_elements(By.TAG_NAME, "tr")

    per_row =[]
    price_row =[]
    for element in r_lst:
        percent = element.find_element(By.CSS_SELECTOR, "[class=trades-table__change-per]").text
        per_row.append(percent.strip())
        price = element.find_element(By.CSS_SELECTOR, "[class=trades-table__price]").text
        price_row.append(price.strip())
    df['percent'] = per_row
    df['price'] = price_row
    df['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(df)
    df.to_sql('stocks', conn, if_exists='append', index=False)

if __name__ == "__main__":
    scrap_smlab()