#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:Paul J

from __future__ import unicode_literals
#from selenium.webdriver.support.select import Select
from Automation.aw.App.AppBase import AppBase
from robot.api import logger
from Automation.utils.util import *
import time,os

class News(AppBase):
    '''
           基础设置相关关键字
    Author: Paul J
    '''
    def __init__(self, path=None, title=None):
        super(News, self).__init__()
        if path == None:
            path = abspath(__file__, '../config/DemoProjectApp/news.ini')
        if title == None:
            title = 'NEWS'
        self.APP_NEWS = ConfigIni(path, title)

    def NewsList_enterOneNews(self, title):
        '''
        - 功能：进入某个新闻详情页面
        - 参数：
        | title：标题  |
        '''
        news_list = []
        flag = 0
        #文字和多图新闻#
        elems = self.find_elements(self.APP_NEWS.get_ini("MNEWS_LIST"))
        #图文新闻#
        elems2 = self.find_elements(self.APP_NEWS.get_ini("MNEWS_LIST2"))
        if len(elems) > 0:
            news_list = news_list + elems
        if len(elems2) > 0:
            news_list = news_list + elems2
        for news in news_list:
            if title == self.Get_Attribute_By_Element(news, "name"):
                news.click()
                logger.info("进入新闻详情：" + title)
                self.wait_until_page_contains_element(self.APP_NEWS.get_ini("NEWS_DETAIL_PAGE"), timeout=10)
                break

    def checkNewsPage(self, *titles):
        '''
        - 功能：[检查点]校验微新闻列表页面
        - 参数：
        | titles：校验的标题  |
        '''
        logger.info("[检查点]校验微新闻列表页面")
        news_list = []
        flag = 0
        #文字和多图新闻#
        elems = self.find_elements(self.APP_NEWS.get_ini("MNEWS_LIST"))
        #图文新闻#
        elems2 = self.find_elements(self.APP_NEWS.get_ini("MNEWS_LIST2"))
        if len(elems) > 0:
            logger.info("存在文字新闻和多图新闻")
            news_list = news_list + elems
        if len(elems2) > 0:
            logger.info("存在图文新闻")
            news_list = news_list + elems2
        for title in titles:
            for news in news_list:
                if title == self.Get_Attribute_By_Element(news, "name"):
                    logger.info("新闻已找到-" + title)
                    flag = flag + 1
                    break
        if flag == len(titles):
            logger.info("所有新闻标题已经找到")
            return True
        else:
            logger.info("存在未找到的新闻")
            return False
        
    def checkNewsDetail(self, **checkpoint):
        '''
        - 功能：[检查点]校验微新闻详情
        - 参数：
        | checkpoint：校验检查点，字典性（可以支持源、作者）  |
        '''
        logger.info("[检查点]校验微新闻详情")
        error_list = []
        if 'title' in checkpoint and checkpoint['title'] != '':
            elem_title = self.find_element(self.APP_NEWS.get_ini("NEWS_DETAIL_TITLE"))
            title = self.Get_Attribute_By_Element(elem_title, "name")
            if title != checkpoint['title']:
                error_list.append("标题不一致")
        if "content" in checkpoint and checkpoint['content'] != '':
            elem_content = self.find_element(self.APP_NEWS.get_ini("NEWS_DETAIL_CONTENT").decode("utf-8") % checkpoint['content'])
            if elem_content == "" or elem_content is None:
                error_list.append("正文不一致")
        if len(error_list) > 0:
            for item in error_list:
                logger.info(item)
            return False
        else:
            logger.info("文章详情验证通过")
            return True
        

