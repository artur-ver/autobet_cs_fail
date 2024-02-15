import time
import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import selenium.common.exceptions
from selenium_stealth import stealth

from fake_useragent import UserAgent

from dotenv import load_dotenv

load_dotenv()

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument(f"--user-agent={UserAgent().random}")
options.add_argument("--disable-blink-features=AutomationControlled")

options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
# driver.maximize_window()

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.get('https://2cs.fail/ru/wheel')

login_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(('xpath', '/html/body/app-root/div/shell-wrapper/div[2]/div/shell-header/div[3]/ui-login-button/button')))

login_button.click()

telegram_login = driver.find_element('xpath', '//*[@id="cdk-dialog-0"]/ui-dialog-login/div/div/div[4]/ui-login-dialog-button[1]/button')
telegram_login.click()

WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(('xpath', '//*[@id="login-phone"]')))

number_input = driver.find_element('xpath', '//*[@id="login-phone"]')
number_input.send_keys(os.getenv('PHONE_NUMBER'))

button_country = driver.find_element('xpath', '//*[@id="login-country-selected"]')
button_country.click()

county_input = driver.find_element('xpath', '//*[@id="login-country-search"]')
county_input.send_keys(f"{os.getenv('COUNTRY') + '\n'}")

button_phone_num = driver.find_element('xpath', '//*[@id="send-form"]/div[2]/button[2]')
button_phone_num.click()

WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located(('css selector', 'div.select-color__color.select-color__color_x2')))

driver.refresh()

WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located(('css selector', 'div.select-color__color.select-color__color_x2')))

x2_button = driver.find_element('css selector', 'div.select-color__color.select-color__color_x2')

x3_button = driver.find_element('css selector', 'div.select-color__color.select-color__color_x3')

x4_button = driver.find_element('css selector', 'div.select-color__color.select-color__color_x5')

make_bet_button = driver.find_element('css selector', 'button.bet-creator__action.btn.btn_blue')

game_status_text = driver.find_element('class name', 'information__status').text.strip().lower()

count_bet_money = driver.find_element('xpath', '//*[@id="bet-amount"]')

if count_bet_money:
    count_bet_money.clear()
    count_bet_money.send_keys('0.1')

else:
    driver.close()

while True:
    if game_status_text == 'до старта':
        main_timer = float(driver.find_element('class name', 'information__timer').text)
        print(main_timer)
        time.sleep(1)
        if main_timer <= 4:
            print('time to bet')
            price_x2x3x4 = driver.find_elements('css selector', '.color-header__bank.currency_USD')
            values = []
            #bets price
            for element in price_x2x3x4:
                text = element.text
                values.append(float(text))

            x2 = values[0]
            x3 = values[1]
            x4 = values[2]
            x35 = values[3]
            summa_x = sum((x2, x3, x4))
            print("Our sum:", summa_x)

            if summa_x < 10:
                print('Мы в нужном денежном диапазоне')

                if x3 * 2 < x2 + x4:
                    x3_button.click()
                    make_bet_button.click()

                elif x2 * 1.6 < x3 + x4 - x2:
                    x2_button.click()
                    make_bet_button.click()

                # elif x4 * 3 < (x3 + x2) * 1.4:
                #     x4_button.click()
                #     make_bet_button.click()
                else:
                    pass
            else:
                print('Too high bank')

            time.sleep(18)

    else:
        pass
