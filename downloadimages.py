from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

def download_images(query, n, path):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://images.google.com/')
    box = driver.find_element(By.CSS_SELECTOR, '.gLFyf')
    box.send_keys(query)
    box.send_keys(Keys.ENTER)
    def scroll_to_bottom():
        last_height = driver.execute_script('\
        return document.body.scrollHeight')

        while True:
            driver.execute_script('\
            window.scrollTo(0,document.body.scrollHeight)')

            time.sleep(3)

            new_height = driver.execute_script('\
            return document.body.scrollHeight')

            try:
                driver.find_element(By.CSS_SELECTOR, ".YstHxe input").click()
                time.sleep(3)
            except:
                pass

            if new_height == last_height:
                break
            
            last_height = new_height
    
    scroll_to_bottom()
    
    for i in range(10, 10+n):
        try:
            img = driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img')
            img.screenshot(path + query + str(i) + '.png')
            time.sleep(0.2)
    
        except Exception as e:
            print(e)
            continue

    driver.close()