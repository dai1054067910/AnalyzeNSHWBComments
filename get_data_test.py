from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
import re

if not os.path.exists('./Data'):
    os.mkdir('./Data')


browser = webdriver.Chrome('D:/software/chromedriver_win32/chromedriver')
url = 'https://weibo.com/u/5769940593?profile_ftype=1&is_all=1#_0'
browser.get(url)
print('Waiting')
time.sleep(15)
print('Finish Waiting')

Pl_Official_MyProfileFeed__25 = browser.find_element_by_id('Pl_Official_MyProfileFeed__25')
WB_feed_WB_feed_v3_WB_feed_v4 = Pl_Official_MyProfileFeed__25.find_element_by_css_selector('div[module-type="feed"]')
divs = WB_feed_WB_feed_v3_WB_feed_v4.find_elements_by_css_selector('div[tbinfo="ouid=5769940593"]')
TIMES = 0
FLESH_TIME = 0

WEIBO_COUNT = 8
for i in range(WEIBO_COUNT):
    div = divs[i]
    fl_comment = div.find_element_by_css_selector('a[action-type="fl_comment"]')
    ActionChains(browser).click(fl_comment).perform()
    time.sleep(2)
    need_approval_comment = div.find_element_by_css_selector('div[node-type="need_approval_comment"]')
    list_ul = need_approval_comment.find_element_by_css_selector('div[class="list_ul"]')
    _blank = list_ul.find_elements_by_css_selector('a[target="_blank"]')[-1]
    ActionChains(browser).click(_blank).perform()
    browser.switch_to_window(browser.window_handles[1])
    time.sleep(5)

    browser.execute_script('window.scrollTo(0, 10000)')
    time.sleep(1)
    browser.execute_script('window.scrollTo(0, 100000)')
    time.sleep(1)
    list_ul = browser.find_element_by_css_selector('div[class="list_ul"]')
    more_click_list = list_ul.find_elements_by_css_selector('a[class="WB_cardmore S_txt1 S_line1 clearfix"]')
    pre_comment_count = 0
    while len(more_click_list) > 0:
        more_click = more_click_list[-1]
        ActionChains(browser).click(more_click).perform()
        time.sleep(1)
        browser.execute_script('window.scrollTo(0, 100000)')
        time.sleep(1)
        list_ul = browser.find_element_by_css_selector('div[class="list_ul"]')
        comments = list_ul.find_elements_by_css_selector('div[class="WB_text"]')
        more_click_list = list_ul.find_elements_by_css_selector('a[action-type="click_more_comment"]')
        if len(comments)-pre_comment_count == 0:
            break
        print(len(comments))
        pre_comment_count = len(comments)

    comments = list_ul.find_elements_by_css_selector('div[class="WB_text"]')
    total_text = ''
    print('comments count: ', len(comments))
    for comment in comments:
        string = comment.text
        if '回复' in string:
            continue
        else:
            if '：' in string:
                string = re.split(r'：', string, maxsplit=1)[1]
            total_text += (' '+string)

    with open('./Data/' + str(i) + '.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(total_text)

    browser.close()
    browser.switch_to_window(browser.window_handles[0])
    print(
        ' Finish', TIMES
    )
browser.close()