#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:Paul J
from __future__ import unicode_literals
from robot.api import logger
from Automation.base.db import db
from datetime import timedelta, datetime
from Automation.utils.util import *
from Automation.aw.Page.PageBase import PageBase

class WxwDataStatistics(PageBase):
    '''
           数据统计相关关键字
    '''
    db_name = "" 
    db_ip = ""
    db_user = ""
    db_password = ""
    
    def __init__(self, path=None, title=None):
        super(WxwDataStatistics, self).__init__()
        if path == None:
            path = abspath(__file__, '../config/DemoProjectPage/datastatistics.ini')
        if title == None:
            title = 'DATA STATISTICS'
        self.DATASTATISTICS = ConfigIni(path, title)

    def setDbInfo_DS(self, db_name, db_ip, db_user, db_password):
        '''
        - 功能：设置数据库连接信息
        - 参数：
        | db_name：数据库名  | db_ip：数据库ip | db_user：数据库用户名 | db_password：数据库密码 |
        '''
        logger.info("设置数据库连接信息")
        self.db_name = db_name
        self.db_ip = db_ip
        self.db_user = db_user
        self.db_password = db_password
        
    def insertTestRecord(self):
        '''
        - 功能：插入测试记录
        '''
        logger.info("插入测试记录")
        yesterday = datetime.today() + timedelta(-1)
        yesterday_format = yesterday.strftime('%Y-%m-%d %H:%M:%S')
        dbo = db(self.db_ip, self.db_user, self.db_password, self.db_name)
        dbo.connentDB()
        dbo.executeSQL(self.DATASTATISTICS.get_ini("SQL_INIT"), 
                      ("777", "/baidu.com","1.1.1.1", "1.1.1.1", "4", "2797", 
                       "1275064372", yesterday_format, "1", "43", "2", "1", "1", 
                       "Safari/537.36corp_android_app"))
        dbo.executeSQL(self.DATASTATISTICS.get_ini("SQL_INIT"), 
                      ("888", "/baidu.com","2.2.2.2", "2.2.2.2", "1", "911", 
                       "1275064372", yesterday_format, "1", "43", "4", "1", "1", 
                       "Safari/537.36corp_android_app"))
        dbo.executeSQL(self.DATASTATISTICS.get_ini("SQL_INIT"), 
                      ("999", "/baidu.com","3.3.3.3", "3.3.3.3", "3", "789", 
                       "1275064372", yesterday_format, "1", "43", "7", "1", "1", 
                       "Safari/537.36corp_android_app"))
        dbo.commit()
        dbo.curClose()
        dbo.connClose()

    def delTestRecord(self):
        '''
        - 功能：删除测试记录
        '''
        logger.info("删除测试记录")
        dbo = db(self.db_ip, self.db_user, self.db_password, self.db_name)
        dbo.connentDB()
        dbo.executeSQL(self.DATASTATISTICS.get_ini("SQL_DEL"), ("/baidu.com",))
        dbo.commit()
        dbo.curClose()
        dbo.connClose()

    def wxw_enterDataStatisics(self, name):
        '''
        - 功能：进入数据统计的子菜单
        - 参数：
        | name：子菜单名称  |
        '''
        logger.info("进入数据统计的子菜单：" + name)
        name_dict = {
                     u"访问报表":"MENU_ACCESS_REPORT",
                     u"访问明细":"MENU_ACCESS_DETAIL"
                     }

        if name not in name_dict.keys():
            raise TypeError("%s is a inviled prameter" % name)
        self.ums_open_wxw()
        self.click(self.DATASTATISTICS.get_ini("MENU_DATA_ANALYSIS").decode("utf-8"))
        self.click(self.DATASTATISTICS.get_ini(name_dict[name]).decode("utf-8"))
        if name == "访问报表":
            assert self.checkAccessReportPage("13", "3", "3", "1")
            self.ums_close_windows()
        
    def AccessDetail_enterAccessDetail(self, item):
        '''
        - 功能：进入访问明细的子菜单
        - 参数：
        | item：子菜单名称  |
        '''
        logger.info("进入访问明细的子菜单：" + item)
        item_dict = {
                     "频道明细":"MENU_CHANNEL_DETAIL",
                     "栏目明细":"MENU_COLUMN_DETAIL",
                     "文章明细":"MENU_PAGE_DETAIL"
                     }
        if item not in item_dict.keys():
            raise TypeError("%s is a inviled prameter" % item)
        self.click(self.DATASTATISTICS.get_ini(item_dict[item]).decode("utf-8"))
        if item == "频道明细":
            assert self.checkAccessDetailPage(item, "4", "1", "1", "1.0")
        if item == "栏目明细":
            assert self.checkAccessDetailPage(item, "7", "1", "1", "1.0")
        if item == "文章明细":
            assert self.checkAccessDetailPage(item, "2", "1", "1", "1.0")
