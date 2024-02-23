import time
import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv

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


def login_telegram():
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

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(('css selector', 'wheel-game-color')))

    global registration
    registration = True


WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located(('css selector', 'div.select-color__color.select-color__color_x2')))

driver.refresh()

WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located(('css selector', 'div.select-color__color.select-color__color_x2')))

game_status_text = driver.find_element('css selector', '.information__status').text.strip().lower()

count_bet_money = driver.find_element('xpath', '//*[@id="bet-amount"]')

registration = False
price_bot_to_csv = 30
if count_bet_money:
    count_bet_money.clear()
    count_bet_money.send_keys('0.1')

else:
    driver.close()

if not os.path.isfile('file.csv'):
    with open('file.csv', 'w', newline='', encoding='utf-8') as csvfile:
        pass


def bot_check():
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(('css selector', 'wheel-game-color')))

    big_block_players = driver.find_elements('css selector', 'wheel-game-color')

    x2_users = big_block_players[0].find_elements('css selector', 'wheel-bet')
    x3_users = big_block_players[1].find_elements('css selector', 'wheel-bet')
    x4_users = big_block_players[2].find_elements('css selector', 'wheel-bet')

    found_high_balance = False  # Flag to track if anyone has balance > 10

    for x2_user in x2_users:
        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(('css selector', '.wheel-bet__bank.currency_USD')))
        except Exception:
            pass

        try:
            money = float(x2_user.find_element('css selector', '.wheel-bet__bank.currency_USD').text)
            name = x2_user.find_element('css selector', '.wheel-bet__nickname.nickname.link').text.strip().replace(' ', '')
        except Exception:
            pass
        else:
            if money >= price_bot_to_csv and name:
                found_high_balance = True
                with open('file.csv', 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csvfile.read()
                    if name not in reader:
                        with open('file.csv', 'a', newline='', encoding='utf-8') as csvfile_append:
                            writer = csv.writer(csvfile_append, delimiter=';')
                            writer.writerow([name, money])
        #print('x 2', money, name, end='\n')

    for x3_user in x3_users:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(('css selector', '.wheel-bet__bank.currency_USD')))
        try:
            money = float(x3_user.find_element('css selector', '.wheel-bet__bank.currency_USD').text)
            name = x3_user.find_element('css selector', '.wheel-bet__nickname.nickname.link').text.strip().replace(' ', '')
        except Exception:
            pass
        else:
            if money >= price_bot_to_csv and name:
                found_high_balance = True
                with open('file.csv', 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csvfile.read()
                    if name not in reader:
                        with open('file.csv', 'a', newline='', encoding='utf-8') as csvfile_append:
                            writer = csv.writer(csvfile_append, delimiter=';')
                            writer.writerow([name, money])
        #print('x 3', money, name, end='\n')

    for x4_user in x4_users:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(('css selector', '.wheel-bet__bank.currency_USD')))
        try:
            money = float(x4_user.find_element('css selector', '.wheel-bet__bank.currency_USD').text)
            name = x4_user.find_element('css selector', '.wheel-bet__nickname.nickname.link').text.strip().replace(' ', '')
        except Exception:
            pass
        else:
            if money >= price_bot_to_csv and name:
                found_high_balance = True
                with open('file.csv', 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csvfile.read()
                    if name not in reader:
                        with open('file.csv', 'a', newline='', encoding='utf-8') as csvfile_append:
                            writer = csv.writer(csvfile_append, delimiter=';')
                            writer.writerow([name, money])
        #print('x 4', money, name, end='\n')

    return not found_high_balance


login_telegram()


def main():
    while True:
        try:
            if game_status_text == 'до старта' and bot_check(): #untill start
                x2_button = driver.find_element('css selector', 'div.select-color__color.select-color__color_x2')

                x3_button = driver.find_element('css selector', 'div.select-color__color.select-color__color_x3')

                x4_button = driver.find_element('css selector', 'div.select-color__color.select-color__color_x5')

                make_bet_button = driver.find_element('css selector', 'wheel-home-bet-creator')

                try:
                    main_timer = float(driver.find_element('class name', 'information__timer').text)

                    print(main_timer)

                    time.sleep(1)
                    if main_timer <= 4.5:   #TACTIC 
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

                        if summa_x < 20:    #TACTIC sum banc
                            print('Мы в нужном денежном диапазоне')

                            if x3 * 2 < x2 + x4:    #TACTIC x3
                                WebDriverWait(driver, 20).until(
                                    EC.visibility_of_element_located(
                                        ('css selector', 'div.select-color__color.select-color__color_x3')))

                                x3_button.click()
                                make_bet_button.click()

                            if x2 * 1.6 < x3 + x4 - x2:     #TACTIC x2
                                WebDriverWait(driver, 20).until(
                                    EC.visibility_of_element_located(
                                        ('css selector', 'div.select-color__color.select-color__color_x2')))

                                x2_button.click()
                                make_bet_button.click()

                            # elif x4 * 3 < (x3 + x2) * 1.4:    #TACTIC 
                            # WebDriverWait(driver, 20).until(
                            #     EC.visibility_of_element_located(('css selector', 'div.select-color__color.select-color__color_x5')))
                            #     x4_button.click()
                            #     make_bet_button.click()
                            else:
                                pass
                        else:
                            print('Too high bank')

                        time.sleep(18)
                except ValueError:                  #On situation when main_timer is str
                    pass

            else:
                print('somebody have more than 10$ bet')
                time.sleep(5)

        except UnboundLocalError:
            print('error')


if __name__ == '__main__':
    if registration:
        main()
