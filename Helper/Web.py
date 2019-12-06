from selenium import webdriver
from win32.win32process import CREATE_NO_WINDOW

driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver_win32\chromedriver.exe")

driver.get('https://******')


email_input = driver.find_element_by_name('username')
pass_input = driver.find_element_by_name('password')
login_button = driver.find_element_by_xpath("//form[@class='form-horizontal ng-dirty ng-touched ng-valid']/div[5]/div[1]/button[@type='submit']")

email_input.send_keys('@@@@@@')
pass_input.send_keys('******')


login_button.click()
