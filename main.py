import os
import random
from subprocess import CREATE_NO_WINDOW
import threading
import time
import pandas as pd
import requests
import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from PyQt5.QtCore import QThread, pyqtSignal
from selenium.webdriver.support.select import Select
import json
import io
import base64
from PIL import Image
class Reg(QThread):
    show = pyqtSignal(int, int, str)
    check = pyqtSignal(bool)
    def __init__(self, ref, x, y) -> None:
        super().__init__()
        self.ref = ref
        self.x = x
        self.y = y
        self.userid = []
        self.cookiepd = []
    def getDriver(self):
        try:
            options = webdriver.ChromeOptions()
            # options.headless = True
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            path = os.path.join(os.getcwd(), "webgl")
            # print(path)
            options.add_argument('-load-extension='+path)
            options.add_argument('--lang=vi')
            options.add_argument('--app=https://httpbin.org/ip')
            options.binary_location = self.ref.pathChrome.text()
            options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
            # options.add_argument('-window-size=516,726') 
            options.add_argument('-window-size=360,700') 
            options.add_argument('-window-position=%s,%s'%(self.x, self.y)) 
            s = Service("chromedriver.exe")
            s.creation_flags = CREATE_NO_WINDOW
            self.driver = webdriver.Chrome(service=s, options=options, version_main=self.ref.versionChrome.value(), use_subprocess=True)
        except WebDriverException as e:
            if 'This version of ChromeDriver only supports' in str(e):
                self.show.emit(self.row, 4, 'Vui lòng cài đúng version!')
                return 'version_error'
            self.show.emit(self.row, 4, 'Đang mở lại chrome...')
            try:self.driver.close()
            except: pass
            return self.getDriver()
            
        
    def MoveToElementClick(self, by: By, value: str, text: str=...):
        ac = ActionChains(self.driver)
        
        try:
            el = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((by, value)))
        except:
            self.driver.implicitly_wait(5)
            el = self.driver.find_element(by, value)
        # el.click()
        ac.move_to_element(el).click(el).perform()
        if text != ...: ac.send_keys_to_element(el, text).perform()
    def ClickElement(self, by: By, value: str, click=True):
        ac = ActionChains(self.driver)
        self.driver.implicitly_wait(10)
        el = self.driver.find_element(by, value)
        ac.move_to_element(el).perform()
        time.sleep(1)
        if click: el.click()
    def ClickJs(self, el):
        self.driver.execute_script("arguments[0].click();", el)
    def SetBirthDay(self):
        self.show.emit(self.row, 4, 'Đang nhập ngày sinh...')
        # time.sleep(1)
        self.MoveToElementClick('xpath', '//div[text()="Tháng"]')
        # time.sleep(1)
        month = self.driver.find_elements("xpath", "//div[contains(text(), 'Tháng')]")
        month.pop(0)
        self.ClickJs(random.choice(month))
        # time.sleep(1)
        self.MoveToElementClick('xpath', '//div[text()="Ngày"]')
        # time.sleep(1)
        day = self.driver.find_element("xpath", '//div[text()="%s"]'%str(random.randint(5, 10)))
        self.ClickJs(day)
        # time.sleep(1)
        self.MoveToElementClick('xpath', '//div[text()="Năm"]')
        # time.sleep(1)
        year = self.driver.find_element("xpath", '//div[text()="%s"]'%str(random.randint(2002, 2005)))
        self.ClickJs(year)
        self.MoveToElementClick('xpath', '//button[text()="Tiếp"]')
        # time.sleep(999)
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
    def APIOmo(self, key, url):
        try:
            base64_str = base64.b64encode(requests.get(url).content)
            buffer = io.BytesIO()
            imgdata = base64.b64decode(base64_str)
            img = Image.open(io.BytesIO(imgdata))
            new_img = img.resize((340, 212))  # x, y
            new_img.save(buffer, format="PNG")
            img_b64 = str(base64.b64encode(buffer.getvalue()))[2:-1]
            # open('cc.txt', 'w').write(img_b64)
            data = '''{"api_token": "%s","data": {"type_job_id": "22","image_base64": "%s","width_view": 340,"height_view": 212}}'''%(key, img_b64)
            headers = {
                "Content-Type": "application/json"
            }
            createjob = requests.post('https://omocaptcha.com/api/createJob', data=data, headers=headers).json()
            if not createjob["error"]:
                time.sleep(3)
                while True:
                    result = requests.post("https://omocaptcha.com/api/getJobResult", data='{"api_token": "%s", "job_id": %s}'%(key, createjob["job_id"]), headers=headers).json()
                    print(result)
                    if result["status"] == "success":
                        x1, y1, x2, y2 = result["result"].split("|")
                        return (int(x1),int(y1),int(x2),int(y2))
                    elif result["status"] == "fail":
                        return ()
                    time.sleep(1)
            else:
                return ()
        except: return ()
    def APIOmoXoay(self, key, url1, url2):
        ngoai = str(base64.b64encode(requests.get(url1).content)).replace("b'", '').replace("'", '')
        trong = str(base64.b64encode(requests.get(url2).content)).replace("b'", '').replace("'", '')
        data = '''{"api_token": "%s","data": {"type_job_id": "23","image_base64": "%s|%s"}}'''%(key, trong, ngoai)
        # print(data)
        headers = {
            "Content-Type": "application/json"
        }
        createjob = requests.post('https://omocaptcha.com/api/createJob', data=data, headers=headers).json()
        if not createjob["error"]:
            time.sleep(3)
            while True:
                result = requests.post("https://omocaptcha.com/api/getJobResult", data='{"api_token": "%s", "job_id": %s}'%(key, createjob["job_id"]), headers=headers).json()
                print(result)
                if result["status"] == "success":
                    return result["result"]
                elif result["status"] == "fail":
                    return 0
                time.sleep(1)
        else:
            return 0
    def SolveCaptcha(self):
        while True:
            time.sleep(10)
            if 'Chọn 2 đối tượng có hình dạng giống nhau:' in self.driver.page_source:
                self.show.emit(self.row, 4, 'Đang giải captcha...')
                driver = self.driver
                driver.implicitly_wait(20)
                src = driver.find_element('xpath', '//img')
                src = src.get_attribute('src')
                # print(src)
                api = self.APIOmo(self.ref.keyOmo, src)
                if api == ():
                    self.MoveToElementClick('xpath', '//span[text()="Làm mới"]')
                    return self.SolveCaptcha()
                x1, y1, x2, y2 = api 
                # print(x1,y1,x2,y2)
                driver.implicitly_wait(20) 
                el = driver.find_element('xpath', "//div[contains(@class, 'captcha_verify_img')]")
                w, h = -el.size["width"], el.size["height"]
                ac = ActionChains(driver)
                ac.move_to_element_with_offset(el, w/2, h/2).move_by_offset(x1, -h+y1).click().perform()
                ac.move_to_element_with_offset(el, w/2, h/2).move_by_offset(x2, -h+y2).click().perform()
                self.MoveToElementClick('xpath', '//div[text()="Xác nhận"]')
                self.CheckCaptcha()
                return
            elif 'Kéo thanh trượt để ghép hình' in self.driver.page_source:
                self.show.emit(self.row, 4, 'Đang giải captcha...')
                driver = self.driver
                src = driver.find_elements('xpath', '//img')
                ngoai = src[0].get_attribute('src')
                trong = src[1].get_attribute('src')
                xcapt = int(self.APIOmoXoay(self.ref.keyOmo, ngoai, trong))
                if xcapt == 0:
                    self.MoveToElementClick('xpath', '//span[text()="Làm mới"]')
                    return self.SolveCaptcha()
                ac = ActionChains(driver)
                el = driver.find_element('xpath', '//*[@id="captcha_container"]/div/div[3]/div[2]/div[2]')
                ac.move_to_element(to_element=el)
                ac.click_and_hold(on_element=el)
                for i in range(5):
                    ac.move_by_offset(round(float(xcapt/5)), 0)
                    ac.pause(0.3)
                ac.release()
                ac.perform()
                self.CheckCaptcha()
                return
            elif 'Xác minh để tiếp tục' in self.driver.page_source:
                return
            elif 'Ngày sinh của bạn sẽ không được hiển thị công khai.' in self.driver.page_source:
                return
            elif 'Bỏ qua' in self.driver.page_source:
                return
            # time.sleep(1)
    def ConvertCookieJ2Team(self, cookietiktok: list):
        dm = '{"url":"https://www.tiktok.com","cookies":[{"domain":".tiktok.com","expirationDate":1710170623.193059,"hostOnly":false,"httpOnly":false,"name":"_ttp","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"2LBlgV8K5FSfN7cKBGs2wpsxm3C"},{"domain":"www.tiktok.com","expirationDate":1707585694.968242,"hostOnly":true,"httpOnly":true,"name":"ttwid","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"1%7CarBCrmd9ppNI68pOGD3o0qzW9KGPzIxFao9k4y0VykA%7C1676049690%7C01e9cdbc94d306782c6cf60c4be3938513898e36b858c49e2f76be40eff0e407"},{"domain":".www.tiktok.com","expirationDate":1702567076,"hostOnly":false,"httpOnly":false,"name":"tiktok_webapp_theme","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"light"},{"domain":".tiktok.com","expirationDate":1681233703.89739,"hostOnly":false,"httpOnly":false,"name":"passport_csrf_token","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"7bbe64c343db91f85b9b0225be3dee24"},{"domain":".tiktok.com","expirationDate":1681233703.897422,"hostOnly":false,"httpOnly":false,"name":"passport_csrf_token_default","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"7bbe64c343db91f85b9b0225be3dee24"},{"domain":".tiktok.com","expirationDate":1678812190.711985,"hostOnly":false,"httpOnly":true,"name":"passport_auth_status","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"97c0a98a240cf26bd570f92e224b4292%2C"},{"domain":".tiktok.com","expirationDate":1678812190.711997,"hostOnly":false,"httpOnly":true,"name":"passport_auth_status_ss","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"97c0a98a240cf26bd570f92e224b4292%2C"},{"domain":".www.tiktok.com","expirationDate":1677251876,"hostOnly":false,"httpOnly":false,"name":"__tea_cache_tokens_1988","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"{%22_type_%22:%22default%22%2C%22user_unique_id%22:%227198578561794491947%22%2C%22timestamp%22:1676531181818}"},{"domain":".tiktok.com","expirationDate":1676668675.878273,"hostOnly":false,"httpOnly":true,"name":"tt_chain_token","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"XuLIUuI5dWJb8ZY5KvdkKA=="},{"domain":".tiktok.com","hostOnly":false,"httpOnly":true,"name":"tt_csrf_token","path":"/","sameSite":"lax","secure":true,"session":true,"storeId":"0","value":"Qml3zgYh-tEZE0sMkwoMgj-Gh-6GavHVdJJ0"},{"domain":".tiktok.com","expirationDate":1708183011.903075,"hostOnly":false,"httpOnly":false,"name":"_abck","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"A71FB20D73F2955FA09C1473F0C6FEBB~0~YAAQUhBFdj4qZjiGAQAAkA7zXwkLUkFg696VRoa6lncyOQXQA0Sr0bzhUnE5ZDUgJhEcXXfRDL4WBftHVNNtGvb8JlXCKiu4bkWR1fZunB0rj9kHl0u1+89FUQu9oJQcQxm5h5Kb1mSAzqkdMHM4NGiLDsB65jW7M1HDWvKbRh8ZuF1XExTcVAyOnZpl9un5YXxCnhojGA2HaU4mT41iJR2OCVK8mISTGS3ZButJdHURdzUzVBVoWlsMhyjRg3LNZEBHoGQKVvlG8GBuGrKZ3+c9oT6ADBAZTc3vNQRN0J3pJo6BL0Dyo9DYspdWokG6ohaT24PUQu/lqE/B+skelEU5/lcfBXX1yFZiFpndTiDnwl5bVV0Srx/HNkSQeXhJCPvEdW0tOFlhl7xRnAvblDjcYFOJfjTQ~-1~-1~-1"},{"domain":".tiktok.com","expirationDate":1676661411.90311,"hostOnly":false,"httpOnly":false,"name":"bm_sz","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"057C65E30B768E15E12D3FB43F965842~YAAQUhBFdkEqZjiGAQAAkA7zXxL1RVxIzltmpf/4NNzhmdbjRqyxgkacQxx9qTnKeMGmtpTBoO7TP0vOBZEm2UhKuKHcPI4X/edPUqt98PpBTLxS0ncY+pkVDocRe4ffVlWYIXkr2sbHBafiGxM/y9QS9BRMJfarAl23oZc3UgNfcTn1JUb2qlFwwx/dEwLMrcmZ/sE4RaC61985btOirV0ffDOaWGWODhawCP+TrkZg3U94arnqWtiiLiHr56n77fmhmpneDqOqV5Ft8yNZXBEzZiUw7hhbfTGfNzZQ75MBN/U=~3617840~4535107"},{"domain":".tiktok.com","expirationDate":1676654211.641581,"hostOnly":false,"httpOnly":true,"name":"ak_bmsc","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"56A8E3A4E891540EEF2E654D3D4FAA73~000000000000000000000000000000~YAAQUhBFdk0qZjiGAQAAWxXzXxI8/aZg/2QuEB1gl5MBXACADmYnDPIW6n6cQCIAwCBcWQXAzX4ZcdkhiFEkiUYQ6kkTTQknTSG0+yKBTyH0zLELjUSVc460RVs5pRV6JxBJbNp2r52xT56wK2P5lSpsgugLJNRBTUT/TOXcTW5sjNLAi6g0FcvpCkD5ZhQNZn5xcpN2DEEku16f92q/r+oY/22WzTNoX+bmxqsbaJkBx0Vg2ZETDAuv0BNRMqMmyNauykI7ZF0OvvFk9mWP5Hi2ECunOA+cR1JTkhBoTTPJ1U1eFBCZAfF5mi8R4yVzg2jwQPp71gk0ITdKGmrS8fqPSpdN3Ro0rm/17HqKlkUW+/NnF066TmgSPJakDZx4+GOqogWA/8Yz6pS0n5tztHifeXjQrExlvgNS3ku2Bq1mP26JUxVZSjGBuV6dfWs6fapSJpX41cXBkL168nEyapSe+96+0SuzRdFaR52SGG4a2yfh84ChCd8NQw=="},{"domain":".tiktok.com","hostOnly":false,"httpOnly":false,"name":"s_v_web_id","path":"/","sameSite":"no_restriction","secure":true,"session":true,"storeId":"0","value":"verify_le8oddkq_xFWp20RM_ZdpO_48wR_BKkO_ParJG6R0AAKq"},{"domain":".tiktok.com","expirationDate":1681831073.704403,"hostOnly":false,"httpOnly":true,"name":"cmpl_token","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"AgQQAPOFF-RO0rLVHnuj-d0i-YfkDvRa_4MOYMn8QQ"},{"domain":".tiktok.com","expirationDate":1707751073.704432,"hostOnly":false,"httpOnly":true,"name":"sid_guard","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"29aa9c7bb66a7c8a20d4a96c34ef662e%7C1676647071%7C5184000%7CTue%2C+18-Apr-2023+15%3A17%3A51+GMT"},{"domain":".tiktok.com","expirationDate":1681831073.704443,"hostOnly":false,"httpOnly":true,"name":"uid_tt","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"fa4ca849af69fae2f6c269d908c2724714fd89fe93421bbdb5fdd295637d48d4"},{"domain":".tiktok.com","expirationDate":1681831073.704454,"hostOnly":false,"httpOnly":true,"name":"uid_tt_ss","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"fa4ca849af69fae2f6c269d908c2724714fd89fe93421bbdb5fdd295637d48d4"},{"domain":".tiktok.com","expirationDate":1681831073.704464,"hostOnly":false,"httpOnly":true,"name":"sid_tt","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"29aa9c7bb66a7c8a20d4a96c34ef662e"},{"domain":".tiktok.com","expirationDate":1681831073.704473,"hostOnly":false,"httpOnly":true,"name":"sessionid","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"29aa9c7bb66a7c8a20d4a96c34ef662e"},{"domain":".tiktok.com","expirationDate":1681831073.704483,"hostOnly":false,"httpOnly":true,"name":"sessionid_ss","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"29aa9c7bb66a7c8a20d4a96c34ef662e"},{"domain":".tiktok.com","expirationDate":1681831073.704495,"hostOnly":false,"httpOnly":true,"name":"sid_ucp_v1","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"1.0.0-KDkwZDgxYmU3NjBhZDc3ZTZlOTVjN2QzNmM3ZmFlZDBiZWY3ZTlhYTAKIAibiKzewpv89WIQn7W-nwYYswsgDDDl4q-XBjgEQOoHEAMaBm1hbGl2YSIgMjlhYTljN2JiNjZhN2M4YTIwZDRhOTZjMzRlZjY2MmU"},{"domain":".tiktok.com","expirationDate":1681831073.704505,"hostOnly":false,"httpOnly":true,"name":"ssid_ucp_v1","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"1.0.0-KDkwZDgxYmU3NjBhZDc3ZTZlOTVjN2QzNmM3ZmFlZDBiZWY3ZTlhYTAKIAibiKzewpv89WIQn7W-nwYYswsgDDDl4q-XBjgEQOoHEAMaBm1hbGl2YSIgMjlhYTljN2JiNjZhN2M4YTIwZDRhOTZjMzRlZjY2MmU"},{"domain":".tiktok.com","expirationDate":1681831073.983148,"hostOnly":false,"httpOnly":true,"name":"store-idc","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"useast2a"},{"domain":".tiktok.com","expirationDate":1681831073.983181,"hostOnly":false,"httpOnly":true,"name":"store-country-code","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"vn"},{"domain":".tiktok.com","expirationDate":1681831073.9832,"hostOnly":false,"httpOnly":true,"name":"store-country-code-src","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"uid"},{"domain":".tiktok.com","expirationDate":1681831073.983216,"hostOnly":false,"httpOnly":true,"name":"tt-target-idc","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"alisg"},{"domain":".tiktok.com","expirationDate":1708183074.142736,"hostOnly":false,"httpOnly":true,"name":"tt-target-idc-sign","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"iRm3zvttyfrbFxAA-U31OGuartgNEyud2bOapLsGrN4EOsPYm1JEdTLsuStMYL43NpGa9Y2ePACyexVQxdzXKd2KNWA762cFH8vVUHegGvfEi0bKLyh_95etTeIwZuClgS_CzO6KRGpmBGXrNdJrdPx4hKk5U776DS8GcAQb12hxUPj1ZuZQWUc5u9AQmj-Ve3IWAuZUiazeIpUdPBlNQihdisE1X6rlpAUcOinjwpG-5P7rlqcQqtddIuEZFNQ8yrwsXi0zdMPhIEJBtM5CJ_AaqWahmf7PDVYTpOrdJuI3_X6gBDI6CeK0WoaOZF7R-9zVUsG4xOKZ0SvEMKMRVAWf3dgtuRxDEenK9X8M5DUve-atuhP3hymqy6W88BGKwFPfKADCaLMUKEFSkG1WV5Ey8T2fnLKZOKF7bw7MphT9NODtIEGaDTBTyMVJle09kVfJ7MFEPOfD9Dew9jJgXxuIUX3OhD41-sFStTiDWrMqMv52PKSHywTA8dwivk2H"},{"domain":".www.tiktok.com","hostOnly":false,"httpOnly":false,"name":"passport_fe_beating_status","path":"/","sameSite":"unspecified","secure":false,"session":true,"storeId":"0","value":"true"},{"domain":".tiktok.com","expirationDate":1708183078.629616,"hostOnly":false,"httpOnly":true,"name":"ttwid","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"1%7Cw6soajNXYudsZ_F5su59vPy3jjjXbVSUf2rf6ASr-Oc%7C1676647076%7C41bc704aea99f95c155d89207050ae5d2e598008ee084d9d1512a3933b9f7964"},{"domain":".tiktok.com","expirationDate":1708183079.407064,"hostOnly":false,"httpOnly":true,"name":"odin_tt","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"2aaebdc5ecf0fccdff6b293c176e63ac11b881db017d5e5460a9b2e67193206f0da5b41d871483644216727f1c33a81ad52a75709a6c7e698085ae4462e1e08b4d6c6b316dd3caf6bca71eb3b2fe3ee6"},{"domain":".tiktok.com","expirationDate":1676654215.409467,"hostOnly":false,"httpOnly":false,"name":"bm_sv","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"76B00AEB44BD7C57990CAEE3069456A7~YAAQIhFFdgHk5CWGAQAAJBr0XxKlBCAuDubsc5k/7pxamD+oZZ6hI0J1ydMwxjpyJhSdZOc2uoy5TDfoF6/Pg1cAr6YGuvN5leeHSyF1RUHGfCVP1ssik3y+wCGhQqn/mdFmWXaKehrkqNJuCQQgEx1b4qrYuJbSJzhPaL/TgEASZUl0k6HhYYWZ/LCsG6E8ChzBn9AVOJldvEvPYaTKwmlaRaTP/cgiA77LTRgDzzlyt3v8S+8iNEIf4cPfZf4c~1"},{"domain":".tiktok.com","expirationDate":1677511081.85999,"hostOnly":false,"httpOnly":false,"name":"msToken","path":"/","sameSite":"no_restriction","secure":true,"session":false,"storeId":"0","value":"MqDUaPmu29XKrRRLWl6vTCDAmc074DGRDvC_nCC6oD03K5HMHDyg203pYNGZojwZJoNFjTtoVkeFhDjDnjH21fb20lk8Jr11MpgonB5yXP50Qr6D5ocbUTviQrgzuu70Q4fbdaPmWcw0gEys9g=="},{"domain":"www.tiktok.com","expirationDate":1684423081,"hostOnly":true,"httpOnly":false,"name":"msToken","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"MqDUaPmu29XKrRRLWl6vTCDAmc074DGRDvC_nCC6oD03K5HMHDyg203pYNGZojwZJoNFjTtoVkeFhDjDnjH21fb20lk8Jr11MpgonB5yXP50Qr6D5ocbUTviQrgzuu70Q4fbdaPmWcw0gEys9g=="}]}'
        file =  json.loads(dm)["cookies"]
        cookie = {"url":"https://www.tiktok.com","cookies": ""}
        cc = []
        for i in file:
            for ii in cookietiktok:
                if i["name"] == ii["name"]:
                    if 'expiry' in ii:
                        i.update({'expirationDate': ii['expiry']})
                    i.update({"value": ii["value"]})
            cc.append(i)
        cookie.update({"cookies": cc})
        return str(cookie).replace("'", '"').replace(' ', '').replace('True', 'true').replace('False', 'false')
    def FindUsername(self):
        driver = self.driver
        username = driver.page_source.split('"uniqueId":"')
        username.pop(0)
        for i in range(3):
            u = username[i]
            driver.get('https://www.tiktok.com/@'+u.split('"')[0])
            time.sleep(1)
            if '</svg><span>Sửa hồ sơ</span></button>' in driver.page_source:
                return u.split('"')[0]
            
    def GetCookie(self):
        driver = self.driver
        self.cookieweb = ""
        username = self.FindUsername()
        web = driver.get_cookies()
        for ck in web:
            self.cookieweb += "%s=%s;"%(ck["name"], ck["value"])
        self.cookiej2team = self.ConvertCookieJ2Team(web)
        self.show.emit(self.row, 2, username)
        self.show.emit(self.row, 3, self.cookieweb)
        if not os.path.exists('cookiej2team'): os.mkdir("cookiej2team")
        if not os.path.exists('cookieweb'): os.mkdir("cookieweb")
        with open("cookiej2team\\%s.json"%username, 'a+') as file:
            file.write(self.cookiej2team+"\n")
        with open("cookieweb\\cookieweb.txt", 'a+') as file:
            file.write(self.cookieweb+"\n")
        if os.path.exists("cookieweb\\cookiejs2team.xlsx"):
            writer = pd.read_excel("cookieweb\\cookiejs2team.xlsx") 
            user_id = [i[0] for i in writer.values]
            cookie = [i[1] for i in writer.values]
        else:
            user_id = []
            cookie = []
        user_id.append(username)
        cookie.append(self.cookiej2team)
        columns=['user_id','Cookie']
        df = pd.DataFrame(list(zip(user_id,cookie)), columns=columns)
        with pd.ExcelWriter("cookieweb\\cookiejs2team.xlsx", engine='xlsxwriter', engine_kwargs={'options':{'strings_to_urls': False}}) as writer:
                    df.to_excel(writer, sheet_name='cookie', index=False)
    def UpAvatar(self):
        self.show.emit(self.row, 4, 'Thành công đang chuẩn bị vào profile...')

        driver = self.driver
        time.sleep(4)
        driver.implicitly_wait(10)

        next = driver.find_element('xpath', '//div[text()="Bỏ qua"]')
        self.ClickJs(next)
        # self.MoveToElementClick('xpath', '//div[text()="Bỏ qua"]')
        # self.ClickElement('xpath', '//*[@data-e2e="profile-icon"]')

        time.sleep(3)
        self.GetCookie()
        # self.ClickElement('xpath', '//*[text()="Xem hồ sơ"]')
        self.show.emit(self.row, 4, 'Đang cập nhật ảnh đại diện...')
        # time.sleep(2)
        self.MoveToElementClick('xpath', '//*[text()="Sửa hồ sơ"]')
        driver.implicitly_wait(10)
        file = random.choice(os.listdir(self.ref.pathFolder))
        img = os.path.join(self.ref.pathFolder, file)
        driver.find_element('xpath', "//input[contains(@class, 'InputUpload')]").send_keys(img)
        # sign = driver.find_element('xpath', '//*[text()="Đăng ký"]')
        # self.ClickJs(sign)
        time.sleep(2)
        self.ClickElement('xpath', '//*[text()="Đăng ký"]')
        time.sleep(2)

        self.ClickElement('xpath', '//*[text()="Lưu"]', click=False)
        # time.sleep(99)
        
        save = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(('xpath', '//*[text()="Lưu"]')))
        self.ClickJs(save)
        time.sleep(10)
    def CheckCaptcha(self):
        while True:
            if "Đã hoàn tất xác minh" in self.driver.page_source:
                return
            elif 'Không thể xác minh' in self.driver.page_source:
                self.MoveToElementClick('xpath', '//span[text()="Làm mới"]')
                return self.SolveCaptcha()
            time.sleep(1)
    def reg(self, gmail: str, pwd: str):
        driver = self.getDriver()
        if driver == "version_error": 
            return 'stopall'
        driver = self.driver
        
        driver.get("https://www.tiktok.com/signup")
        main = driver.window_handles[0]
        if 'Chấp nhận cookie từ TikTok trên trình duyệt này?' in driver.page_source:
            try:
                driver.execute_script('document.querySelector("body > tiktok-cookie-banner").shadowRoot.querySelector("div > div.button-wrapper > button:nth-child(2)").click()')
            except WebDriverException:
                pass
        driver.implicitly_wait(20)
        Select(driver.find_element('xpath', "//select[contains(@class, 'SelectFormContainer')]")).select_by_value('vi-VN')
        # self.MoveToElementClick('xpath', '//button[text()="Đăng nhập"]')
        self.show.emit(self.row, 4, 'Đang đăng nhập google...')
        self.MoveToElementClick('xpath', '//p[text()="Tiếp tục với Google"]')
        self.CheckWindowLogin()
        self.MoveToElementClick('xpath', '//input[@aria-label="Email hoặc số điện thoại"]', gmail)  
        self.MoveToElementClick('xpath', '//div[@id="identifierNext"]')
        self.MoveToElementClick('xpath', '//input[@aria-label="Nhập mật khẩu của bạn"]', pwd)
        self.MoveToElementClick('xpath', '//div[@id="passwordNext"]')
        try:
            self.MoveToElementClick('xpath', '//*[@id="confirm"]')
        except: pass
        driver.switch_to.window(main)

        self.SolveCaptcha()
        if 'data-e2e="profile-icon"' in driver.page_source:
            self.show.emit(self.row, 4, "Đã tạo rồi!")
            self.GetCookie()
            return
        self.SetBirthDay()
        
        self.SolveCaptcha()
        self.UpAvatar()
        self.show.emit(self.row, 4, "Thành công!")
    def Stop(self):
        self.show.emit(self.row, 4, "Đã dừng tạo!")

        try: threading.Thread(target=self.driver.quit).start()
        except: pass
        self.terminate()
    def CheckBalance(self):
        while True:
            try:
                self.show.emit(self.row, 4, "Đang check tiền captcha...")
                balance = requests.post('https://omocaptcha.com/api/getBalance', data='{"api_token": "%s"}'%self.ref.keyOmo, headers={"Content-Type": "application/json"}).json()["balance"]
                print(balance)
                if float(balance) < 0.00060:
                    self.show.emit(self.row, 4, "Hết tiền captcha !")
                    return False
                else: return True
            except: continue
    def run(self):
        while True:
            try: 
                gmail, pwd = str(next(self.ref.iterGmail)).split("|")
            except: return
            
            self.row = self.ref.tableWidget.rowCount()
            self.ref.tableWidget.insertRow(self.row)
            if not self.CheckBalance(): return
            try:
                self.show.emit(self.row, 0, gmail)
                self.show.emit(self.row, 1, pwd)
                self.show.emit(self.row, 4, "Đang bắt đầu reg...")
                check = self.reg(gmail, pwd)
                if check == "stopall":
                    return
                self.check.emit(True)
                self.driver.close()
                time.sleep(1)
            except Exception as e:
                try: self.driver.close()
                except: pass
                self.check.emit(False)
                self.show.emit(self.row, 4, str(e))
                try:
                    with open('gmailfail.txt', 'a+', encoding="utf-8") as file:
                        file.write("%s|%s\n"%(gmail, pwd))
                except: pass


    
