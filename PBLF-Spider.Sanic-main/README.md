# UESTC-PBLF
基于Python的数据爬取系统与可视化云服务设计代码
```
|——UESTC-PBLF-Spider.Sanic
    |——   python_top250                      #爬虫的实现
    |          |——douban_spider.json         #爬取的数据汇总
    |             douban_spider.py           #爬虫脚本
    |——   Sanic Web                          #可视化的实现
               |——analysis.py                #情感分析脚本
                   chart.py                  #词云及饼状图绘制
                   chart.pyserver.py         #web服务
                   stopword.txt              #词云垃圾词的字典


    
