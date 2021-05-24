from selenium import webdriver
import os
import urllib.request
import time
import datetime
from selenium.webdriver.chrome.options import Options
from PIL import Image

chrome_options = Options()
chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")


def doScrollDown(whileSeconds, driver):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        if datetime.datetime.now() > end:
            break

header_n = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

def crawl(keywords):
    path = "https://www.google.com/search?q=" + keywords + "&newwindow=1&rlz=1C1CAFC_enKR908KR909&sxsrf=ALeKk01k_BlEDFe_0Pv51JmAEBgk0mT4SA:1600412339309&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj07OnHkPLrAhUiyosBHZvSBIUQ_AUoAXoECA4QAw&biw=1536&bih=754"
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")
    driver = webdriver.Chrome('./chromedriver',options=options)
    #driver.implicitly_wait(3)
    driver.get(path)
    driver.maximize_window()
    #time.sleep(1)

    counter = 0
    succounter = 0

    for x in driver.find_elements_by_class_name('rg_i.Q4LuWd'):
        counter = counter + 1
        #print(counter)
        # 이미지 url
        img = x.get_attribute("data-src")
        if img is None:
            img = x.get_attribute("src")
        #print(img)

        # 이미지 확장자
        imgtype = 'jpg'

        # 구글 이미지를 읽고 저장한다.

        try:
            raw_img = urllib.request.urlopen(img).read()
            File = open(os.path.join('resource\\school_img.png'), "wb")
            File.write(raw_img)
            File.close()

            resized_img = Image.open('resource\\school_img.png').resize((240, 135))
            resized_img.save('resource\\school_img.png')
            return 0
        except:
            print('error')

    #print(succounter, "succesfully downloaded")
    driver.close()


