from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json
import JS_scripts

class ConfigJson():
    def __init__(self):
        self.email = None
        self.password = None
        self.links = []
        self.learning_path = []

    def loadConfig(self):
        with open("config.json") as file:
            jsonConfig = json.loads(file.read())
            self.email = jsonConfig['credentials']['email'].strip()
            self.password = jsonConfig['credentials']['password'].strip()

    def dump(self):
        print("Credentials")
        print("Email: ", self.email)
        print("Password: ", self.password)

class LinkedinScraper():
    def __init__(self):
        options = Options()
        options.add_argument("--log-level=3")
        self.config = None
        self.chapters = []
        self.driver = webdriver.Chrome(options=options)

    def get(self, url):
        self.driver.get(url)
        sleep(5)
  
    def clearCache(self):
        self.get('chrome://settings/clearBrowserData')
        self.driver.execute_script(JS_scripts.clear_cache_button)
        print("\nCleaning cache before scraping.", end='', flush=True)
        while self.driver.current_url != "chrome://settings/":
            sleep(0.2)
            print('.', end='', flush=True)
        print("\nCache clean")

    def login(self, email, password):
        print("INFO: Logging in")
        self.driver.get("https://www.linkedin.com/learning-login/")
        sleep(5)
        email_input = self.driver.find_element_by_xpath('//*[@id="auth-id-input"]')
        email_input.send_keys(email)
        email_continue_btn = self.driver.find_element_by_xpath('//*[@id="auth-id-button"]')
        email_continue_btn.click()
        sleep(5)
        password_input = self.driver.find_element_by_xpath('//*[@id="password"]')
        password_input.send_keys(password)
        password_continue_btn = self.driver.find_element_by_xpath('//*[@id="fastrack-div"]/form/div[2]/button')
        password_continue_btn.click()


    def scrape(self):
        try:
          print("INFO: Trying to expand contents tab")
          content_btn = bot.driver.find_element_by_class_name('classroom-nav__sidebar-toggle')
          content_btn.click()
        except:
          print("INFO: Contents tab already expanded")
        chapters = bot.driver.find_elements_by_css_selector('[data-control-name="chapter_contents_toggle"]')
        chaptersText = bot.driver.find_elements_by_css_selector('[data-control-name="chapter_contents_toggle"] h3')
        [c.click() for c in chapters]
        for idx, text in enumerate(chaptersText, 1):
            self.chapters.append(
                f"{idx}. {text.get_attribute('innerText').lstrip('0123456789.- ')}")

    def dump(self):
        print([c for c in self.chapters])


try:
  config = ConfigJson()
  config.loadConfig()
  bot = LinkedinScraper()
  bot.clearCache()
  bot.login(config.email, config.password)
  bot.get("https://www.linkedin.com/learning/programming-foundations-algorithms/")
  bot.scrape()
  bot.dump()
except Exception as err:
  print("An exception has occured: ")
  print(err)

