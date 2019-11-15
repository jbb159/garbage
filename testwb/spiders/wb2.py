# -*- coding: utf-8 -*-
import scrapy

from testwb.items import  wbItem
import re
class Wb2Spider(scrapy.Spider):
    name = 'wb2'
    allowed_domains = ['weibo.com']
    key = '吴彦祖'
    start_urls = ['https://s.weibo.com/weibo?q={}&Refer=index'.format(key)]

    def __init__(self):
        self.i = 1
        self.key = '吴彦祖'


    def start_requests(self):
        cookies = 'SINAGLOBAL=2365626625392.585.1570796110890; UM_distinctid=16dc2c7f446236-0c290e1055ebd2-5e4f281b-e1000-16dc2c7f4473e0; _s_tentry=www.baidu.com; Apache=832191630551.2955.1573702435009; ULV=1573702435026:59:15:15:832191630551.2955.1573702435009:1573647921582; Ugrow-G0=1ac418838b431e81ff2d99457147068c; TC-V5-G0=62b98c0fc3e291bc0c7511933c1b13ad; wb_view_log_5846939166=1280*7201.5; secsys_id=31981fd64250b6b2f1d1e3ff1fc32537; login_sid_t=4c190f86080839032c01abb953221fe0; cross_origin_proto=SSL; WBStorage=384d9091c43a87a5|undefined; wb_view_log=1280*7201.5; UOR=,,www.baidu.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhChY96YYuARE-CXQXxZzp35JpX5K2hUgL.Fo-RShq4e0.pSoq2dJLoI0qLxKqL1-BLBK-LxKqL1-BLB-qLxK-L1hML12BLxKqLB-2LBonLxKnL12eLBoqLxK-L1K-L122t; ALF=1605253300; SSOLoginState=1573717301; SCF=AuvOcFYfhWUVGa6ZR7byNobb1JLQRzd8WOXdYCbhRMYX6rrBc8s3UWigC4BiXZFY-fWoX7NfbHH0pbnO03y38q8.; SUB=_2A25wyXVlDeRhGeNG71QY8yfNzTqIHXVTv-GtrDV8PUNbmtAKLWz-kW9NS12oipZRdfaNkZ6H24AO1qU6U3JUBx6W; SUHB=0V5lBOKzzIQ_vi; un=18382108766; wvr=6; TC-Page-G0=b32a5183aa64e96302acd8febeb88ce4|1573717307|1573717307; webim_unReadCount=%7B%22time%22%3A1573717309460%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'
        cookies = {i.split('=')[0] :i.split('=')[1] for i in cookies.split(';')}
        yield scrapy.Request(self.start_urls[0],cookies=cookies)


    def parse(self, response):
        # 收集用户id  ，内容，转发数目，评论数目
        user = response.xpath('.//div[@class="content"]//a[@class="name"]/@nick-name').extract()
        print(len(user),"用户数量！！！！")
        userid = response.xpath('.//div[@class="info"]//a[@class="name"]/@href').extract()
        userids = []
        for id in userid:
            s=re.findall(r'\.com\/(\d+)\?ref',id)
            userids.append(s)
        print(len(userids),'用户id数量！！')


        dianzan  =response.xpath('.//div[@class="card-wrap"]//div[@class="card-act"]//li[4]/a/em/text()').extract()
        zhuanfa = response.xpath('.//div[@class="card-wrap"]//div[@class="card-act"]//li[2]/a/text()').extract()
        pinglun= response.xpath('.//div[@class="card-wrap"]//div[@class="card-act"]//li[3]//a/text()').extract()
        print("+++++++++++")
        mess = response.xpath(".//div[@class='content']/p[@class='txt']/text()").extract()
        for x,y,z,f,g,h in zip(user,userids,dianzan,zhuanfa,pinglun,mess):
            print(x,y,z,f,g)
            print("\r\n")

        item  = wbItem()
        item['name'] =x
        item['id'] =y
        item['dianzan'] =z
        item['zhuanfa'] =f
        item['pinglun'] =g
        item['message'] = h
        yield  item


        self.i +=1
        next_url = 'https://s.weibo.com/weibo?q={}&Refer=index&page={}'.format(self.key,self.i)

        yield   scrapy.Request(next_url,callback=self.parse)



        # pinlun = response.xpath('.//div[@class="card-wrap"]//div[@class="card-act"]//li[3]/a/text()').extract()
        # pinlun = [ re.findall(r'评论.*(\d+)',i )for i in pinlun]
