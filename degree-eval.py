#!/Users/dancikg/opt/anaconda3/bin/python

# Pull up degree evals for student by last name

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import Select
import pickle
import os.path
import sys
import time

if len(sys.argv) != 2 :
    print('Usage: degree-eval lastName')
    exit()

lastName = sys.argv[1]

driver = webdriver.Firefox()
driver.implicitly_wait(10)
cfile = '/Users/dancikg/Downloads/degree_eval.p'


if os.path.exists(cfile) :
    
    driver.get('https://dw-prod.ec.easternct.edu')
    cookies = pickle.load( open (cfile, "rb") )

    for c in cookies :
        driver.add_cookie(c)

    driver.get("https://dw-prod.ec.easternct.edu/responsiveDashboard/?PORTALSTUID=10250547&SCRIPT=SD2WORKS")


else :
    driver.get("https://dw-prod.ec.easternct.edu/responsiveDashboard/?PORTALSTUID=10250547&SCRIPT=SD2WORKS")
    input("Enter credentials on page and press any key and enter when done: ")
    cookies = driver.get_cookies()
    pickle.dump(cookies, open( cfile, "wb") )



# click Advanced search
elem= driver.find_elements_by_tag_name('button')
elem[0].click()

# enter student's name
el_ln = driver.find_element_by_id('lastName')
el_ln.clear()
el_ln.send_keys(lastName)
el_ln.send_keys(Keys.RETURN)

