#!/Users/dancikg/opt/anaconda3/bin/python

# Pull up degree evals for student by last name

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import Select
import pickle
import os.path
import sys
import time

valid = len(sys.argv) == 2 or len(sys.argv) == 3 or (len(sys.argv) >= 3 and sys.argv[len(sys.argv)-1] == '--reset')

if not valid:
    print('Usage: degree-eval lastName [firstName] [--reset]')
    exit()

lastName = sys.argv[1]
firstName = None
if len(sys.argv) > 2:
	firstName = sys.argv[2]
	if firstName == '--reset' :
		firstName = None

if '--reset' in sys.argv:
	os.remove(cfile)

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
elem[2].click()

# enter student's last name
el_ln = driver.find_element_by_id('lastName')
el_ln.clear()
el_ln.send_keys(lastName)

if not firstName:
	el_ln.send_keys(Keys.RETURN)
	exit()

# enter student's first name
el_ln = driver.find_element_by_id('firstName')
el_ln.clear()
el_ln.send_keys(firstName)
el_ln.send_keys(Keys.RETURN)


