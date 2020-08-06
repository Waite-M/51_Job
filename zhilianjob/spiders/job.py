# -*- coding: utf-8 -*-
import scrapy
import re

class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = []
    start_urls = ["https://js.51jobcdn.com/in/resource/js/2020/search/common.a8c323f7.js"]
    citydict = {}
    #搜索职位
    job = 'php'
    #地点
    position = '深圳'
    #爬取页数
    pages = '3'
    #解析js获取城市id
    def parse(self, response):
        city = re.findall(r'window.area={(.*?)"}', response.text)
        #获取列表形式的城市id
        citylist =  str(city).replace("[\'",'').replace("\']",'').replace('"','').split(',')
        #将citylist每个元素以字典形式存到citydict内
        for i in citylist:
            id = i.split(':')[0]
            name =i.split(':')[1]
            self.citydict[name] = id
        #将城市id,职业，爬取页码与搜索链接拼接成成的完整url进行爬取
        for i in range(int(self.pages)):
            searchurl = "https://search.51job.com/list/%s,000000,0000,00,9,99,%s,2,%d.html"%(self.citydict[self.position],self.job,i+1)
            yield scrapy.Request(searchurl,callback=self.parse_joblist,meta={'page':i+1})
    #解析搜索页面获取详细信息url
    def parse_joblist(self,response):
        jstext = response.xpath('/html/body/script[2]/text()').extract()
        jobdetail = re.findall(r'job_href":"(.*?)"',str(jstext))
        for url in jobdetail:
            detailurl = url.replace('\\\\','')
            self.log(detailurl)
            yield scrapy.Request(detailurl,callback=self.parse_detail,meta={'page':response.meta['page']})
    #解析职业详细信息页面
    def parse_detail(self,response):
        item = {}
        item['job'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/text()').extract()[0]
        item['company'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/text()').extract()[0]
        msg = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/@title').extract()[0].split('|')
        if len(msg) <= 3:
            item['region'] = msg[0]
            item['experience'] = '无'
            item['education'] = '无'
            item['number'] = msg[1]
        else:
            item['region'] = msg[0]
            item['experience'] = msg[1]
            item['education'] = msg[2]
            item['number'] = msg[3]
        item['Salary'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()').extract()[0]
        item['jobmessage'] = response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div//text()').extract()
        item['companymessage'] =response.xpath('/html/body/div[3]/div[2]/div[3]/div[3]/div/text()').extract()
        item['page'] = str(response.meta['page'])
        yield item



