import time
import asyncio
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures.thread import ThreadPoolExecutor
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def web_parsing(list_fio):

    executor = ThreadPoolExecutor(3)
    page_counter = 1

    async def scrape(debtor_url_text, *, loop):
        return await loop.run_in_executor(executor, scraper, debtor_url_text)

    def scraper(fio_ay):
        # options
        nonlocal page_counter
        options = webdriver.FirefoxOptions()

        # user-agent
        options.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.set_preference("dom.webdriver.enabled", False)
        options.headless = True

        driver = webdriver.Firefox(options=options)

        url = "https://old.bankrot.fedresurs.ru/ArbitrManagersList.aspx"
        try:
            driver.get(url)

            # ВСТАВКА ФИО
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "ctl00_cphBody_ArbitrManagerList1_tbLastName"))).send_keys(fio_ay.split()[0])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_cphBody_ArbitrManagerList1_tbFirstName"))).send_keys(fio_ay.split()[1])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_cphBody_ArbitrManagerList1_tbMiddleName"))).send_keys(fio_ay.split()[2])
            # ПОИСК ПО ФИО
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_cphBody_ArbitrManagerList1_ibArmSearch"))).click()
            time.sleep(5)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@title='Карточка арбитражного управляющего']"))).click()

            time.sleep(3)
            page_ay_1 = driver.page_source
            try:
                driver.execute_script("window.scrollTo(1000, document.body.scrollHeight);")
                time.sleep(2)
                driver.find_element(By.XPATH, """//a[@href="javascript:__doPostBack('ctl00$cphBody$gvMessages','Page$2')"]""").click()
                time.sleep(4)

                page_ay_2 = driver.page_source
            except:
                page_ay_2 = ""
            try:
                driver.execute_script("window.scrollTo(1000, document.body.scrollHeight);")
                time.sleep(2)
                driver.find_element(By.XPATH, """//a[@href="javascript:__doPostBack('ctl00$cphBody$gvMessages','Page$3')"]""").click()
                time.sleep(4)
                driver.execute_script("window.scrollTo(1000, document.body.scrollHeight);")

                page_ay_3 = driver.page_source
            except:
                page_ay_3 = ""
            url_ay = driver.current_url
            return [url_ay, page_ay_1, page_ay_2, page
