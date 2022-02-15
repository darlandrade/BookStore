"""Need polishing"""

import json
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import json


def scrap():
    url = "https://www.amazon.com.br/ref=nav_logo"

    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome('C:\\Users\\darla\\anaconda3\\chromedriver.exe', options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    contador = 0

    with open("livros_aleatorios.json", "r") as file:
        livros = json.load(file)

        urls = {}
        for titulo, autor in livros.values():
            print(titulo, autor)
            contador += 1
            sleep(1)
            wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))).send_keys(f"{titulo} {autor}")
            sleep(1)
            wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))).send_keys(Keys.ENTER)

            elemento_na_pagina = driver.find_element(By.XPATH,
                                                     '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]/div/div/div/div/div[1]/span/a/div/img')
            conteudo_elemento = elemento_na_pagina.get_attribute('outerHTML')

            soup = BeautifulSoup(conteudo_elemento, "html.parser")

            # urls[f"{contador}"] = soup.image["src"]
            print(soup.img['src'])
            sleep(2)

    with open("url_livros.json", 'w') as gravar:
        obj = json.dumps(urls)
        gravar.write(obj)



if __name__ == '__main__':
    scrap()
