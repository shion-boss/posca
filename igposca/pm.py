import random,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .models import taged_data,posca_point


def random_time():
    t=random.uniform(1, 3)
    time.sleep(t)
    return t


def save_post(driver,count):
    random_time()
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
