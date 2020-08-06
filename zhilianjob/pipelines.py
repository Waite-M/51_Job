# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import xlrd
import xlwt
from xlutils import copy
import datetime

class ZhilianjobPipeline:
    def open_spider(self, spider):
        #定义excel存储的路径
        self.path = 'D:/spider/php/'
        if not os.path.exists(self.path):
            os.makedirs(self.path,0o777)
        self.file = self.path + str(datetime.date.today()) + 'job.xls'
    def close_spider(self, spider):
        pass
    def process_item(self, item, spider):
        #文件不存在则先创建文件
        if not os.path.exists(self.file):
            wt = xlwt.Workbook()
            sheet = wt.add_sheet(item['page'])
            titlelist = ['职位','公司','地区','经验','学历','需求人数','职位信息','公司福利及信息']
            #添加字段
            row = len(sheet.get_rows())
            #获取itemlist
            listitem = self.itemlist(item)
            #同时写入字段及职位信息
            for i in range(len(titlelist)):
                sheet.write(0,i,titlelist[i])
                sheet.write(1, i,listitem[i])
            wt.save(self.file)
            print('写入成功1')
        else:
            rd = xlrd.open_workbook(self.file)
            wt = copy.copy(rd)
            #以爬取页数命名的工作表名称是否在的工作表中
            if item['page'] not in rd.sheet_names():
                sheet = wt.add_sheet(item['page'])
            else:
                sheet = wt.get_sheet(item['page'])
            titlelist = ['职位', '公司', '地区', '经验', '学历', '薪资','需求人数', '职位信息', '公司福利及信息']
            # 获取已有列数，基于该列往下写入
            row = len(sheet.get_rows())
            #获取itemlist
            listitem = self.itemlist(item)
            if row == 0:
                for i in range(len(titlelist)):
                    sheet.write(0, i, titlelist[i])
                    sheet.write(1, i, listitem[i])
            else:
                for i in range(len(titlelist)):
                    sheet.write(row, i, listitem[i])
            wt.save(self.file)
            print('写入成功2')

    # 将item字典转换为list写入
    def  itemlist(self,item):
        listitem = []
        listitem.append(item['job'])
        listitem.append(item['company'])
        listitem.append(item['region'])
        listitem.append(item['experience'])
        listitem.append(item['education'])
        listitem.append(item['Salary'])
        listitem.append(item['number'])
        listitem.append(item['jobmessage'])
        listitem.append(item['companymessage'])
        return listitem


