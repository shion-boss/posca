from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
from django.conf import settings

# Create your views here.


def index_view(request):
    #options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    #※headlessにしている
    options = Options()
    #headlessの設定をTrueにする
    options.headless = True
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome()
    driver.implicitly_wait(60)
    driver.get('https://www.instagram.com/?hl=ja')
    l=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    l.send_keys('dn.2a1')
    r=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    r.send_keys(settings.PAS)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
    driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[4]/a').click()
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[4]/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/a').click()
    a=driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h2')
    t=a.get_attribute("textContent")
    params={
        'a':t,
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
        #options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options = Options()
        #headlessの設定をTrueにする
        options.headless = True
        #※headlessにしている
        driver = webdriver.Chrome(options=options)
        #driver = webdriver.Chrome()
        driver.implicitly_wait(60)
        driver.get('https://www.instagram.com/?hl=ja')
        l=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        l.send_keys('dn.2a1')
        r=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        r.send_keys(settings.PAS)
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[4]/a').click()
        driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[4]/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/a').click()
        a=driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h2')
        t=a.get_attribute("textContent")

        #search_box = driver.find_element_by_name("q")
        #search_box.send_keys('インスタグラム')
        #search_box.submit()
        #s=driver.find_element_by_xpath('//*[@id="rso"]/div['+str(input_text)+']/div/div[1]/a/h3/span').click()
        #a=driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/div/p/a/span').get_attribute("textContent")
        driver.quit()
        return HttpResponse(t)
    else:
        return HttpResponse('こんにちわ')
