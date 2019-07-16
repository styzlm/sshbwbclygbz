

import os
import re
import time
import logging
import pickle
import requests
import numpy as np
from lxml import etree
import config
import codecs

pattern = re.compile('\d+')


class WbScrapy(object):
    def __init__(self):
        self.filter_flag = 0
        self.rest_time = 20  # 等待时间
        self.weibo_comment_detail_urls = []  # 微博评论地址

        self.rest_min_time = 10
        self.rest_max_time = 20

        self.get_cookies_by_account()
        self.request_header()


    # 加载cookie
    def get_cookies_by_account(self):
        with open(config.COOKIE_SAVE_PATH, 'rb') as f:
            cookie = pickle.load(f)
            # 未来抓取页面需要的可不登陆的cookie
            self.cookie = {
                "Cookie": cookie[config.ACCOUNT_ID]
            }

    # 获取请求的cookie和headers
    def request_header(self):
        # 避免被禁，获取头文件
        headers = requests.utils.default_headers()
        user_agent = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
        }
        headers.update(user_agent)
        self.headers = headers



    def get_content_and_comment_to_db(self, limit=3,uid = '3216482742',code = 'Ho4vl3qnK'):

        try:
            i = 0

            content_and_comment_dict = {}
            comment_url = 'http://weibo.cn/comment/{}?uid={}&rl={}'.format(code,uid,i)
            html_detail = requests.get(comment_url, cookies=self.cookie, headers=self.headers).content
            selector_detail = etree.HTML(html_detail)
            resultlist = []
            file_path = r'.\weiboComment_' + uid + '.txt'
            shu = codecs.open(file_path, 'a', encoding='utf-8')

            if selector_detail.xpath("//div[@id='pagelist']//div/input[1]/@value") is None:
                pass
            else:
                all_comment_pages = int(
                    selector_detail.xpath("//div[@id='pagelist']//div/input[1]/@value")[0])
                print(all_comment_pages)

            content_and_comment_dict["comment"] = []


            end_idx = all_comment_pages - 2
            if end_idx > limit:
                end_idx = limit

            for page in range(1, end_idx):
                print("当前解析的页面是{}, 总页面{}。".format(page, end_idx))

                if page % 5 == 0:
                    rest_time = np.random.randint(self.rest_min_time, self.rest_max_time)
                    time.sleep(rest_time)


                detail_comment_url = comment_url + "&page=" + str(page)
                print(detail_comment_url)


                html_detail_page = requests.get(url=detail_comment_url, cookies=self.cookie,
                                                headers=self.headers).content
                selector_comment_detail = etree.HTML(html_detail_page)

                comment_list = selector_comment_detail.xpath("//div[starts-with(@id, 'C_')]")

                for comment in comment_list:
                    single_comment_user_name = comment.xpath("a[1]/text()")[0]

                    print(len(comment.xpath('span[1]//text()')))
                    single_text = comment.xpath('span[1]//text()')
                    single_comment_content = ''

                    single_comment_content = single_comment_content.join(single_text)

                    result_dict = {'username': single_comment_user_name, 'commentCount': single_comment_content}
                    resultlist.append(result_dict)
                    full_single_comment = '<' + single_comment_user_name + '>' + ': ' + single_comment_content
                    print(full_single_comment)
                    shu.write(full_single_comment + '\n\r')

                    content_and_comment_dict['comment'].append(full_single_comment)
                    content_and_comment_dict['last_idx'] = page



        except Exception as e:
            logging.error('在获取微博内容和评论的过程中抛出异常, error:', e)
            print('\n' * 2)
            print('=' * 20)

def tongji(uid = '3216482742',code = 'Ho4vl3qnK'):
    filename = '.\weiboComment_' + uid + '.txt'
    f = codecs.open(filename, "r", encoding='utf-8')
    total = 0
    hit = 0
    for x in f:
        if len(x) == 1:
            total = total + 1
        if "还愿" in x:
            hit = hit + 1

    print(total)
    print(hit)
    print(hit / total)


if __name__ == "__main__":
    wb_scrapy = WbScrapy()
    wb_scrapy.get_content_and_comment_to_db(limit=10,uid = '3216482742',code = 'Ho4vl3qnK')
    huanyuanlv = tongji(uid = '3216482742',code = 'Ho4vl3qnK')
