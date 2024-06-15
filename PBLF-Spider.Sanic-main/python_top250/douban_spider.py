#!/usr/bin/env python
# -*- coding:utf-8 -*-
# auther:youzhi
# time:2023/4/28

import requests
import re
from bs4 import BeautifulSoup
import io
import sys
import os
import json

psych = {}
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030') #改变标准输出的默认编码
for i in range(10):
    pages = 25 * i
    url = 'https://movie.douban.com/top250?start='+str(pages)
    headers = {
        'Cookie':'ll="118318"; bid=HrM482BKMCI; __utma=30149280.822541997.1681217859.1686558326.1686562827.9; __utmz=30149280.1684325598.7.5.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __gads=ID=c03f23a38469906a-22a6b5c92cdd0055:T=1681217881:RT=1686569363:S=ALNI_MbMg931FcKtHsx45VAzkUmtzBIMYw; __gpi=UID=00000bf2993f1cae:T=1681217881:RT=1686569363:S=ALNI_MZiG2a4mDopBC1h22rCb6otzdviDA; viewed="35809725_35809727_34866266_35889905"; __utmc=30149280; __utmc=223695111; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1682694463; _pk_id.100001.4cf6=26ce6f32ac06806e.1686558325.; __utma=223695111.38269168.1686558326.1686558326.1686562827.2; __utmz=223695111.1686558326.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=v5oiR48PM9CL0BKEuzFH5kQrWPPcGTK7; _vwo_uuid_v2=D845CCAE662BBA4AB110CE0CEC3EB27FA|63e67fa1171565d73f54a5cc2264e226' ,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
    }
    resp = requests.get(url, headers=headers)
    s = resp.content.decode('utf-8')
    #print(s)
    obj0 = re.compile(r'<div class="pic">.*?<em class="">(?P<id>\d+)</em>.*?<a href="(?P<url>.*?)".*?alt="(?P<name>.*?)".*?</div>', re.S)
    s1 = obj0.finditer(s)
    for it in s1:
        url1 = it.group('url')
        psych['movie_name'] = it.group('name')
        #爬取movie_id
        segments = url1.split('/')
        psych['movie_id'] = segments[-2]
        #进入子页面爬取具体信息
        headers1 = {
           'Cookie': 'll="118318"; bid=HrM482BKMCI; __utma=30149280.822541997.1681217859.1682694221.1682694492.4; __utmz=30149280.1682694492.4.3.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1682694219%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_id.100001.4cf6=f9e79381ee5f85c2.1681217878.3.1682697549.1681386503.; __utma=223695111.502929304.1681217879.1682694221.1682694492.4; __utmz=223695111.1682694492.4.3.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __yadk_uid=o1VAl23DP0NJZmV38kRzQCIDIUmRJYN3; _vwo_uuid_v2=D9C75907DC2E3D57F8F24C00E2C93D4EA|afa3bbe77a2af21c4ba299a3a4008104; __gads=ID=c03f23a38469906a-22a6b5c92cdd0055:T=1681217881:RT=1681217881:S=ALNI_MbMg931FcKtHsx45VAzkUmtzBIMYw; __gpi=UID=00000bf2993f1cae:T=1681217881:RT=1682694502:S=ALNI_MZiG2a4mDopBC1h22rCb6otzdviDA; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1681217894; viewed="35889905"; __utmc=30149280; __utmc=223695111; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1682694463; ap_v=0,6.0'.encode('utf-8').decode('latin1'),
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
        }
        resp1 = requests.get(url1, headers=headers1)
        s1 = resp1.content.decode('utf-8')
        html = BeautifulSoup(s1, 'html.parser')
        #print(s1)
        #爬取movie_name, movie_rating, moive_director, moive_author,
        #moive_actor ,moive_type, moive_language, movie_imbd, moive_date, moive_area
        info_str = html.find("div", {"id": "info"}).get_text()
        #print(info_str)
        psych['movie_director'] = re.search(r"导演: (.+)\n",info_str).group(1).strip()
        author = re.search(r"编剧: (.+)", info_str).group(1)
        authors_list = author.split(" / ")
        authors_top_two = authors_list[:2]
        psych['movie_author'] = authors_top_two
        actors = re.search(r"主演: (.+)", info_str).group(1)
        actors_list = actors.split(" / ")
        actors_top_two = actors_list[:2]
        psych['movie_actor'] = actors_top_two
        psych['movie_type'] = re.search(r"类型: (.+)\n", info_str).group(1).strip()
        psych['movie_language'] = re.search(r"语言: (.+)\n", info_str).group(1).strip()
        psych['movie_imbd'] = re.search(r"IMDb: (.+)\n", info_str).group(1).strip()
        psych['comment_timestamp'] = re.search(r"上映日期: (.+)\n", info_str).group(1).strip()
        psych['movie_area'] = re.search(r"制片国家/地区: (.+)\n", info_str).group(1).strip()
        #print(psych)
        #爬取comment_list
        comment_info = html.findAll('div', {'class': 'comment'})
        comment_list = []
        for comment in comment_info:
            comment_dict = {}

            comment_id_match = re.search(r'<input type="hidden" value="(\d+)"', str(comment))
            comment_content_match = re.search(r'<span class="short">(.+?)</span>', str(comment))
            comment_timestamp_match = re.search(r'<span class="comment-time" title="(.+?)">', str(comment))
            comment_rating_match = re.search(r'<span class="allstar\d+ rating" title="(.+)"></span>', str(comment))
            comment_username_match = re.search(r'<a href=".*?" class="">(.+)</a>', str(comment))
            comment_isuseful_match = re.search(r'<span class="votes vote-count">(.+)</span>', str(comment))

            if comment_id_match:
                comment_dict['comment_id'] = comment_id_match.group(1)
            if comment_content_match:
                comment_dict['comment_content'] = comment_content_match.group(1)
            if comment_timestamp_match:
                comment_dict['comment_timestamp'] = comment_timestamp_match.group(1)
            if comment_rating_match:
                comment_dict['comment_rating'] = comment_rating_match.group(1)
            if comment_username_match:
                comment_dict['comment_username'] = comment_username_match.group(1)
            if comment_isuseful_match:
                comment_dict['comment_isuseful'] = comment_isuseful_match.group(1)

            comment_list.append(comment_dict)

        psych['comment_list'] = comment_list
        file_path = './douban_spider.json'
        file_exists = os.path.isfile(file_path)

        # 如果文件已存在，则读取已有数据
        data = []
        if file_exists:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

        # 添加新的数据到列表中
        data.append(psych)

        # 将数据保存到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
