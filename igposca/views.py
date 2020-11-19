from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time

# Create your views here.


def index_view(request):
    params={
        'a':'b',
    }
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.google.com/')
    time.sleep(5)
    search_box = driver.find_element_by_name("q")
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    time.sleep(5)
    driver.quit()
    return render(request,'igposca/index.html',params)

def index2_view(request):
    params={
        'a':'b',
    }
    return render(request,'igposca/index.html',params)

def test_ajax_response(request):
    if request.method == 'POST':
        input_text = request.POST["input_data"]
        hoge = "Ajax Response: " + input_text
        #options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        #driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome()
        driver.get('https://www.google.com/')
        time.sleep(5)
        search_box = driver.find_element_by_name("q")
        search_box.send_keys('ChromeDriver')
        search_box.submit()
        time.sleep(5)
        driver.quit()
        return HttpResponse(hoge)
