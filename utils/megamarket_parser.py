import traceback
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def start_browser():
    opt = webdriver.ChromeOptions()

    opt.add_argument("--start-maximized")
    opt.add_argument('window-size=2560,1440')

    opt.add_argument('--disable-gpu')

    opt.add_argument('--no-sandbox')

    opt.add_argument('--disk-cache-size=0')

    browser = webdriver.Chrome(options=opt)
    browser.implicitly_wait(10)

    return browser


def trace(func):
    def wrapper(*args):
        browser = start_browser()

        result = func(*args, browser=browser)

        browser.quit()
        return result

    return wrapper


@trace
def parse(links: list[str], browser: WebDriver = None) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []

    for link in links:
        try:
            browser.get(link)
            result.append(parse_element(link, browser))

        except Exception as e:
            print(traceback.format_exc())
            return result

    return result


def parse_element(link, browser):
    title = browser.find_element(By.XPATH,
                                 "//h1[@itemprop='name'][@class='pdp-header__title pdp-header__title_only-title']")
    price = browser.find_element(By.XPATH, "//span[@class='sales-block-offer-price__price-final']")

    codes = browser.find_elements(By.XPATH, "//span[@class='regular-characteristics__attr-description']")

    return int(price.text.replace("₽", "").replace(" ", "")), codes[len(codes) - 1].text
