#!/Users/dancikg/opt/anaconda3/bin/python

# Get my course schedule

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import sys


if (len(sys.argv) == 2 and sys.argv[1].lower() != '--csc') or len(sys.argv) > 2 :
     print('Usage: mycourses [--csc]')
     exit()


driver = webdriver.Firefox()
driver.implicitly_wait(10)

driver.get("https://ssb-prod.ec.easternct.edu/PROD/bwskfcls.p_termsel")


# click Advanced search
elem= driver.find_elements_by_tag_name('input')
elem[1].click()

both = driver.find_element_by_id('oc_id')
both.click()



# select 'Computer Science' (direct selection does not work)
if len(sys.argv) > 1 and sys.argv[1].lower() == '--csc':  
    select = Select(driver.find_element_by_id('subj_id'))
    subj = driver.find_element_by_id('subj_id')
    subj.send_keys('c')
    for i in range(20) :
        subj.send_keys(Keys.DOWN)
        if select.first_selected_option.text == 'Computer Science' :
            break


else : 
    # select instructor (direct selection does not work)
    select = Select(driver.find_element_by_id('instr_id'))
    name = driver.find_element_by_xpath("//select[@id='instr_id']/option[@value='8A92261F1A2BAAECB202A0A1EF704C67']")
    
    name.send_keys('D')
    
    for i in range(20) :
        name.send_keys(Keys.DOWN)
        if select.first_selected_option.text == 'Dancik, Garrett M.' :
            break


# submit
btn = driver.find_element_by_name('SUB_BTN')
btn.click()
