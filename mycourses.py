#!/usr/bin/python3

# Get my course schedule

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import sys
from selenium.webdriver.support.select import Select


if (len(sys.argv) == 2 and sys.argv[1].lower() == '--help' or len(sys.argv) > 3) :
     print('Usage: mycourses [--csc|--dsc|--mat] [--back]')
     exit()


driver = webdriver.Firefox()
driver.implicitly_wait(10)

driver.get("https://ssb-prod.ec.easternct.edu/PROD/bwskfcls.p_termsel")


# select term
elem = driver.find_elements(by = 'id', value = 'term_id')
if '--back' in sys.argv :
	s = Select(elem[0])
	s.select_by_index(2)

# submit term
elem= driver.find_elements(by = 'tag name', value = 'input')
elem[1].click()


# select both for open/close
both = driver.find_element(by = 'id', value = 'oc_id')
both.click()


# select 'Computer Science' (direct selection does not work)
if len(sys.argv) > 1 and sys.argv[1].lower() != '--back': 
    subj = sys.argv[1].upper().strip('--') 
    select = Select(driver.find_element(by = 'id', value = 'subj_id'))
    subj_input = driver.find_element(by = 'id', value = 'subj_id')
    subj_input.send_keys(Keys.DOWN)
    print('looking at', select.first_selected_option.get_attribute('value'))
    for i in range(100) :
        print('looking at', select.first_selected_option.get_attribute('value'))
        if select.first_selected_option.get_attribute('value') == subj :
            break
        subj_input.send_keys(Keys.DOWN)
else : 
    # select instructor (direct selection does not work)
    select = Select(driver.find_element(by = 'id', value = 'instr_id'))
    name = driver.find_element_by_xpath("//select[@id='instr_id']/option[@value='8A92261F1A2BAAECB202A0A1EF704C67']")
    
    name.send_keys('D')
    
    for i in range(20) :
        name.send_keys(Keys.DOWN)
        if select.first_selected_option.text == 'Dancik, Garrett M.' :
            break


# submit
btn = driver.find_element(by = 'name', value = 'SUB_BTN')
btn.click()
