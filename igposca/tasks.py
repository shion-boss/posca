from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from celery import shared_task
from .models import Widget,taged_data,posca_point
from posca.celery import app
import time
from django_celery_results.models import TaskResult
from .pm import save_post,random_time
from celery.decorators import periodic_task
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import os
from django_celery_results.models import TaskResult
from celery.result import AsyncResult
from django.core import serializers
import logging




@app.task
def add():
    time.sleep(300)
    Widget(name='いけてるね。12/9').save()
    return 'ok'

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
    driver.get('https://www.instagram.com/accounts/login/')
    random_time()
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
    return [{"status": True}]

#,serializer='json'



@app.task(name='task_likes')
def ig_like_view():
    logger = logging.getLogger(__name__)
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions') #すべての拡張機能を無効にする。ユーザースクリプトも無効
    options.add_argument('--proxy-server="direct://"') # Proxy経由ではなく直接接続する
    options.add_argument('--proxy-bypass-list=*')      # すべてのホスト名
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size('1200', '1000')
    driver.implicitly_wait(30)
    driver.set_page_load_timeout(100)
    

    #インスタグラムを検索
    try:
        driver.get('https://www.instagram.com/accounts/login/')
    except:
        logger.info('Instagramを開けませんでした。')
    else:
        logger.info('Instagramを開きました。')
    try:
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys('dn.2a1')
    except:
        logger.info('ユーザーネームを打ち込めませんでした。')
        print('ユーザーネームを打ち込めませんでした。')
    else:
        logger.info('ユーザーネームを打ち込みました。')
        print('ユーザーネームを打ち込みました。')
    try:
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys('dntwoaone')
    except:
        logger.info('パスワードを打ち込めませんでした。')
        print('パスワードを打ち込めませんでした。')
    else:
        logger.info('パスワードを打ち込みました。')
        print('パスワードを打ち込みました。')
    try:
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    except:
        logger.info('ログインに失敗')
        print('ログインに失敗')
    else:
        logger.info('ログインに成功')
        print('ログインに成功')
    #ユーザーネーム入力
    """
    go = True
    while go:
        try:
            driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys('dn.2a1')
        except:
            logger.info('ユーザーネームを打ち込めませんでした。')
            go=True
        else:
            logger.info('ユーザーネームを打ち込みました。')
            go=False

    if len(driver.find_elements_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input'))==1:
        un=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        un.send_keys('dn.2a1')
    elif len(driver.find_elements_by_xpath("//form[input/@name='username']"))==1:
        un=driver.find_element_by_xpath("//form[input/@name='username']")
        un.send_keys('dn.2a1')
    elif len(driver.find_elements_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input'))==1:
        un=driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
        un.send_keys('dn.2a1')
    else:
        d=len(driver.find_elements_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input'))
        data= str(d)+':input[username]を取得出来ませんでした。'
        return data
    """
    #パスワード入力
    """
    go = True
    while go:
        try:
            driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys('dntwoaone')
        except:

            go=True
        else:

            go=False
        #execute_script('document.getElementsByName("name属性")[0].value="%s";' % text)
    time.sleep(5)
    try:
        driver.execute_script('document.getElementsByClassName("_9GP1n")[0].classList.add("HlU5H");')
        driver.execute_script('document.getElementsByName("username")[0].classList.add("focus-visible");')
        driver.execute_script('document.getElementsByName("username")[0].dataset.focusVisibleAdded="";')
        driver.execute_script('document.getElementsByClassName("f0n8F")[0].classList.add("FATdn");')
        #driver.execute_script('document.getElementsByName("username")[0].value="%s";' %'dn.2a1')
        driver.execute_script('document.getElementsByName("username")[0].setAttribute("value", "dn.2a1");')
        driver.execute_script('document.getElementsByName("username")[0].removeAttribute("data-focus-visible-added");')
        driver.execute_script('document.getElementsByName("username")[0].classList.remove("focus-visible");')
        driver.execute_script('document.getElementsByClassName("_9GP1n")[0].classList.remove("HlU5H");')
    except:
        print('JavaScript失敗')
        #logger.info('ユーザーネームを打ち込めませんでした。')
    else:
        print('JavaScript成功')
        #logger.info('ユーザーネームを打ち込みました。')

    try:
        driver.execute_script('document.getElementsByClassName("_9GP1n")[1].classList.add("HlU5H");')
        driver.execute_script('document.getElementsByName("password")[0].classList.add("focus-visible");')
        driver.execute_script('document.getElementsByName("password")[0].dataset.focusVisibleAdded="";')
        driver.execute_script('document.getElementsByClassName("f0n8F")[1].classList.add("FATdn");')
        #driver.execute_script('document.getElementsByName("password")[0].value="%s";' %'dntwoaone')
        driver.execute_script('document.getElementsByName("password")[0].setAttribute("value", "dntwoaone");')
        driver.execute_script('document.getElementsByName("password")[0].removeAttribute("data-focus-visible-added");')
        driver.execute_script('document.getElementsByName("password")[0].classList.remove("focus-visible");')
        driver.execute_script('document.getElementsByClassName("_9GP1n")[1].classList.remove("HlU5H");')
    except:
        print('JavaScript失敗')
        #logger.info('パスワードを打ち込めませんでした。')
    else:
        print('JavaScript成功２')
        #logger.info('パスワードを打ち込みました。')
    time.sleep(1)
    #driver.execute_script('document.getElementsByTagName("button")[0].disabled = false;')
    time.sleep(3)
    if len(driver.find_elements_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input'))==1:
        ik=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        ik.send_keys('dntwoaone')
    elif len(driver.find_elements_by_xpath("//form[input/@name='password']"))==1:
        ik=driver.find_element_by_xpath("//form[input/@name='password']")
        ik.send_keys('dntwoaone')
    elif len(driver.find_elements_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input'))==1:
        ik=driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
        ik.send_keys('dntwoaone')
    else:
        return 'input[password]を取得出来ませんでした。'

    #インスタグラムにログイン
    go =True
    while go:
        try:
            driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
        except:
            logger.info('ログインに失敗しました。')
            go=True
        else:
            logger.info('ログインに成功しました。')
            go=False

    if len(driver.find_elements_by_xpath('//*[@id="loginForm"]/div/div[3]')) ==1:
        login=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]')
        login.click()
    elif len(driver.find_elements_by_xpath('//*[@id="loginForm"]/div/div[3]/button')) ==1:
        login=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
        login.click()
    elif len(driver.find_elements_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')) ==1:
        login=driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
        login.click()
    elif len(driver.find_elements_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div')) ==1:
        login=driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div')
        login.click()
    elif len(driver.find_elements_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')) ==1:
        login=driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')
        login.click()
    """
    #情報を保存しない
    try:
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
    except:
        logger.info('「情報を保存しない」をクリック出来ませんでした。')
    else:
        logger.info('「情報を保存しない」をクリックしました。')
    #お知らせを受け取らない
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    except:
        logger.info('「お知らせを受け取らない」をクリック出来ませんでした。')
    else:
        logger.info('「お知らせを受け取らない」をクリックしました。')
    for s in range(10):
        driver.get('https://www.instagram.com/explore/tags/息子/?hl=ja')
        random_time()
        if len(driver.find_elements_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[2]'))==1:
            driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[2]').click()
        elif len(driver.find_elements_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div/div[2]'))==1:
            driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div/div[2]').click()
        else:
            logger.info('最新の投稿を取得できませんでした。')
        random_time()
        for i in range(11):
            e=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[2]')
            webdriver.ActionChains(driver).double_click(e).perform()
            random_time()
            driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]').click()
            random_time()
        logger.info('一つ目のいいねが完了しました。')

        driver.get('https://www.instagram.com/explore/tags/娘/?hl=ja')
        random_time()
        if len(driver.find_elements_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[2]'))==1:
            driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[2]').click()
        elif len(driver.find_elements_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div/div[2]'))==1:
            driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div/div[2]').click()
        else:
            logger.info('最新の投稿を取得できませんでした。')

        random_time()
        for i in range(11):
            e=driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[2]/div/div/div[2]')
            webdriver.ActionChains(driver).double_click(e).perform()
            random_time()
            driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]').click()
            random_time()
        logger.info('二つ目のいいねが完了しました。')
        time.sleep(3000)

    driver.close()
    return 'いいね完了'
