from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import random

driver = webdriver.Firefox()

driver.get("http://egzamin-inf.pl")

button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "getRandomQuestion")))

buttons = ["b_a", "b_b", "b_c", "b_d"]

times = 10

# --------------------------------

def load_page():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "b_a")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "b_b")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "b_c")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "b_d")))

def next_answer():
    button.click()
    time.sleep(0.5)

def click_random():
    option = driver.find_element(By.ID, random.choice(buttons))
    option.click()
    time.sleep(0.5)

def read_text():
    res = driver.find_element(By.ID, "res1")
    print(res.text)
    time.sleep(0.5)

next_answer()

for _ in range(times):
    load_page()
    next_answer()

    click_random()
    read_text()

driver.quit()
