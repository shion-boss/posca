from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time

# Create your views here.


def index_view(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #※headlessにしている
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome()
    driver.implicitly_wait(60)
    driver.get('https://www.google.com/')
    search_box = driver.find_element_by_name("q")
    search_box.send_keys('お金')
    search_box.submit()
    a=driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/a/h3/span').get_attribute("textContent")
    driver.quit()
    params={
        'a':a,
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
        #※headlessにしている
        #driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome()
        driver.implicitly_wait(60)
        driver.get('https://www.google.com/')
        search_box = driver.find_element_by_name("q")
        search_box.send_keys('インスタグラム')
        search_box.submit()
        s=driver.find_element_by_xpath('//*[@id="rso"]/div['+str(input_text)+']/div/div[1]/a/h3/span').click()
        a=driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/div/p/a/span').get_attribute("textContent")
        driver.quit()
        return HttpResponse(a)
    else:
        return HttpResponse('こんにちわ')
