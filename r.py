# import io
import base64
from time import sleep
# from PIL import Image

# base64_str = ''

# buffer = io.BytesIO()
# imgdata = base64.b64decode(base64_str)
# img = Image.open(io.BytesIO(imgdata))
# new_img = img.resize((340, 212))  # x, y
# new_img.save(buffer, format="PNG")
# img_b64 = str(base64.b64encode(buffer.getvalue()))[2:-1]
# print(img_b64)
# import requests

# cc = requests.get("https://lf19-captcha-sign.ibytedtos.com/obj/captcha-dl-usa-us/3d_2385_ab3b13ae51bc5b0902b15c2c5dca12a06674c194_1.jpg?x-expires=1676224658&x-signature=35C3enKiLP2FdZcS06fsTJyF8uo%3D").content
# from urllib.request import urlopen 
# import base64

# cc = base64.b64encode(urlopen("https://lf19-captcha-sign.ibytedtos.com/obj/captcha-dl-usa-us/3d_2385_ab3b13ae51bc5b0902b15c2c5dca12a06674c194_1.jpg?x-expires=1676224658&x-signature=35C3enKiLP2FdZcS06fsTJyF8uo%3D").read())
# print(cc)

import base64
import requests


def get_as_base64(url):

    return base64.b64encode(requests.get(url).content)
print(get_as_base64('https://p19-captcha-va.ibyteimg.com/tos-maliva-i-71rtze2081-us/5ec7a760e9f948a3b29236ab80c00cdb~tplv-71rtze2081-1.png'))
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import cv2
# plt.imshow(cv2.imread(r"C:\Users\Chido\Downloads\cbimage.png"))
# plt.show()
def solve_choose(driver):
        #/html/body/div[8]/div/div[3]/div[2]
        achains = ActionChains(driver)
        for position in range(5,9):
            try:
                img = driver.find_element(
                    By.XPATH,  f'/html/body/div[{position}]/div/div[2]/img')
                break
            except:
                pass
        else:
            return False

        el = driver.find_element(
            By.XPATH,  f'/html/body/div[{position}]/div/div[2]')


        # Xử lý captcha bên folder Solve Captcha
        rectangles, result = Bypass_captcha_same(img.size['width'], img.size['height'], dow_img_the_same(img.get_attribute("src"))).solve_the_same()
            
        if result == False:
            driver.find_element(
            By.XPATH,  f"/html/body/div[{position}]/div/div[3]/div[1]/a[1]/span[2]").click()
            sleep(2)
        else:
            for (x, y, w, h) in rectangles:
                achains.move_to_element_with_offset(el, -img.size['width']/2, img.size['height']/2).\
                        move_by_offset(x+w/2, -img.size['height']+y+h/2).click().perform()
                sleep(1)
            driver.find_element(
                    By.XPATH, f'/html/body/div[{position}]/div/div[3]/div[2]').click()
            sleep(2)
            return True