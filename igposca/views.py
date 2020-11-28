from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
from django.conf import settings
import urllib
import os
from .models import taged_data,posca_point
from .tasks import test_task,add,mul
from django_celery_results.models import TaskResult
from celery.result import AsyncResult


# Create your views here.
def save_post(driver,count):
    #poscagramの投稿か確認
    try:
        ign=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a')
    except:
        #print('ignameを取得出来ませんでした')
        try:
            ign=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div/span/a')
        except:
            pass
            #print('poscagramのignameを取得出来ませんでした')
    #usernameを取得
    igname=ign.text
    #print(igname)
    if igname == 'poscagram':
        p_point=posca_point.objects.order_by("id").first()
        if p_point.count == 0:
            p_point.count=1
            p_point.save()
            if count == 0 and len(driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div/div/a'))>0:
                #2つ目の投稿へ
                driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a').click()
            elif len(driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]'))>0:
                #3つ目以降の投稿へ
                driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]').click()
            else:
                return False
            return True
        else:
            p_point.count=0
            p_point.save()
            return False
    cur_url = driver.current_url
    if taged_data.objects.filter(page_url=cur_url).exists():
        if count == 0 and len(driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div/div/a'))>0:
            #2つ目の投稿へ
            driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a').click()
        elif len(driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]'))>0:
            #3つ目以降の投稿へ
            driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]').click()
        else:
            return False

        return True
    #メイン画像を取得
    try:
        main_img = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[1]/div[1]/img')
    except:
        main_img = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img')
    main_src = main_img.get_attribute('src')
    #print("画像の枚数によって変わる？")
    #トップ画像を取得
    top_img=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[1]/div/a/img')
    top_src=top_img.get_attribute('src')
    #print('トプ画取得')
    #続きを読む
    try:
        readmore=driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/div[1]/div/div/div[1]/div/span/span[2]/button')
    except:
        pass
    else:
        readmore.click()
    if len(driver.find_elements_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span')) >0:
        message=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span')
        text=message.text
    elif len(driver.find_elements_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/ul[1]/div/li/div/div[1]/div[2]/span')) >0:
        message=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/ul[1]/div/li/div/div[1]/div[2]/span')
        text=message.text
    else:
        text=''
    #print(text)
    #taged_dataに投稿を保存
    taged_data(igname=igname,top_img_url=top_src,main_img_url=main_src,text=text,page_url=cur_url).save()

    if count == 0 and len(driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div/div/a'))>0:
        #2つ目の投稿へ
        driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a').click()
    elif len(driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]'))>0:
        #3つ目以降の投稿へ
        driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]').click()
    else:
        return False
    return True

def index_view(request):
    task=add.delay(10,5)
    task_id = task.id
    a=AsyncResult(task_id).status
    return HttpResponse(a)

def index2_view(request):
    b=mul.delay(4,5)
    params={
        'a':b,
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
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions') #すべての拡張機能を無効にする。ユーザースクリプトも無効
    options.add_argument('--proxy-server="direct://"') # Proxy経由ではなく直接接続する
    options.add_argument('--proxy-bypass-list=*')      # すべてのホスト名
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(30)
    driver.set_page_load_timeout(100)
    #インスタグラムを検索
    driver.get('https://www.instagram.com')
    #ユーザーネーム入力
    l=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    l.send_keys('poscagram')
    #パスワード入力
    r=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    r.send_keys(settings.IGKEY)
    #インスタグラムにログイン
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    #情報を保存しない
    try:
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
    except:
        pass
    #お知らせを受け取らない
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    except:
        pass
    #タグ付けさえた投稿を検索
    driver.get('https://www.instagram.com/poscagram/tagged/')
    #最新の投稿を開く
    driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/article/div/div/div[1]/div[1]').click()
    ################################
    count=0
    while save_post(driver=driver,count=count):
        count+=1
        #print('yeah')
    else:
        pass
        #print('ふぅ、、疲れたぜ')
    data='おまえは天才'
    driver.close()
    return HttpResponse(data)


def ajax_test_view(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(100)
    #インスタグラムを検索
    driver.get('https://www.instagram.com')
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
    driver.close()
    """
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    mobile_emulation = { "deviceName": "iPhone X" }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get('https://www.instagram.com/?hl=ja')
    driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div/div/div/div[2]/button').click()
    l=driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[3]/div/label/input')
    l.send_keys('poscagram')
    time.sleep(1)
    #パスワード入力
    r=driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[4]/div/label/input')
    r.send_keys(settings.IGKEY)
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[6]/button').click()

    try:
        driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/button').click()
    except:
        pass
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    except:
        pass
    try:
        driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
    except:
        pass

    #j=driver.find_element_by_xpath('/html/body/div[1]/form/input')
    input=driver.find_elements_by_tag_name('input')
    vvv=0
    for i in input:
        try:
            driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/button').click()
        except:
            pass
        try:
            driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        except:
            pass
        try:
            driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
        except:
            pass
        vvv+=1
        if vvv !=1:
            continue
        try:
            i.send_keys("C:/Users/ssstl/OneDrive/デスクトップ/2021_newyearcamp_2Days/2021_newyearcamp_2Days/AdobeStock_277473598.jpeg")
        except:
            print(str(i) + "　is can't send_key")

        else:
            print(str(i) + "　is can send_key")
    """
    p_point=posca_point.objects.order_by("id").first()
    return HttpResponse('ajax接続完了'+str(p_point.count))
    #driver.find_element_by_xpath('/html/body/div[1]/section/nav[2]/div/div/div[2]/div/div/div[3]').click()

"""
j=driver.find_element_by_xpath('/html/body/div[1]/section/nav[2]/div/div/form/input')
j.send_keys("C:/Users/ssstl/OneDrive/デスクトップ/2021_newyearcamp_2Days/2021_newyearcamp_2Days/AdobeStock_277473598.jpeg")
j.send_keys("C:/Users/ssstl/OneDrive/デスクトップ/2021_newyearcamp_2Days/2021_newyearcamp_2Days/AdobeStock_277473598.jpeg")
j=driver.find_element_by_xpath('/html/body/div[1]/section/nav[2]/div/div/form/input')
j.send_keys("C:/Users/ssstl/OneDrive/デスクトップ/2021_newyearcamp_2Days/2021_newyearcamp_2Days/AdobeStock_277473598.jpeg")
return HttpResponse('ajax接続完了')
profile
/html/body/div[1]/section/main/div[1]/form/input
    /html/body/div[1]/form/input
    /html/body/div[1]/section/main/section/div[1]/div/div/div/div/button/form/input
    /html/body/div[1]/section/nav[2]/div/div/form/input
"""
#.tb_sK


#画像をフォルダを指定して保存する
#img_name='img_'+str(i)+'.png'
#urllib.request.urlretrieve(src, os.path.join('media', img_name))
