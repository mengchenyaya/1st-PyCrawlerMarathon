# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
import json


class PttcrawlerSpider(scrapy.Spider):
    
    name = 'Pttcrawler'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/NBA/M.1577677835.A.2E0.html']
    cookies = {'over18': '1'}
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,cookies=self.cookies,callback=self.parse)

    def parse(self, resp):
           
        #check status
        if resp.status != 200:
            print(f'ERROR in {resp.url}')
            return None  
        
        #author/title/date
        try:
         author,title,date = resp.selector.css('div.article-metaline>span.article-meta-value::text').getall()
        except : 
            author = ''
            title = ''
            date = ''       
            
        #ip
        try:
            ip = resp.selector.css('span.f2').re('(\d+\.\d+\.\d+\.\d+)')[0]
        except :
            ip = ''
            
            
        #article content
        contents = resp.selector.css('div#main-content::text').getall()
        content = ''
        for c in contents:
            c.strip(' \t\n\r')
            content += c
 
        p, b, n = 0, 0, 0
        messages = []
        
        pushes = resp.selector.css("div.push")
        for push in pushes:
            # 假如留言段落沒有 push-tag 就跳過
            if not push.css('span.push-tag'):
                continue
            
            
            # comment >> tag/id/content/date
            push_tag = push.css('span.push-tag::text').get().strip(' \t\n\r')
            push_userid = push.css('span.push-userid::text').get().strip(' \t\n\r')
            push_content = ''.join(push.css('span.push-content::text').getall()[:]).strip(': ')
            push_ipdatetime = push.css('span.push-ipdatetime::text').get().strip(' \t\n\r')

            # 整理打包留言的資訊, 並統計推噓文數量
            messages.append({
                'push_tag': push_tag,
                'push_userid': push_userid,
                'push_content': push_content,
                'push_ipdatetime': push_ipdatetime})
    
            if push_tag == u'推':
                p += 1
            elif push_tag == u'噓':
                b += 1
            else:
                n += 1
        
        
        # total nums of comments
        message_count = {'all': p+b+n, 'count': p-b, 'push': p, 'boo': b, 'neutral': n}
        
        # main data   
        data = {
            'url': resp.url,
            'article_author': author,
            'article_title': title,
            'article_date': date,
            'article_content': content,
            'ip': ip,
            'message_count': message_count,
            'messages': messages
        }

        
        yield data
