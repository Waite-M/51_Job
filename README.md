# zhilianJob_Spider
# 智联招聘岗位信息的爬取
爬取智联招聘网站的岗位信息并存储到xls工作簿中
## 1. 使用教程
###   1.1 首先安装所需要用的库，re、xlrd、 xlwt、from xlutils import copy、os、from scrapy.http import HtmlResponsefrom 、from fake_useragent import UserAgent
###   1.2 spider目录下的job.py，配置爬取的岗位信息及爬取的页数
![Image text](https://github.com/Waite-M/ZhiLian_Job/blob/master/%E5%9B%BE%E7%89%87/%E7%A4%BA%E4%BE%8B%E5%9B%BE%E7%89%871.png)
###   1.3 piplines.py中定义存储的路径
![Image text](https://github.com/Waite-M/ZhiLian_Job/blob/master/%E5%9B%BE%E7%89%87/%E7%A4%BA%E4%BE%8B%E5%9B%BE%E7%89%872.png)
###   1.4 运行scrapy爬虫获取所需信息
