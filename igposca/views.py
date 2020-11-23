from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
from django.conf import settings
import urllib
import os
from .models import taged_data

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
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(100)
    #インスタグラムを検索
    driver.get('https://www.instagram.com/?hl=ja')
    #ユーザーネーム入力
    l=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    l.send_keys('poscagram')
    time.sleep(1)
    #パスワード入力
    r=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    r.send_keys(settings.IGKEY)
    time.sleep(1)
    #インスタグラムにログイン
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    time.sleep(1)
    #情報を保存しない
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
    time.sleep(1)
    #お知らせを受け取らない
    driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    time.sleep(1)
    #タグ付けさえた投稿を検索
    driver.get('https://www.instagram.com/poscagram/tagged/')
    #最新の投稿を開く
    driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/article/div/div/div[1]/div[1]').click()
    #メイン画像を取得
    try:
        main_img = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[1]/div[1]/img')
    except:
        main_img = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img')
    main_src = main_img.get_attribute('src')
    print("画像の枚数によって変わる？")
    #usernameを取得
    ign=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a')
    print('いい感じ！')
    igname=ign.text
    print(igname)
    #トップ画像を取得
    top_img=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[1]/div/a/img')
    top_src=top_img.get_attribute('src')
    print('トプ画取得')
    #続きを読む
    try:
        readmore=driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/div[1]/div/div/div[1]/div/span/span[2]/button')
    except:
        pass
    else:
        readmore.click()
    message=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span')
    text=message.text
    print(text)
    #taged_dataに投稿を保存
    taged_data(igname=igname,top_img_url=top_src,main_img_url=main_img,text=text).save()
    data=str(igname)+'\n'+str(top_src)+'\n'+str(main_src)+'\n'+str(text)
    print(data)
    return HttpResponse(data)
"""
    taged=taged_data(igname=igname,top_img_url=top_src,main_img_url=main_src,text=text)
    taged.save()

    #2つ目の投稿へ
    driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a').click()
    for i in range(2):
        #画像を取得
        img = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[1]/div[1]/img')
        #画像のurlを取得
        src = img.get_attribute('src')
        #3つ目以降の投稿へ
        driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]').click()
        time.sleep(1)
"""


def ajax_test_view(request):
    return HttpResponse('ajax接続完了')


#画像をフォルダを指定して保存する
#img_name='img_'+str(i)+'.png'
#urllib.request.urlretrieve(src, os.path.join('media', img_name))
