# -*- coding: utf-8 -*-
import scrapy
from testwb.items  import hrItem
import json
class HrSpider(scrapy.Spider):
    def __init__(self):
         self.i = 1


    name = 'hr'
    allowed_domains = ['tencent.com']
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1573650571182&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40009&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn']

    def parse(self, response):
        rs = json.loads(response.text)
        print(type(rs))
        print("*"*32)
        lista = rs.get('Data').get('Posts')
        for i in lista:
            print(i.get('Responsibility'))
        print("*"*32)
        self.i = self.i + 1
        next_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40009&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn%27]'.format(self.i)
        yield scrapy.Request(next_url,callback=self.parse,)

