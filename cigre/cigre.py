from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

import time

downloads_dir = 'D:\Downloads'
url = "https://e-cigre.org/search_results.asp?page=1&nb_limit=9&most_popular=Y&keywords_title_ref=&publication_type=1&publication_author="

options = Options()

options.set_preference('browser.download.folderList', 2)
options.set_preference('browser.download.dir', downloads_dir)

options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')

driver = webdriver.Firefox(options=options)

driver.get(url)

username_field = driver.find_element(By.NAME, "login")
password_field = driver.find_element(By.NAME, "pwd")
username_field.send_keys("lrozik@morenergy.gr")
password_field.send_keys("RES_D&C_2023")
password_field.send_keys(Keys.RETURN)

sumbit_button = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/div[1]/div[2]/form/input[3]')
sumbit_button.click()
time.sleep(10)

page_panel = [navigator.text for navigator in driver.find_elements(By.TAG_NAME, 'td')]

while '>' in page_panel:
    for i in range(9):
        books = list(driver.find_elements(By.CLASS_NAME, 'titre'))
        books[i].click()
        time.sleep(5)

        download = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/section/div[1]/div[10]/div[2]/div[2]/a')
        download.click()
        time.sleep(5)
        
        window_handles = driver.window_handles

        for handle in window_handles:
            if handle != driver.current_window_handle:
                driver.switch_to.window(handle)
                driver.close()
                break

        driver.switch_to.window(window_handles[0])
        driver.back()

    page_panel = driver.find_elements(By.TAG_NAME, 'td')
    page_panel_text = [navigator.text for navigator in page_panel]

    if '>' in page_panel_text:
        next_page_index = page_panel_text.index('>')
        next_page = page_panel[next_page_index]
        next_page.click()
        time.sleep(5)
    else:
        break
driver.close()