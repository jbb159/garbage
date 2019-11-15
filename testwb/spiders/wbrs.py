# -*- coding: utf-8 -*-
import scrapy
import re
from testwb.items import wbItem

class WbrsSpider(scrapy.Spider):
    name = 'wbrs'
    allowed_domains = ['weibo.com']
    key = '杨超越'
    start_urls = ['https://s.weibo.com/weibo?q={}&Refer=top_summary'.format(key)]

    def __init__(self):
        self.i = 1

    def start_requests(self):

        cookie = 'SINAGLOBAL=2365626625392.585.1570796110890; UM_distinctid=16dc2c7f446236-0c290e1055ebd2-5e4f281b-e1000-16dc2c7f4473e0; _s_tentry=login.sina.com.cn; Apache=5271311587734.826.1573647921524; ULV=1573647921582:58:14:14:5271311587734.826.1573647921524:1573637729216; WBStorage=384d9091c43a87a5|undefined; login_sid_t=71dec798a15d52dbc1efac58e32b45d6; cross_origin_proto=SSL; UOR=,,login.sina.com.cn; webim_unReadCount=%7B%22time%22%3A1573653089722%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; WBtopGlobal_register_version=307744aa77dd5677; SCF=AuvOcFYfhWUVGa6ZR7byNobb1JLQRzd8WOXdYCbhRMYXzofXViBiuy9wbNp7Ynj4B2z9KOXwvK8H1xPv1fEiWak.; SUB=_2A25wyHohDeRhGeNG71QY8yfNzTqIHXVTvOzprDV8PUNbmtAKLW2jkW9NS12oipJqCS-CIqlwyNX0C_iHLMmIhF1s; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhChY96YYuARE-CXQXxZzp35JpX5K2hUgL.Fo-RShq4e0.pSoq2dJLoI0qLxKqL1-BLBK-LxKqL1-BLB-qLxK-L1hML12BLxKqLB-2LBonLxKnL12eLBoqLxK-L1K-L122t; SUHB=0xnCvC_iRtDb1E; ALF=1574257905; SSOLoginState=1573653105; un=18382108766'
        b = {i.split("=")[0]:i.split("=")[1] for i in cookie.split(";")}
        print(b)
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=b)

    def parse_detail(self, response):
        num = re.findall(r'(\d+)',response.text)
        print(num)

    def parse(self, response):

        print("*"*32)
        divs  = response.xpath('.//div[@class="card-wrap"]')
        for i in divs:
            name = response.xpath('.//a[@class="name"]/text()').extract()
            urls = response.xpath('.//div[@class="avator"]/a/@href').extract()




        review_lists = []
        review_list = re.findall(r's-color-red">杨<\/em><em class="s-color-red">超越<\/em>(.+)? <\/p>',response.text)
        for i in review_list:
            i = i.replace('<em class="s-color-red">杨</em><em class="s-color-red">超越</em>','杨超越')
            print("\r\n")
            i = re.sub(r'<img.+>','',i)
            i = re.sub(r'<a.+>', '', i)
            i = re.sub(r'<\/a>','',i)
            i = re.sub(r'<br\/>','',i)
            i = re.sub(r'<em.+>','',i)
            i = i.strip()
            i = i.replace('\u200b','')
            print(i)
            review_lists.append(i)


        item = wbItem()

        for x,y,z in zip(name,urls,review_lists):
            y = 'http:' + y
            print(x,y,z)
            item['name']=x
            item['private_url'] = y
            item['comment'] = z

            # yield scrapy.Request(y,callback=self.parse_detail,dont_filter=True)

            yield item

        # 翻页
        print("*"*32)
        print("\r\n\r\n")
        self.i = self.i + 1
        nexturl = 'https://s.weibo.com/weibo/%25E6%259D%25A8%25E8%25B6%2585%25E8%25B6%258A?topnav=1&wvr=6&b=1&page={}'.format(self.i)
        yield  scrapy.Request(nexturl,callback=self.parse,)

