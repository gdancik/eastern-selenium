from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import datetime

def getTerm(args) :
   for term in ['--fall','--spring','--summer','--winter'] :
     if term in args :
      return term[2:].capitalize() 
   return None

def getSubject(args):
    for term in ['--csc']:
        if term in args:
            return term[2:].capitalize()
    return None


if (len(sys.argv) == 2 and sys.argv[1].lower() == '--help' or len(sys.argv) > 3) or len(sys.argv) < 2 :
     print('Usage: mycourses [--subj] [--term]')
     print('\t subj: three character subject code,e.g., csc')
     print('\t term: fall, summer, spring, or winter')
     exit()


#open a chrome webpage
driver = webdriver.Chrome()
driver.implicitly_wait(10)

#navigate to course schedule selection page
driver.get("https://reg-prod.ec.easternct.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=search")


# pop out the drop down menu. 
driver.find_element(By.CLASS_NAME, "select2-arrow").click()

# enter selected term
term_text_box = driver.find_element(By.ID, "s2id_autogen1_search")
term_text_box.send_keys(getTerm(sys.argv) + " " + str(datetime.date.today().year))

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
subject_box.send_keys(getSubject(sys.argv))

# enter dancik's name in instructor field
instructor_input = driver.find_element(By.ID, "s2id_autogen8")
instructor_input.send_keys("Dancik")

# wait for search to propigate and select outputs
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CSC")))
subject_box.send_keys(Keys.ENTER)
instructor_input.send_keys(Keys.ENTER)


# sanity wait for submit button to be available then click it
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search-go")))
submit_bttn = driver.find_element(By.ID, "search-go")
submit_bttn.click()

if(input()):
    driver.quit()


