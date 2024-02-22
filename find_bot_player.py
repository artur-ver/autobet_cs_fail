import time
import csv

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_stealth import stealth

from fake_useragent import UserAgent

# Setting up options for the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--incognito')  # Incognito mode
options.add_argument('--headless')   # Headless mode
options.add_argument(f"--user-agent={UserAgent().random}")  # Random User-Agent
options.add_argument("--disable-blink-features=AutomationControlled")  # Disabling certain automation-related features

options.add_experimental_option('excludeSwitches', ['enable-automation'])  # Excluding the enable-automation option
options.add_experimental_option('useAutomationExtension', False)          # Disabling the automation extension

# Creating a ChromeDriver service
service = Service(executable_path=ChromeDriverManager().install())

# Creating an instance of the Chrome WebDriver with options and service
driver = webdriver.Chrome(service=service, options=options)

# Applying stealth mode to avoid detection of automation
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# Opening the web page
driver.get('https://2cs.fail/ru/wheel')

# Refreshing the page
driver.refresh()

# Opening the CSV file to append data
with open('file.csv', 'a', newline='', encoding='utf-8') as csvfile_append:
    writer = csv.writer(csvfile_append, delimiter=';')

    while True:  # Infinite loop
        # Waiting for an element to appear on the page
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(('css selector', 'wheel-game-color')))

        # Getting a list of users with different bets (x2, x3, x4)
        big_block_players = driver.find_elements('css selector', 'wheel-game-color')

        x2_users = big_block_players[0].find_elements('css selector', 'wheel-bet')
        x3_users = big_block_players[1].find_elements('css selector', 'wheel-bet')
        x4_users = big_block_players[2].find_elements('css selector', 'wheel-bet')

        # Processing users with x2 bets
        for x2_user in x2_users:
            try:
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located(('css selector', '.wheel-bet__bank.currency_USD')))
            except Exception:
                pass

            try:
                # Parsing the username and bet amount
                money = float(x2_user.find_element('css selector', '.wheel-bet__bank.currency_USD').text)
                name = x2_user.find_element('css selector', '.wheel-bet__nickname.nickname.link').text.strip().replace(' ', '')
            except Exception:
                pass

            if money > 10 and name:
                # If the bet amount is greater than 10 and the username is present, the data is added to the CSV file
                with open('file.csv', 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csvfile.read()
                    if name not in reader:
                        with open('file.csv', 'a', newline='', encoding='utf-8') as csvfile_append:
                            writer = csv.writer(csvfile_append, delimiter=';')
                            writer.writerow([name, money])
            print('x 2', money, name, end='\n')

        # Processing users with x3 bets
        for x3_user in x3_users:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located(('css selector', '.wheel-bet__bank.currency_USD')))
            try:
                money = float(x3_user.find_element('css selector', '.wheel-bet__bank.currency_USD').text)
                name = x3_user.find_element('css selector', '.wheel-bet__nickname.nickname.link').text.strip().replace(' ', '')
            except Exception:
                pass

            if money > 10 and name:
                with open('file.csv', 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csvfile.read()
                    if name not in reader:
                        with open('file.csv', 'a', newline='', encoding='utf-8') as csvfile_append:
                            writer = csv.writer(csvfile_append, delimiter=';')
                            writer.writerow([name, money])
            print('x 3', money, name, end='\n')

        # Processing users with x4 bets
        for x4_user in x4_users:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located(('css selector', '.wheel-bet__bank.currency_USD')))
            try:
                money = float(x4_user.find_element('css selector', '.wheel-bet__bank.currency_USD').text)
                name = x4_user.find_element('css selector', '.wheel-bet__nickname.nickname.link').text.strip().replace(' ', '')
            except Exception:
                pass

            if money > 10 and name:
                with open('file.csv', 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csvfile.read()
                    if name not in reader:
                        with open('file.csv', 'a', newline='', encoding='utf-8') as csvfile_append:
                            writer = csv.writer(csvfile_append, delimiter=';')
                            writer.writerow([name, money])
                    else:
                        pass
            print('x 4', money, name, end='\n')

        # Pause for 5 seconds before looping again
        time.sleep(5)
