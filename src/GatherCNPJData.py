import os
import psycopg2
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def GetCNPJFromDB(conn):
    query = """
        SELECT 
            DISTINCT(cnpj)
        FROM 
            regulartrips
        """
    
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

def PreProcessName(name):
    result = "".join(name.split("-")[:-2])
    return result.rstrip()

if __name__ == "__main__":
    conn = psycopg2.connect(host='localhost', port=5432, dbname='ANTT', user=os.environ["PGDBUSER"], password=os.environ["PGDBPASSWORD"])
    cnpjs = GetCNPJFromDB(conn)

    baseUrl = "https://cnpj.biz/"
    className = "post-title.empresa-title"

    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    result = []

    for cnpj in cnpjs:
        cnpj = cnpj[0]

        finalUrl = baseUrl + cnpj
        driver.get(finalUrl)

        try:
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, className))
                )
            companyName = PreProcessName(element.text)
            result.append((cnpj, companyName))
            print(f"Successfully fetched name from {cnpj}: {companyName}")
        except Exception as e:
            print(e)
            print(f"Failed to fetch company name from cnpj: {cnpj}, {finalUrl}")
            driver.print_page()
        
        time.sleep(2)
        
    conn.close()
    driver.close()

    filePath = "../data/companyNames.csv"
    df = pd.DataFrame(result, columns=['cnpj', 'name'])
    df.to_csv(filePath)
