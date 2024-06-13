import asyncio

from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driverClosed = False
options = wd.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disk-cache-size=0')
options.add_argument("--ignore-certificate-errors")
options.add_argument("--enable-javascript")
options.add_argument("start-maximized")


def start_browser():
    driver = wd.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


async def yandex_parser(links: list) -> list:
    driver = start_browser()
    listProducts = []
    for link in links:
        productInfo = await parse_link(driver, link)
        if productInfo is not None:
            listProducts.append(productInfo)
    driver.quit()
    return listProducts


async def parse_link(driver, link: str) -> tuple | None:
    await asyncio.sleep(1)
    driver.get(link)

    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'Container')))
        driver.quit()
        return
    except TimeoutException:
        pass

    soup = BeautifulSoup(driver.page_source, "html.parser")

    price: int = 0

    article = soup.find('span', class_='YwVL7 _33wnU _2SUA6 _33utW IFARr _1A5yJ').find('span').text

    # Если нет в продаже
    notSale = soup.find('span', class_='_2SUA6 _3_ISO _13aK2 _1A5yJ')
    if notSale:
        price = 0
    else:
        priceElement = soup.find('h3', class_='Jdxhz').text
        price_cleaned = ''.join(filter(str.isdigit, priceElement))
        try:
            price = int(price_cleaned)
        except:
            price = 0

    return price, article
