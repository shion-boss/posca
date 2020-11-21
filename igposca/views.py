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
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    a=driver.find_element_by_xpath('//*[@id="rso"]/div[5]/div/div[1]/a/h3/span').get_attribute("textContent")
    driver.quit()
    p=0
    for i in range(10):
        p +=1
        driver.get('https://www.google.com/')
        search_box = driver.find_element_by_name("q")
        search_box.send_keys('ChromeDriver')
        search_box.submit()
        a=driver.find_element_by_xpath('//*[@id="rso"]/div['+str(input_text)+']/div/div[1]/a/h3/span').get_attribute("textContent")
        driver.quit()
    b= a + ':' + str(p)
    params={
        'a':b,
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
        #※headlessにしている
        driver = webdriver.Chrome(options=options)
        #driver = webdriver.Chrome()
        driver.implicitly_wait(60)
        p=0
        for i in range(10):
            p +=1
            driver.get('https://www.google.com/')
            search_box = driver.find_element_by_name("q")
            search_box.send_keys('ChromeDriver')
            search_box.submit()
            a=driver.find_element_by_xpath('//*[@id="rso"]/div['+str(input_text)+']/div/div[1]/a/h3/span').get_attribute("textContent")
            driver.quit()
        b= a + ':' + str(p)
        return HttpResponse(b)
    else:
        return HttpResponse('こんにちわ')
