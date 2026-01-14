#!/usr/bin/python3

# Modified by GMD to use Firefeox, argparse and output information to console

# My Courses V2
# navigates to csc course load of Dr Dancik, G. for the specified term.
# Author: Tucker Noniewicz
# Production Date: 11/22/2025
#
# Revision 2: adding additional command line options
# 

import argparse

from time import sleep
from tabulate import tabulate

from datetime import datetime, date

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

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

parser.add_argument(
    "--instructor",
    default="None",
    help="keyword for desired instructor (default: None)"
)

args = parser.parse_args()

# Extract arguments
subj = args.subj
term = args.term

if args.instructor :
    print("instructor not yet implemented")
    exit()

if not term :
    term = getCurrTerm()

instructor = args.instructor

# Use Firefox
driver = webdriver.Firefox()
driver.implicitly_wait(10)

#navigate to course schedule selection page
driver.get("https://reg-prod.ec.easternct.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=search")


# pop out the drop down menu. 
driver.find_element(By.CLASS_NAME, "select2-arrow").click()

# enter selected term
term_text_box = driver.find_element(By.ID, "s2id_autogen1_search")
term_text_box.send_keys(term)

def wait_and_send(driver, by, value, text):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))    
    element = driver.find_element(by, value)
    element.send_keys(text)
    return element

#wait for search to propogate
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "select2-highlighted")))
term_text_box.send_keys(Keys.ENTER)

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

element = WebDriverWait(driver, 10).until(
    lambda d: d.find_element(By.CLASS_NAME, "total-pages").text.strip() == "1"
)

tr = driver.find_elements(By.TAG_NAME, 'tr')

abbreviate_day = {'Monday': 'M', 
             'Tuesday': 'T',
             'Wednesday': 'W',
             'Thursday': 'R',
             'Friday': 'F'
}

def get_cell_value(x) :
    if "<li" in x.get_attribute('innerHTML') : 
        li_values = x.find_elements(By.TAG_NAME, 'li')
        days = [l.get_attribute('data-name') for l in li_values if l.get_attribute('aria-checked') == 'true']
        days = [abbreviate_day.get(d, '?') for d in days]
        s = x.find_elements(By.TAG_NAME, 'span')
        return ''.join(days) + ', ' + s[1].text
    return x.text

def map_row(tr, type) :
    return list(map(lambda x: get_cell_value(x), tr.find_elements(By.TAG_NAME, type)))

header = map_row(tr[0], 'th')
rows = [map_row(r, 'td') for r in tr[1:]]
df = pd.DataFrame(rows, columns = header)
df = df[['Subject', 'Course Number', 'Section', 'Title', 'Instructor', 'Meeting Times', 'Status']]


def format_seats(x) :
    ret = f"{x[1] - x[0]}/{x[1]}"
    if x[0] == 0 :
        return ret + '*'
    return ret
   
df["Status"] = df["Status"].str.extract(r"(\d+)\s+of\s+(\d+)").astype(int).apply(format_seats, axis=1)
df["Instructor"] = df["Instructor"].str.replace('(Primary)', '')
df = df.applymap(str.strip)

print(tabulate(df, headers='keys', tablefmt='grid', showindex = False))

'''
# open the advanced search options
driver.find_element(By.ID, "advanced-search-link").click()

# enter 2nd cmnd ln arg in the subject box
subject_box = driver.find_element(By.ID, "s2id_autogen1")
subject_box.send_keys(subj)

if instructor :
    # enter instructor's name
    instructor_input = driver.find_element(By.ID, "s2id_autogen8")
    instructor_input.send_keys(instructor)

# wait for search to propigate and select outputs
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, argArr[0].upper())))
subject_box.send_keys(Keys.ENTER)
instructor_input.send_keys(Keys.ENTER)

# send enter to submit form
actions = ActionChains(driver)
actions.send_keys(Keys.ENTER)
actions.perform()
'''