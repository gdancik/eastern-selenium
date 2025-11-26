# My Courses V2
# navigates to csc course load of Dr Dancik, G. for the specified term.
# Author: Tucker Noniewicz
# Production Date: 11/22/2025
#
# Revision 2: adding additional command line options
# 
import sys
import json

from re import search
from datetime import datetime, date

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: The file 'your_file.json' was not found.")
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from the file. Check for malformed JSON.")


def getCurrTerm():
    right_now = datetime.now()

    if datetime(right_now.year, 8, 25) < right_now < datetime(right_now.year, 12, 21):
        return 'fall'

    winter_term_start = datetime(right_now.year, 12, 22)

    if right_now.month == 1:
        winter_term_start.year = winter_term_start.year - 1

    if winter_term_start < right_now < datetime(right_now.year, 1, 14):
        return "winter"

    if datetime(right_now.year, 1, 15) < right_now < datetime(right_now.year, 5, 31):
        return "spring"
    
    if datetime(right_now.year, 6, 1) < right_now < datetime(right_now.year, 8, 24):
        return "summer"
    
    raise Exception("something has gone terribly wrong")

def getTerm(args):
    out = getCurrTerm()
    for arg in args:
        term=search("^--term=[a-zA-Z]+$", arg)
        if term != None:
            out = arg[7:]
    return out

def getSubject(args):
    out = config["mycourses_v2"]["defaults"]["subject"]
    for arg in args:
        term=search("^--subj=[a-zA-Z]{3}$", arg)
        if term != None:
            out = arg[7:]
    return out

def getInstructor(args):
    out = config["mycourses_v2"]["defaults"]["instructor"]
    for arg in args:
        term=search("^--instructor=[a-zA-Z]+$", arg)
        if term != None:
            out = arg[13:]
    return out

def getArgs(args):
    return [
        getSubject(args).lower(),
        getTerm(args).lower(),
        getInstructor(args).lower()
    ]


if (len(sys.argv)>=2 and sys.argv[1].lower() == "--help") or (len(sys.argv) > 4):
    print('Usage: mycourses [--subj=SUBJ] [--term=TERM] [--instructor=INST]')
    print('\t SUBJ: three character subject code, default: csc')
    print('\t TERM: fall, summer, spring, or winter, default: current')
    print('\t INST: last name of desired instructor. default: dancik')
    exit()


#open a chrome webpage
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

# generates the args in the form [subj, term, inst]
argArr = getArgs(sys.argv)

#navigate to course schedule selection page
driver.get("https://reg-prod.ec.easternct.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=search")


# pop out the drop down menu. 
driver.find_element(By.CLASS_NAME, "select2-arrow").click()

# enter selected term
term_text_box = driver.find_element(By.ID, "s2id_autogen1_search")
term_text_box.send_keys(argArr[1])

#wait for search to propogate
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "select2-result-label")))
term_text_box.send_keys(Keys.ENTER)

#submit form
driver.find_element(By.ID, "term-go").click()

# wait until the page loads to the next form
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search-go")))

# open the advanced search options
driver.find_element(By.ID, "advanced-search-link").click()

# enter 2nd cmnd ln arg in the subject box
subject_box = driver.find_element(By.ID, "s2id_autogen1")
subject_box.send_keys(argArr[0])

# enter dancik's name in instructor field
instructor_input = driver.find_element(By.ID, "s2id_autogen8")
instructor_input.send_keys(argArr[2])

# wait for search to propigate and select outputs
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, argArr[0].upper())))
subject_box.send_keys(Keys.ENTER)
instructor_input.send_keys(Keys.ENTER)

# send enter to submit form
actions = ActionChains(driver)
actions.send_keys(Keys.ENTER)
actions.perform()