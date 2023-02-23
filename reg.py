import random
from subprocess import CREATE_NO_WINDOW
import time
import requests
import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import 
import io
import base64
from PIL import Image
class Reg:
    def __init__(self) -> None:
        pass
    def getDriver(self):
        global driver
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.images": 2,
            # "profile.default_content_setting_values.cookies": 2,
        },)
        # options.add_experimental_option(
        #     "prefs",
        #     {
        #         "profile.default_content_setting_values.cookies": 2,
        #     },
        # )
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument('--lang=vi')
        # options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
		# options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('-window-size=516,726') 
        s = Service("chromedriver.exe")
        s.creation_flags = CREATE_NO_WINDOW
        self.driver = webdriver.Chrome(service=s, options=options, use_subprocess=True, executable_path_mkdtemp=True)
        # self.driver.delete_executable_path_mkdtemp()
        driver = self.driver
        
    def MoveToElementClick(self, by: By, value: str, text: str=...):
        ac = ActionChains(self.driver)
        self.driver.implicitly_wait(20)
        el = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((by, value)))
        # el = self.driver.find_element(by, value)
        # el.click()
        ac.move_to_element(el).click(el).perform()
        if text != ...: ac.send_keys_to_element(el, text).perform()
    def ScrollElementClick(self, el):
        ac = ActionChains(self.driver)
        self.driver.implicitly_wait(20)
        ac.move_to_element(el).click(el).perform()
    def SetBirthDay(self):
        self.MoveToElementClick('xpath', '//div[text()="Tháng"]')
        month = self.driver.find_elements("xpath", "//div[contains(text(), 'Tháng')]")
        day = self.driver.find_element("xpath", '//div[text()="%s"]'%str(random.randint(1,31)))
        year = self.driver.find_element("xpath", '//div[text()="%s"]'%str(random.randint(1970,1999)))
        month.pop(0)
        self.ScrollElementClick(random.choice(month))
        self.MoveToElementClick('xpath', '//div[text()="Ngày"]')
        self.ScrollElementClick(day)
        self.MoveToElementClick('xpath', '//div[text()="Năm"]')
        self.ScrollElementClick(year)
        self.MoveToElementClick('xpath', '//button[text()="Tiếp"]')
    def CheckWindowLogin(self):
        while True:
            for win in self.driver.window_handles:
                self.driver.switch_to.window(win)
                if 'identifier' in self.driver.current_url:
                    return 
                else: 
                    time.sleep(1)
                    continue
            time.sleep(1)
        
    def run(self):
        self.getDriver()
        driver = self.driver
        
        driver.get("https://www.tiktok.com/signup")
        main = driver.window_handles[0]
        # self.MoveToElementClick('xpath', '//button[text()="Đăng nhập"]')
        self.MoveToElementClick('xpath', '//p[text()="Tiếp tục với Google"]')
        self.CheckWindowLogin()
        self.MoveToElementClick('xpath', '//input[@aria-label="Email hoặc số điện thoại"]', "ElijahClarke52@c3nd.edu.vn")
        self.MoveToElementClick('xpath', '//div[@id="identifierNext"]')
        self.MoveToElementClick('xpath', '//input[@aria-label="Nhập mật khẩu của bạn"]', "Mailthue111a")
        self.MoveToElementClick('xpath', '//div[@id="passwordNext"]')
        self.MoveToElementClick('xpath', '//div[@id="confirm"]')
        driver.switch_to.window(main)
        self.SetBirthDay()

        pass
if __name__ == "__main__":
    test = Reg()
    test.run()
