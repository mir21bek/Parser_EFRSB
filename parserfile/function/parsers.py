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
        options = webdriver.ChromeOptions()

        # user-agent
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        # options.page_load_strategy = 'none'

        driver = webdriver.Chrome(options=options)

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
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{fio_ay}')]"))).click()

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
            return [url_ay, page_ay_1, page_ay_2, page_ay_3]

        except Exception as ex:
            # print(111, ex)
            return ["Ошибка", "Ошибка", "Ошибка", "Ошибка"]
        finally:
            print(f"{page_counter}: Страница скопирована")
            page_counter += 1
            driver.quit()

    async def main(debtors_url_text):
        tasks = []
        for debtor_url_text in debtors_url_text:
            tasks.append(scrape(debtor_url_text, loop=asyncio.get_event_loop()))

        results = await asyncio.gather(*tasks)
        all_debtor = [result for result in results if result]
        return all_debtor

    loop = asyncio.get_event_loop()
    all_debtor = loop.run_until_complete(main(list_fio))

    return all_debtor


def web_debtor_inn(debtors_url):

    executor = ThreadPoolExecutor(3)
    inn_counter = 1

    async def scrape(debtors_url, *, loop):
        return await loop.run_in_executor(executor, scraper, debtors_url)

    def scraper(debtors_url):
        # options
        nonlocal inn_counter
        options = webdriver.ChromeOptions()

        # user-agent
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        # options.page_load_strategy = 'eager'
        options.page_load_strategy = 'none'

        driver = webdriver.Chrome(options=options)

        try:
            driver.get(debtors_url[0])
            debtor_inn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ctl00_cphBody_lblINN"))).text

            return [debtors_url[0], debtors_url[1], debtor_inn]
        except Exception as ex:
            # print(111, ex)
            return False
        finally:
            print(f"{inn_counter}: Инн Скопирован")
            inn_counter += 1
            driver.quit()

    async def main(debtors_url):
        tasks = []
        for debtor_url_text in debtors_url:
            tasks.append(scrape(debtor_url_text, loop=asyncio.get_event_loop()))

        results = await asyncio.gather(*tasks)
        all_debtor = [result for result in results if result]
        return all_debtor

    loop = asyncio.get_event_loop()
    all_debtor = loop.run_until_complete(main(debtors_url))
    return all_debtor


def html_parse(all_pages):
    try:
        first_soup = BeautifulSoup(all_pages[1], "html.parser")
        inn_ay = int(first_soup.find("tr", id="ctl00_cphBody_trInn").text.split("ИНН")[1])
        cro_ay_element = first_soup.find("a", id="ctl00_cphBody_lnkSro")
        try:
            cro_ay_text = cro_ay_element.text.strip()
        except:
            cro_ay_text = ""
        try:
            cro_ay_url = "https://old.bankrot.fedresurs.ru" + str(cro_ay_element["href"])
        except:
            cro_ay_url = ""

        all_debtor = []
        all_debtor_name = []
        all_debtor_url = []
        for idx, page in enumerate(all_pages):
            if idx != 0:
                if page:
                    try:
                        soup = BeautifulSoup(page, "html.parser")
                        all_element_debtor = soup.find("table", id="ctl00_cphBody_gvMessages").find_all("tr")
                        for element_debtor in all_element_debtor:
                            try:
                                all_data_publication = datetime.datetime.strptime(element_debtor.find_next().text.strip()[0:10], '%d.%m.%Y')
                                if all_data_publication >= datetime.datetime(2023, 1, 1):
                                    block_debtor = element_debtor.find_all("a")[-1]
                                    debtor_url = "https://old.bankrot.fedresurs.ru" + block_debtor["href"]
                                    debtor_name = block_debtor.text.strip()
                                    if [debtor_url, debtor_name] not in all_debtor:
                                        all_debtor += [[debtor_url, debtor_name]]
                                        all_debtor_name += [debtor_name]
                                        all_debtor_url += [debtor_url]
                            except Exception as ex:
                                # print(1111, ex)
                                ...
                    except Exception as ex:
                        # print(2222, ex)
                        ...
        # return inn_ay, cro_ay_text, cro_ay_url.strip(), all_debtor_name, all_debtor_url
        return inn_ay, cro_ay_text, cro_ay_url.strip(), all_debtor
    except:
        return False, False, False, False
