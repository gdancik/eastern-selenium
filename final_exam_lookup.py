#!/Users/dancikg/opt/anaconda3/bin/python
from selenium import webdriver
import sys

if len(sys.argv) != 2:
    print("Usage: final_exam_lookup 'MWF 9-9:50'")
    exit();

# the value of "User-Agent" should be set appropriately
headers = {"User-Agent": "FinalExamLookup/1.0"}
myurl = 'https://www.easternct.edu/registrar/final-examinations.html'

#query = 'MWF 9-9:50'
query = sys.argv[1]

driver = webdriver.Firefox()
driver.get(myurl)


source = driver.page_source


source = source.replace(query, '<span style = "background-color:yellow">' + query + '</span>')


myfile = "/Users/dancikg/Downloads/final_exam_schedule.html"

with open(myfile, "w") as f:
    f.write(source)
    
    
driver.get("file://" + myfile)







