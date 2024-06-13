import traceback

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent


async def start_browser():
    opt = webdriver.ChromeOptions()

    # opt.add_argument("--start-maximized")
    # opt.add_argument('window-size=2560,1440')

    user_agent = UserAgent()
    user_agent = user_agent.random

    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-gpu')
    opt.add_argument(f'--user-agent={user_agent}')


    # opt.add_argument('--no-sandbox')
    #opt.add_argument("--headless")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_argument('--disk-cache-size=0')

    browser = webdriver.Chrome(options=opt)
    browser.implicitly_wait(10)

    return browser


def trace(func):
    async def wrapper(*args):
        browser = await start_browser()

        result = await func(*args, browser=browser)

        browser.quit()

        return result

    return wrapper


@trace
async def parse(links: list[str], browser: WebDriver = None) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []

    for link in links:
        try:
            browser.get(link)
            result.append(await parse_element(browser))

        except Exception as e:
            print(traceback.format_exc())
            continue

    return result


async def parse_element(browser):
    price = browser.find_element(By.XPATH, "//span[@class='sales-block-offer-price__price-final']")

    codes = browser.find_elements(By.XPATH, "//span[@class='regular-characteristics__attr-description']")

    return int(price.text.replace("₽", "").replace(" ", "")), codes[len(codes) - 1].text
