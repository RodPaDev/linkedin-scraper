from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
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


#==================================================================================#

class LinkedinScraper():
    def __init__(self):
        options = Options()
        options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

        self.config = None
        self.chapters = []
        self.exercise_files_src = []
        self.links_count = 0

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
        chapters = self.driver.find_elements_by_class_name("classroom-toc-chapter")
        for idx, chap in enumerate(chapters, 1):
            if chap.find_element_by_css_selector("button").get_attribute("aria-expanded") == "false":
                chap.find_element_by_css_selector("button").click()
            self.links_count = self.links_count + len(chap.find_elements_by_css_selector("a"))
            chapter = {
                'id': idx,
                'title': chap.find_element_by_css_selector("h3").get_attribute('innerText').lstrip('0123456789.- '),
                'links': [a.get_attribute('href') for a in chap.find_elements_by_css_selector("a")],
                'src': []
            }
            self.chapters.append(chapter)
        print("INFO: Contents scraped")

    def videoSource(self):
        current_link_count = 0
        for chapter in self.chapters:
          for link in chapter["links"]:
            current_link_count +=1
            self.driver.get(link)
            if "quiz" in self.driver.current_url:
              print("INFO: Quiz detected, will be skipped")
              continue
            elif self.driver.title == "www.linkedin.com":
              print(f"[{current_link_count}/{self.links_count}] - INFO: Bot detection triggered, let's wait 5 seconds")
              i = 5
              while self.driver.title == "www.linkedin.com":
                while i != 0:
                  print('.', end='', flush=True)
                  sleep(1)
                  i -= 1
                self.driver.refresh()
            else:
              print(f"[{current_link_count}/{self.links_count}]")
              sleep(randint(2,3))
              chapter["src"].append(self.driver.find_element_by_css_selector("video").get_attribute("src"))

    def oopsHander(self):
      pass

    def exercise_files(self):
        self.driver.find_element_by_css_selector(
            '[data-control-name="exercise_files_modal"]').click()
        files = self.driver.find_elements_by_css_selector('.classroom-exercise-files-modal__exercise-file-download')
        for exFile in files:
            self.exercise_files_src.append(exFile.get_attribute("href"))

    def dump(self):
        print([c for c in self.chapters])


def prod(clear_cache = False):
  try:
      config = ConfigJson()
      config.loadConfig()
      bot = LinkedinScraper()
      if clear_cache:
        bot.clearCache()
      bot.login(config.email, config.password)
      bot.get("https://www.linkedin.com/learning/programming-foundations-algorithms/")
      bot.scrape()
      bot.videoSource()
      bot.exercise_files()
  except Exception as error:
      print(error)
  finally:
      with open("courseData.json", "w", encoding="utf-8") as file:
          dump =  {
            'exercise_files': bot.exercise_files_src,
            'chapters': bot.chapters
          }
          json.dump(dump, file, ensure_ascii=False, indent=4)


config = ConfigJson()
config.loadConfig()
bot = LinkedinScraper()
bot.login(config.email, config.password)
bot.get("https://www.linkedin.com/learning/programming-foundations-algorithms/")
bot.scrape()
bot.videoSource()
bot.exercise_files()
with open("courseData.json", "w", encoding="utf-8") as file:
    dump =  {
      'exercise_files': bot.exercise_files_src,
      'chapters': bot.chapters
    }
    json.dump(dump, file, ensure_ascii=False, indent=4)
