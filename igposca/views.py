from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
from django.conf import settings
import urllib
import os

# Create your views here.


def index_view(request):
    params={
        'a':'1',
    }
    return render(request,'igposca/index.html',params)

def index2_view(request):
    params={
        'a':'b',
    }
    return render(request,'igposca/index.html',params)

def test_ajax_response(request):
    if request.method == 'POST':
        input_text = request.POST['input_data']
        hoge = "Ajax Response: " + str(input_text)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        #※headlessにしている
        #options = Options()
        #headlessの設定をTrueにする
        #options.headless = True
        driver = webdriver.Chrome(options=options)
        #driver = webdriver.Chrome()
        driver.implicitly_wait(60)
        driver.get('https://www.instagram.com/?hl=ja')
        time.sleep(1)
        l=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        l.send_keys('dn.2a1')
        time.sleep(1)
        r=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        r.send_keys(settings.PAS)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(1)
        try:
            driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        except:
            pass
        time.sleep(1)
        driver.get('https://www.instagram.com/explore/tags/病み/')
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]').click()
        time.sleep(1)
        e=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[2]')
        webdriver.ActionChains(driver).double_click(e).perform()
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a').click()
        for i in range(10):
            e=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[2]')
            webdriver.ActionChains(driver).double_click(e).perform()
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]').click()


        #search_box = driver.find_element_by_name("q")
        #search_box.send_keys('インスタグラム')
        #search_box.submit()
        #s=driver.find_element_by_xpath('//*[@id="rso"]/div['+str(input_text)+']/div/div[1]/a/h3/span').click()
        #a=driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/div/p/a/span').get_attribute("textContent")
        #driver.quit()
        #driver.close()
        return HttpResponse('ふぅ、、完了だぜ。')
    else:
        return HttpResponse('こんにちわ')



def search_tags_ajax_view(request):
    if request.method == 'GET':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(60)
        driver.get('https://www.instagram.com/?hl=ja')
        l=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        l.send_keys('poscagram')
        time.sleep(1)
        r=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        r.send_keys(settings.IGKEY)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        time.sleep(1)
        driver.get('https://www.instagram.com/poscagram/tagged/')
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[2]/article/div/div/div/div[1]').click()
        img = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img')
        src = img.get_attribute('src')
        urllib.request.urlretrieve(src, os.path.join('media', 'momo.png'))


        return HttpResponse('ふぅ、、完了だぜ。')
