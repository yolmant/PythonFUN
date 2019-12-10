from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import EncypData
import json

class WebAutomated():

    def __init__(self):

        #call the driver to run the webapp
        self.driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver_win32\chromedriver.exe")

        self.driver.get(info['website'])
        
    #Function to time out the excecution of the driver
    def wait(self,sec):

        self.driver.implicitly_wait(sec)

    #Function to get the values of the element - no functional
    def get_address(self,element):

        element.get_attribute('value')

    #Function to login the web application using the encrypted credentials
    def login(self,username,password):

        email_input = self.driver.find_element_by_name('username')
        pass_input = self.driver.find_element_by_name('password')

        email_input.send_keys(username)
        pass_input.send_keys(password)

        self.wait(4)
        login_button = self.driver.find_element_by_xpath("//form[@class='form-horizontal ng-dirty ng-touched ng-valid']/div[5]/div[1]/button[@type='submit']")
        login_button.click()

    #Function to create users
    def createUsers(self,first,last,password,email,address,phone):
        elements = {
                    'name':first,
                    'surname':last,
                    'password': password,
                    'email': email,
                    'address':address,
                    'phone': phone
                   }
        
        self.wait(5)
        user_link = self.driver.find_element_by_link_text('USERS')
        user_link.click()

        create_button = self.driver.find_element_by_xpath("//div[@id='DopBlock']/a[1]")
        create_button.click()
        
        self.wait(5)
        # Following loop is equal to "last_input = driver.find_element_by_name('surname')" && "last_input.send_keys(last)"
        for i in elements:
            self.driver.find_element_by_name(i).send_keys(elements[i])

        find_input= self.driver.find_element_by_id('find-tenants')
        find_input.send_keys('Perricone')

        self.wait(5)
        
        checkbox = self.driver.find_element_by_xpath("//tbody[@class='ui-datatable-data ui-widget-content']/tr/td[1]/span/div[1]/div[1]/label[2]")

        self.wait(10)
        checkbox.click()

        self.wait(10)
        confirm_button = self.driver.find_element_by_xpath("//div[@class='modal-footer']/button[1]")
        confirm_button.click()

    def get_address(self):

        site_name = self.driver.find_elements_by_tag_name('h4')
        for i in site_name:
            print(i.text)

        site_edit = self.driver.find_element_by_xpath("//div[@class='tenants']/div[1]/div[1]/div[2]/i[1]")
        site_edit.click()

        self.wait(5)

        address_input = self.driver.find_element_by_name('address')
        print(address_input.get_attribute('value'))
        
            
# call the Encrypted program to desencrypt data stored    
cryp = EncypData.DataCrypt()
data = cryp.DesEncrypt()
info = json.loads(data)

web = WebAutomated()

web.login(info['username'],info['password'])
web.get_address()
##web.createUsers('Adriano','Torrez','Password1234!','adriano@testing.com','dde ne','0000')

#web.driver.close()

