from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import EncypData
import json
import time

#Function to time out the excecution of the driver
def wait(sec):

    driver.implicitly_wait(sec)

#Function to get the values of the element - no functional
def get_address(element):

    element.get_attribute('value')

#Function to login the web application using the encrypted credentials
def login(username,password):

    email_input = driver.find_element_by_name('username')
    pass_input = driver.find_element_by_name('password')

    email_input.send_keys(username)
    pass_input.send_keys(password)

    wait(4)
    login_button = driver.find_element_by_xpath("//form[@class='form-horizontal ng-dirty ng-touched ng-valid']/div[5]/div[1]/button[@type='submit']")
    login_button.click()

#Function to create users
def createUsers(first,last,password,email,address,phone):
    elements = {
                'name':first,
                'surname':last,
                'password': password,
                'email': email,
                'address':address,
                'phone': phone
               }
    
    wait(5)
    user_link = driver.find_element_by_link_text('USERS')
    user_link.click()

    create_button = driver.find_element_by_xpath("//div[@id='DopBlock']/a[1]")
    create_button.click()
    
    wait(5)
    # Following loop is equal to "last_input = driver.find_element_by_name('surname')" && "last_input.send_keys(last)"
    for i in elements:
        driver.find_element_by_name(i).send_keys(elements[i])

    find_input= driver.find_element_by_id('find-tenants')
    find_input.send_keys('Perricone')

    wait(5)
    
    checkbox = driver.find_element_by_xpath("//tbody[@class='ui-datatable-data ui-widget-content']/tr/td[1]/span/div[1]/div[1]/label[2]")

    wait(10)
    checkbox.click()

    wait(10)
    confirm_button = driver.find_element_by_xpath("//div[@class='modal-footer']/button[1]")
    confirm_button.click()
        

# call the Encrypted program to desencrypt data stored    
cryp = EncypData.DataCrypt()
data = cryp.DesEncrypt()
info = json.loads(data)

#call the driver to run the webapp
driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver_win32\chromedriver.exe")

driver.get(info['website'])

login(info['username'],info['password'])
createUsers('Adriano','Torrez','Password1234!','adriano@testing.com','dde ne','0000')


