#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:Paul J
from __future__ import unicode_literals
from datetime import timedelta, datetime
from Automation.utils.util import *
from Automation.aw.Interface.InterfaceBase import InterfaceBase
from Automation.base.db import db
import base64,random,string

class ItfManager(InterfaceBase):
    '''
           门户管理接口相关关键字
    '''

    itf_headers = {"Content-type":"application/x-www-form-urlencoded;charset=UTF-8"}
    
    def __init__(self, path=None, title=None):
        super(ItfManager,self).__init__()
        if path == None:
            path = abspath(__file__, '../config/DemoProjectInterface/ItfManager.ini')
        if title == None:
            title = 'ITF URI'
        self.CONST_ITF = ConfigIni(path, title)

    def initTestDate(self, db_name, db_ip, db_user, db_password, typei, article_id):
        '''
        - 功能：插入预置数据--设置当月当周相关
        - 参数：
        | dbo类：数据库连接信息类  | type：预置信息类型 （当月、当周、总计） | article_id：文章id  |
        '''
        sid = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        dbo = db(db_ip, db_user, db_password, db_name)
        dbo.connentDB()
        if typei == "当周":
            yesterday = datetime.today() + timedelta(-1)
            yesterday_format = yesterday.strftime('%Y-%m-%d %H:%M:%S')
            dbo.executeSQL(self.CONST_ITF.get_ini("SQL_INIT"), 
                      (sid, "/magazine-wap/article/detail.do?articleId=" + article_id,"1.1.1.1", "1.1.1.1", "4", article_id, 
                       "1275064372", yesterday_format, "1", "43", "2", "1", "1", 
                       "Safari/537.36corp_android_app"))
        elif typei == "当月":
            now_month = datetime.today() + timedelta(-30)
            now_month_format = now_month.strftime('%Y-%m-%d %H:%M:%S')
            dbo.executeSQL(self.CONST_ITF.get_ini("SQL_INIT"), 
                      (sid, "/magazine-wap/article/detail.do?articleId=" + article_id,"1.1.1.1", "1.1.1.1", "4", article_id, 
                       "1275064372", now_month_format, "1", "43", "2", "1", "1", 
                       "Safari/537.36corp_android_app"))
        elif typei == "总计":
            print "暂未实现"
        else:
            raise TypeError("%s is a inviled prameter" % typei)
        dbo.commit()
        dbo.curClose()
        dbo.connClose()

    def cleanInitData(self, db_name, db_ip, db_user, db_password):
        '''
        - 功能：清除预设置数据
        - 参数：
        | dbo类：数据库连接信息类  |
        '''
        dbo = db(db_ip, db_user, db_password, db_name)
        dbo.connentDB()
        dbo.executeSQL(self.CONST_ITF.get_ini("SQL_DEL"), ("1.1.1.1",))
        dbo.commit()
        dbo.curClose()
        dbo.connClose()

    def ITF_SelectAllChannels(self, url, spid):
        '''
        - 功能：查询全部频道接口
        - 参数：
        | spid：spid  |
        '''
        #创建session#
        self.create_session("ITF1", url, self.itf_headers)
        #调接口#
        itf_result = self.get_request("ITF1", 
                                      self.CONST_ITF.get_ini("ITF_SELECT_ALL"), 
                                      params={"spId":spid}
                                      )
        #删除session#
        self.delete_all_sessions()
        #返回响应结果#
        return itf_result

    def ITF_SelectArticleByIds(self, url, *ids):
        '''
        - 功能：通过新闻id查询新闻，返回新闻结果顺序按照id传入顺序
        - 参数：
        | ids：新闻id，可多个  |
        '''
        id_param = ''
        for item in ids:
            id_param = id_param + item + ","
        #创建session#
        self.create_session("ITF2", url, self.itf_headers)
        #调接口#
        itf_result = self.get_request("ITF2", 
                                      self.CONST_ITF.get_ini("ITF_SELECT_ARTICLE_BY_ID"), 
                                      params={"ids":id_param}
                                      )
        #删除session#
        self.delete_all_sessions()
        #返回响应结果#
        return itf_result
        
    def ITF_SelectArticleByChannel(self, url, spId, periodicalId, navigationId, page, pageSize):
        '''
        - 功能：通过频道，栏目查询对应的新闻
        - 参数：
        | spId：企业编号  |periodicalId：频道编号  |navigationId：栏目编号  |
        '''
        #创建session#
        self.create_session("ITF3", url, self.itf_headers)
        #调接口#
        itf_result = self.get_request("ITF3", 
                                      self.CONST_ITF.get_ini("ITF_SELECT_ARTICLE_BY_CHANNEL"), 
                                      params={
                                              "spId":spId,
                                              "periodicalId":periodicalId,
                                              "navigationId":navigationId,
                                              "page":page,
                                              "pageSize":pageSize
                                             }
                                      )
        #删除session#
        self.delete_all_sessions()
        #返回响应结果#
        return itf_result
        
    def ITF_SetHotArticleRule(self, url, spId, flag, count):
        '''
        - 功能：热门新闻规则设置，当月，当周
        - 参数：
        | spId：企业编号  |flag：当月 ：当周 ：总计 |count：访问人数  |
        '''
        flag_dict = {
                     "当月":"1",
                     "当周":"2",
                     "总计":"3"
                     }
        if flag not in flag_dict.keys():
            raise TypeError("%s is a inviled prameter" % flag)
        #创建session#
        self.create_session("ITF4", url, self.itf_headers)
        #调接口#
        itf_result = self.get_request("ITF4", 
                                      self.CONST_ITF.get_ini("ITF_SET_HOT_ARTICLE_RULE"), 
                                      params={"spId":spId, 
                                              "flag":flag_dict[flag], 
                                              "count":count
                                              }
                                      )
        #删除session#
        self.delete_all_sessions()
        #返回响应结果#
        return itf_result
        
    def ITF_SelectColumnByChannel(self, url, parentId):
        '''
        - 功能：通过频道id查询对应的栏目
        - 参数：
        | parentId：频道id  |
        '''
        #创建session#
        self.create_session("ITF5", url, self.itf_headers)
        #调接口#
        itf_result = self.get_request("ITF5", 
                                      self.CONST_ITF.get_ini("ITF_SELECT_COLUMN_BY_CHANNEL"), 
                                      params={"parentId":parentId}
                                      )
        #删除session#
        self.delete_all_sessions()
        #返回响应结果#
        return itf_result
    
    def ITF_SelectCycleImageArticle(self, url, spId, count, **send_params):    
        '''
        - 功能：通过频道id和栏目ID查询图片新闻
        - 参数：
        | spId：企业编号  |periodicalId：频道编号  |navigationId：栏目编号  |keywords：查询文章标题中的关键词, 此字段所有字符都需要Base64处理(UTF-8)  |
        '''
        #必填参数校验#
        if spId == "" or count == "" or spId is None or count is None:
            raise ValueError("必填参数不能为空")
        #必填参数#
        params = {
                  "spId":spId,
                  "count":count    
                  }
        #获取非必填参数#
        if "periodicalId" in send_params and send_params["periodicalId"] != "":
            params["periodicalId"] = send_params["periodicalId"]
        if "navigationId" in send_params and send_params["navigationId"] != "":
            params["navigationId"] = send_params["navigationId"]
        if "pageSize" in send_params and send_params["pageSize"] != "":
            params["pageSize"] = send_params["pageSize"]
        if "keywords" in send_params and send_params["keywords"] != "":
            params["keywords"] = base64.b64encode(send_params["keywords"].encode("utf-8"))
        #创建session#
        self.create_session("ITF6", url, self.itf_headers)
        #调接口#
        itf_result = self.get_request("ITF6", 
                                      self.CONST_ITF.get_ini("ITF_SELECT_IMAGE_ARTICLE"), 
                                      params=params
                                      )
        #删除session#
        self.delete_all_sessions()
        #返回响应结果#
        return itf_result

