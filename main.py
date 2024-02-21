# проект посвящен автоматизации ручного труда в рекламе, с помощью библиотеки Selenium
# from take_accs import take_accounts
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import pickle
import time


def load_cookie(driver, login: str):
    path = f"E:\\OSPanel\\domains\\my_life\\ad_fb\\cookies\\{login}_cookies"
    cookies = pickle.load(open(path, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)


def save_cookie(driver, login: str):
    pickle.dump(driver.get_cookies(), open(f"cookies/{login}_cookies", "wb"))


def driver_selenium():

    service = Service(r'E:\OSPanel\domains\selenium\chromedriver\chromedriver.exe')
    useragent = UserAgent()

    options = webdriver.ChromeOptions()
    # убирает режим автоматизации, нас не видят как бота
    options.add_argument('--disable-blink-features=AutomationControlled')
    # Отключает логи, кроме первой строки инициализации:
    options.add_argument('--log-level=3')
    options.add_argument(f"user-agent={useragent.random}")
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    driver = webdriver.Chrome(service=service, options=options)

    return driver
