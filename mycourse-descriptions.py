#!/usr/bin/python3
 
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from eastern import getCurrTerm

parser = argparse.ArgumentParser(
        prog="mycourses",
        description="Query courses by subject, term, and instructor"
    )

parser.add_argument(
    "--subj",
    default="CSC",
    help="keyword for subject (defaults to CSC)"
)

parser.add_argument(
    "--term",
    default=None,    
    help="term: Spring 2026"
)


args = parser.parse_args()

# Extract arguments
subj = args.subj
term = args.term

if not term :
    term = getCurrTerm()


# Use Firefox
driver = webdriver.Firefox()
driver.implicitly_wait(10)

#navigate to course schedule selection page
driver.get("https://reg-prod.ec.easternct.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=courseSearch")


# enter selected term
term_text_box = driver.find_element(By.ID, "s2id_autogen1")
term_text_box.send_keys(term)

def wait_and_send(driver, by, value, text):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))    
    element = driver.find_element(by, value)
    element.send_keys(text)
    return element

#wait for search to propogate
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "select2-result-label")))

driver.find_element(By.CLASS_NAME, "select2-result-label").click()

# wait until the page loads to the next form
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "term-go")))

driver.find_element(By.ID, "term-go").click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search-fields")))

if subj :
    subj_box = wait_and_send(driver, By.ID, 's2id_autogen1', subj)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "select2-highlighted")))
    subj_box.send_keys(Keys.ENTER)

driver.find_element(By.ID, "search-go").click()


wait_and_send(driver, By.CLASS_NAME, 'page-size-select', '50')