#        self.ums_close_windows()
        
    def checkAccessReportPage(self, pv, uv, ip, avg):
        '''
        - 功能：[检查点]校验访问报表
        - 参数：
        | pv：pv数  | uv：uv数 | ip：ip数 | avg：avg数 |
        '''
        logger.info("[检查点]校验访问报表")
        now_pv = self.get_text(self.DATASTATISTICS.get_ini("ACCESS_REPORT_PV"))
        now_uv = self.get_text(self.DATASTATISTICS.get_ini("ACCESS_REPORT_UV"))
        now_ip = self.get_text(self.DATASTATISTICS.get_ini("ACCESS_REPORT_IP"))
        now_avg = self.get_text(self.DATASTATISTICS.get_ini("ACCESS_REPORT_AVG"))
        if now_pv >= pv and now_uv == uv and now_ip == ip and now_avg == avg:
            logger.info("检查点成功")
            return True
        else:
            logger.info("检查点失败")
            return False
        
    def checkAccessDetailPage(self, item, pv, uv, ip, avg):
        '''
        - 功能：[检查点]校验访问报表
        - 参数：
        | item：当前页面  | pv：pv数  | uv：uv数 | ip：ip数 | avg：avg数 |
        '''
        logger.info("[检查点]校验访问明细")
        item_dict = {
                     "频道明细":"menu_channel_detail",
                     "栏目明细":"menu_column_detail",
                     "文章明细":"menu_page_detail"
                     }
        if item not in item_dict.keys():
            raise TypeError("%s is a inviled prameter" % item)
        if item in ["频道明细", "文章明细"]:
            now_pv = self.get_text(self.DATASTATISTICS.get_ini("ACCESS_DETAIL_PV"))
            now_uv = self.get_text(self.DATASTATISTICS.get_ini("ACCESS_DETAIL_UV"))
            now_ip = self.get_text(self.DATASTATISTICS.get_ini("ACCESS_DETAIL_IP"))
            now_avg = self.get_text(self.DATASTATISTICS.get_ini("ACCESS_DETAIL_AVG"))
            if now_pv >= pv and now_uv == uv and now_ip == ip and now_avg == avg:
                logger.info("检查点成功")
                return True
            else:
                logger.info("检查点失败")
                return False
        if item == "栏目明细":
            now_pv = self.get_text(self.DATASTATISTICS.get_ini("COLUMN_DETAIL_PV"))
            now_uv = self.get_text(self.DATASTATISTICS.get_ini("COLUMN_DETAIL_UV"))
            now_ip = self.get_text(self.DATASTATISTICS.get_ini("COLUMN_DETAIL_IP"))
            now_avg = self.get_text(self.DATASTATISTICS.get_ini("COLUMN_DETAIL_AVG"))
            if now_pv == pv and now_uv == uv and now_ip == ip and now_avg == avg:
                logger.info("检查点成功")
                return True
            else:
                logger.info("检查点失败")
                return False
