from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import asyncio

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
    driver=start_browser()
    listProducts = []
    for link in links:
        productInfo = await parse_link(driver,link)
        listProducts.append(productInfo)
    #print(listProducts)
    driver.quit()
    return listProducts


async def parse_link(driver,link: str) -> tuple:
    # global driverClosed
    # if driverClosed:
    #     driver = wd.Chrome(options=options)
    #     driver.implicitly_wait(5)
    await asyncio.sleep(1)
    driver.get(link)

    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'Container')))
        #print("Капча!")
        driver.quit()
        driverClosed = True
        return parse_link(link)
    except TimeoutException:
        pass
        #print("Капчи нет!!!")
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    productInfo = {}
    price: int = 0
    article = soup.find('span', class_='YwVL7 _33wnU _2SUA6 _33utW IFARr _1A5yJ').find('span').text
    productInfo['article'] = article

    # Если нет в продаже
    notSale = soup.find('span', class_='_2SUA6 _3_ISO _13aK2 _1A5yJ')
    if notSale:
        price = 0
    else:
        priceElement = soup.find('h3', class_='Jdxhz').text
        price_cleaned = ''.join(filter(str.isdigit, priceElement))
        try:
            price =  int(price_cleaned)
        except:
            price = 0
    productInfo['price'] = price
    #print(productInfo)
    return (price,article)