#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:41:05 2020

@author: mengchen
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    target_urls = [
        'https://www.ptt.cc/bbs/NBA/M.1577677835.A.2E0.html',
        'https://www.ptt.cc/bbs/NBA/M.1580442396.A.69D.html',
        'https://www.ptt.cc/bbs/NBA/M.1580443584.A.970.html',
    ] #欲爬url
    
    process = CrawlerProcess(get_project_settings()) #取得專案的全局設定
    process.crawl('Pttcrawler', start_urls=target_urls, filename='NBA')
    process.start()

if __name__ == '__main__': #執行 main.py
    main()
