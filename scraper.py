from selenium import webdriver
from time import sleep

class LinkedinScraper():
  def __init__(self):
    self.driver = webdriver.Chrome()

  def login(self, email, password):
    self.driver.get("https://www.linkedin.com/learning-login/")
    sleep(5)
    email_input = self.driver.find_element_by_xpath('//*[@id="auth-id-input"]')
    email_input.send_keys(email)
    email_continue_btn = self.driver.find_element_by_xpath('//*[@id="auth-id-button"]')
    email_continue_btn.click()
    password_input = self.driver.find_element_by_xpath('//*[@id="password"]')
    password_input.send_keys(password)
    password_continue_btn = self.driver.find_element_by_xpath('//*[@id="fastrack-div"]/form/div[2]/button')
    password_continue_btn.click()

