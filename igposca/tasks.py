from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from celery import shared_task
from .models import Widget
from posca.celery import app
import time
from django_celery_results.models import TaskResult
from .pm import save_post,random_time
from celery.decorators import periodic_task
from datetime import timedelta



@app.task
def add(x, y):
    random_time()
    Widget(name='??分間もよく耐えた！').save()
    return x + y

from celery.decorators import periodic_task
from datetime import timedelta
"""
@periodic_task(run_every=timedelta(seconds=10000))
def test_task():
    Widget(name='こんにた').save()
    return 'okだよ'


@app.task(name='task_number_one')
def mul(x, y):
    Widget(name='予定通りだな').save()
    return x * y

"""
@app.task(name='task_search_taged')
def search_taged():
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
    driver.implicitly_wait(60)
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
