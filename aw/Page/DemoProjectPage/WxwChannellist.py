#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from time import sleep
from Automation.utils.util import *
from Automation.aw.Page.PageBase import PageBase


class WxwChannellist(PageBase):
    
    def __init__(self, path=None, title=None):
        super(WxwChannellist, self).__init__()
        if path == None:
            path = abspath(__file__,'../config/DemoProjectPage/channellist.ini')
        if title == None:
            title = 'channellist'
        self.channellist = ConfigIni(path, title)

    def wxw_channel_add(self,channel_name):
        '''
        -事件：微新闻频道新增事件
        -参数：
        | channel_name:新增频道名称 |
        '''
        self.ums_open_wxw()
        self.element_clickable(self.channellist.get_ini("channel_add")).click()
        # self.click(self.channellist.get_ini("channel_add"))
        self.type(self.channellist.get_ini("channel_name"),channel_name)
        self.click(self.channellist.get_ini("channel_name_confirm"))
        self.click(self.channellist.get_ini("channel_name_ok"))
        assert self.element_present(self.channellist.get_ini("channel_add_check"))

    def wxw_channel_mod(self,channel_name,channel_mod_name):
        '''
        -事件：微新闻频道修改事件
        -参数：
        | channel_name:修改频道名称 | channel_mod_name:所修改频道名字 |
        '''
        self.ums_open_wxw()
        #标志首页是否包含所需频道名称
        home_flg = False
        #判断首页是否有所需要的频道名称
        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
        for el_channel_name in channel_name_all:
            if el_channel_name.text == channel_name:
                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[2]"%(channel_name_all.index(el_channel_name)+2))
                home_flg = True
                break
        #如果首页没有
        if not home_flg:
            other_flg = False
            #获取所有列表分页数量
            channel_changepage_all = self.get_elements(self.channellist.get_ini("channel_changepage_all"))
            if len(channel_changepage_all)>0:
                for el_channel_changepage in channel_changepage_all:
                    if not other_flg:
                        self.click(self.channellist.get_ini("channel_list_next").decode('utf-8'))
                        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
                        for el_channel_name in channel_name_all:
                            if el_channel_name.text == channel_name:
                                #查找到el_channel_name在列表中序号，然后+2，因为xpath中取元素从1开始，另外列表第一行也要排查，所以加2
                                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[2]"%(channel_name_all.index(el_channel_name)+2))
                                other_flg = True
                                break
        self.type(self.channellist.get_ini("channel_name"),channel_mod_name)
        self.click(self.channellist.get_ini("channel_name_confirm"))
        self.click(self.channellist.get_ini("channel_name_ok"))
        #获取所有频道名称
        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
        flg = False
        for el_channel_name in channel_name_all:
            if el_channel_name.text == channel_mod_name:
                flg = True
        assert flg

    def wxw_channel_del(self,channel_name):

        '''
        -事件：微新闻频道删除事件
        -参数：
        | channel_name:删除频道的名称 |
        '''
        self.ums_open_wxw()
        #标志首页是否包含所需频道名称
        home_flg = False
        #判断首页是否有所需要的频道名称
        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
        for el_channel_name in channel_name_all:
            if el_channel_name.text == channel_name:
                #判断频道是否已发布，如果已发布需要先进行下架操作
                if self.element_present("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[6]/span[text()='已发布']"%(channel_name_all.index(el_channel_name)+2),2):
                    #下架操作
                    self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[4]"%(channel_name_all.index(el_channel_name)+2))
                    self.scroll_click(self.channellist.get_ini("channel_publish_off"))
                    self.click(self.channellist.get_ini("channel_publish_offconfirm"))
                    self.click(self.channellist.get_ini("channel_publish_offok"))
                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[5]"%(channel_name_all.index(el_channel_name)+2))
                home_flg = True
                break
        #如果首页没有
        if not home_flg:
            other_flg = False
            #获取所有列表分页数量
            channel_changepage_all = self.get_elements(self.channellist.get_ini("channel_changepage_all"))
            if len(channel_changepage_all)>0:
                for el_channel_changepage in channel_changepage_all:
                    if not other_flg:
                        self.click(self.channellist.get_ini("channel_list_next").decode('utf-8'))
                        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
                        for el_channel_name in channel_name_all:
                            if el_channel_name.text == channel_name:
                                #判断频道是否已发布，如果已发布需要先进行下架操作
                                if self.element_present("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[6]/span[text()='已发布']"%(channel_name_all.index(el_channel_name)+2),2):
                                    #下架操作
                                    self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[4]"%(channel_name_all.index(el_channel_name)+2))
                                    self.scroll_click(self.channellist.get_ini("channel_publish_off"))
                                    self.click(self.channellist.get_ini("channel_publish_offconfirm"))
                                    self.click(self.channellist.get_ini("channel_publish_offok"))
                                    #查找到el_channel_name在列表中序号，然后+2，因为xpath中取元素从1开始，另外列表第一行也要排查，所以加2
                                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[5]"%(channel_name_all.index(el_channel_name)+2))
                                other_flg = True
                                break
        self.click(self.channellist.get_ini("channel_sure_delete"))
        self.click(self.channellist.get_ini("channel_name_ok"))
        #获取所有频道名称
        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
        flg = True
        for el_channel_name in channel_name_all:
            if el_channel_name.text == channel_name:
                flg = False
        assert flg

    def wxw_channel_preview(self,channel_name):
        '''
        -事件：微新闻频道预览事件
        -参数：
        | channel_name:预览频道名称 |
        '''
        self.ums_open_wxw()
        #标志首页是否包含所需频道名称
        home_flg = False
        #判断首页是否有所需要的频道名称
        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
        for el_channel_name in channel_name_all:
            if el_channel_name.text == channel_name:
                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[3]"%(channel_name_all.index(el_channel_name)+2))
                home_flg = True
        #如果首页没有
        if not home_flg:
            other_flg = False
            #获取所有列表分页数量
            channel_changepage_all = self.get_elements(self.channellist.get_ini("channel_changepage_all"))
            if len(channel_changepage_all)>0:
                for el_channel_changepage in channel_changepage_all:
                    if not other_flg:
                        self.click(self.channellist.get_ini("channel_list_next").decode('utf-8'))
                        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
                        for el_channel_name in channel_name_all:
                            if el_channel_name.text == channel_name:
                                #查找到el_channel_name在列表中序号，然后+2，因为xpath中取元素从1开始，另外列表第一行也要排查，所以加2
                                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[3]"%(channel_name_all.index(el_channel_name)+2))
                                other_flg = True
        assert self.element_present(self.channellist.get_ini("channel_preview_check").decode("utf-8"))

    def wxw_channel_publish(self,channel_name,pic_path,searchrange):
        '''
        -事件：微新闻频道发布事件
        -参数：
        | channel_name:所需发布频道名称 | pic_path:新闻LOGO地址 | searchrange：设置搜索范围名称 |
        '''
        self.ums_open_wxw()
        #标志首页是否包含所需频道名称
        home_flg = False
        #判断首页是否有所需要的频道名称
        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
        for el_channel_name in channel_name_all:
            if el_channel_name.text == channel_name:
                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[4]"%(channel_name_all.index(el_channel_name)+2))
                home_flg = True
                break
        #如果首页没有
        if not home_flg:
            other_flg = False
            #获取所有列表分页数量
            channel_changepage_all = self.get_elements(self.channellist.get_ini("channel_changepage_all"))
            if len(channel_changepage_all)>0:
                for el_channel_changepage in channel_changepage_all:
                    if not other_flg:
                        self.click(self.channellist.get_ini("channel_list_next").decode('utf-8'))
                        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
                        for el_channel_name in channel_name_all:
                            if el_channel_name.text == channel_name:
                                #查找到el_channel_name在列表中序号，然后+2，因为xpath中取元素从1开始，另外列表第一行也要排查，所以加2
                                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[4]"%(channel_name_all.index(el_channel_name)+2))
                                other_flg = True
                                break
                    break
        self.click(self.channellist.get_ini("channel_publish_addlog"))
        self.js(self.channellist.get_ini("channel_publish_jsupload"))
        self.type(self.channellist.get_ini("channel_publish_logoinput"),pic_path)
        self.click(self.channellist.get_ini("channel_publish_logoupload"))
        if self.element_not_present(self.channellist.get_ini("channel_div_layer")):
            self.scroll_click(self.channellist.get_ini("channel_publish_setrange"))
            self.type(self.channellist.get_ini("channel_publish_searchrange"),searchrange)
            self.click(self.channellist.get_ini("channel_publish_ztreesearch"))
            self.click("xpath=>//a[@title='%s']/parent::li/span[2]"%searchrange)
            self.click(self.channellist.get_ini("channel_publish_confirm"))
            #弹出框关掉后不能立马操作否则太快可能出现button按钮不可点击，因为会有个遮盖，所以需要判断当遮盖消失的时候再进行操作
            if self.element_not_present(self.channellist.get_ini("channel_div_layer")):
                self.click(self.channellist.get_ini("channel_publish_button"))
                self.click(self.channellist.get_ini("channel_publish_ok"))
        assert self.text_present_in_element("xpath=>//*[@id='periodicalTable']/tbody/tr/td[5 and text()='%s']/parent::tr/td[6]"%channel_name,"已发布")

    def wxw_channel_list(self,channel_name):
        '''
        -事件：微新闻频道列表事件
        -参数：
        | channel_name:所需查看列表的频道名称 |
        '''
        self.ums_open_wxw()
        #标志首页是否包含所需频道名称
        home_flg = False
        #判断首页是否有所需要的频道名称
        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
        for el_channel_name in channel_name_all:
            if el_channel_name.text == channel_name:
                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[1]"%(channel_name_all.index(el_channel_name)+2))
                home_flg = True
                break
        #如果首页没有
        if not home_flg:
            other_flg = False
            #获取所有列表分页数量
            channel_changepage_all = self.get_elements(self.channellist.get_ini("channel_changepage_all"))
            if len(channel_changepage_all)>0:
                for el_channel_changepage in channel_changepage_all:
                    if not other_flg:
                        self.click(self.channellist.get_ini("channel_list_next").decode('utf-8'))
                        channel_name_all = self.get_elements(self.channellist.get_ini("channel_name_all"))
                        for el_channel_name in channel_name_all:
                            if el_channel_name.text == channel_name:
                                #查找到el_channel_name在列表中序号，然后+2，因为xpath中取元素从1开始，另外列表第一行也要排查，所以加2
                                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[7]/div/button[1]"%(channel_name_all.index(el_channel_name)+2))
                                other_flg = True
                                break
        assert self.element_present(self.channellist.get_ini("channel_list_check"))

    def wxw_channel_delall(self):
        '''
        -事件：微新闻频道删除所有频道事件
        -参数：
        | 无 |
        '''
        self.ums_open_wxw()
        #此处在element_present中添加第二个参数2秒目的，更快进行判断频道中是否还有数据以及某调频道是否是已发布的
        while self.element_present(self.channellist.get_ini("channel_delall_flag"),5):
             #判断频道是否已发布，如果已发布需要先进行下架操作
            if self.element_present("xpath=>//*[@id='periodicalTable']/tbody/tr[2]/td[6]/span[text()='已发布']",2):
                #下架操作
                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[2]/td[7]/div/button[4]")
                self.scroll_click(self.channellist.get_ini("channel_publish_off"))
                self.click(self.channellist.get_ini("channel_publish_offconfirm"))
                self.click(self.channellist.get_ini("channel_publish_offok"))
            self.click(self.channellist.get_ini("channel_delall_one"))
            self.click(self.channellist.get_ini("channel_sure_delete"))
            self.click(self.channellist.get_ini("channel_name_ok"))
        assert self.element_not_present(self.channellist.get_ini("channel_delall_flag"))


