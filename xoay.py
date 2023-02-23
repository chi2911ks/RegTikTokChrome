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
def getDriver():
    options = webdriver.ChromeOptions()
    # options.add_experimental_option(
    # "prefs",
    # {
    #     "profile.default_content_setting_values.images": 2,
    #     # "profile.default_content_setting_values.cookies": 2,
    # },)
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
    driver = webdriver.Chrome(service=s, options=options, use_subprocess=True, executable_path_mkdtemp=True)
    return driver
def APIOmo(key, url1, url2):
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
def Xoay():
    driver = getDriver()
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    driver.implicitly_wait(10)
    driver.execute_script('''if (document.getElementsByTagName('selenium-mouse-pointer').length == 0) {
    const box = document.createElement('selenium-mouse-pointer');
    const styleElement = document.createElement('style');
    styleElement.innerHTML = `
    selenium-mouse-pointer {
        position: fixed;
        background-size: 20px;
        height: 31px;
        width: 20px;
        z-index: 100003;
        transform: translate(4px, 4px);
        top: 0;
        left: 0;
        background-image: url("https://shopmrbeast.com/_next/static/media/default.97d98757.svg");
    }
    selenium-selenium-mouse-pointer.button-1 {
        transition: none;
        background: rgba(0,0,0,0.9);
    }
    selenium-selenium-mouse-pointer.button-2 {
        transition: none;
        border-color: rgba(0,0,255,0.9);
    }
    selenium-selenium-mouse-pointer.button-3 {
        transition: none;
        border-radius: 4px;
    }
    selenium-selenium-mouse-pointer.button-4 {
        transition: none;
        border-color: rgba(255,0,0,0.9);
    }
    selenium-selenium-mouse-pointer.button-5 {
        transition: none;
        border-color: rgba(0,255,0,0.9);
    }
    `;
    document.head.appendChild(styleElement);
    document.body.appendChild(box);

    addEventListener('mousemove', event => {
        box.style.left = event.pageX - document.scrollingElement.scrollLeft + 'px';
        box.style.top = event.pageY - document.scrollingElement.scrollTop + 'px';
        updateButtons(event.buttons);
    }, true);

    addEventListener('mousedown', event => {
        updateButtons(event.buttons);
        box.classList.add('button-' + event.which);
    }, true);

    addEventListener('mouseup', event => {
        updateButtons(event.buttons);
        box.classList.remove('button-' + event.which);
    }, true);

    function updateButtons(buttons) {
        for (let i = 0; i < 5; i++)
            box.classList.toggle('button-' + i, buttons & (1 << i));
    }
}''')
    driver.find_element('name', 'username').send_keys("chi2911ks53")
    driver.find_element('xpath', '//*[@id="loginContainer"]/div[1]/form/div[2]/div/input').send_keys("Chi@29112004")
    driver.find_element('xpath', '//*[@id="loginContainer"]/div[1]/form/button').click()
    while True:
        if 'Kéo thanh trượt để ghép hình' in driver.page_source:
            time.sleep(5)
            src = driver.find_elements('xpath', '//img')
            trong = src[0].get_attribute('src')
            ngoai = src[1].get_attribute('src')
            xcapt = int(APIOmo("JGWKqGzssbNZEyxCF9NVywp8UzCVVwwNvGZA13IcK39kY0084yfJSpxZlDxzufSVVBmxdgqh6Qp77TZ3", ngoai, trong))
            # print(deg)
            # deg = 30
            ac = ActionChains(driver)
            el = driver.find_element('xpath', '//*[@id="captcha_container"]/div/div[3]/div[2]/div[2]')

            ac.move_to_element(to_element=el)
            
            ac.click_and_hold(on_element=el)
            # ac.move_to_element_with_offset(to_element=el,xoffset= deg,yoffset= 0)
            # ac.release()
            # ac.perform()
            # return
            for i in range(5):
                ac.move_by_offset(round(float(xcapt/5)), 0)
                ac.pause(0.3)
            ac.release()
            ac.perform()
            break
    pass
Xoay()