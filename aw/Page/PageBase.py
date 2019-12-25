#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from robot.api import logger
from Automation.base.page import page
from Automation.utils.util import *
import time

class PageBase(page):
    def __init__(self, path=None, title=None):
        super(PageBase,self).__init__()
        if path == None:
            path = abspath(__file__,'config/common.ini')
        if title == None:
            title = 'common'
        self.common = ConfigIni(path, title)

    def ums_open_browser(self,browser, browserurl):
        '''
        selenium初始化driver
        browser：浏览器类型| browserurl：浏览器安装位置
        '''
        self.open_browser(browser, browserurl)
        self.max_window()

    def ums_close_browser(self):
        '''
        selenium销毁driver，并关闭浏览器
        '''
        self.quit()

    def ums_close_windows(self):
        current_window_handle = None
        while True:
            handle = self.get_all_handles()
            if len(handle) >1:
                self.switch_to_window(handle.pop())
                self.close()
            else:
                current_window_handle = handle[0]
                break
        self.switch_to_window(current_window_handle)

    def ums_login(self,url,sp_code,sp_account,sp_password):
        '''
        企业信息服务平台登录事件
        url：平台地址| sp_code:企业号｜sp_account:登录账号 |sp_password:登录密码
        '''
        self.open(url)
        self.type(self.common.get_ini("sp_code"),sp_code)
        self.type(self.common.get_ini("sp_account"),sp_account)
        self.type(self.common.get_ini("sp_password"),sp_password)
        self.click(self.common.get_ini("sp_login").decode('utf-8'))
        assert self.element_present(self.common.get_ini("wxw_title").decode('utf-8')) and self.element_present(self.common.get_ini("wlwsby_title").decode('utf-8'))

    def ums_Fastlogin(self, url, mobile, password, name):
        '''
        - 功能：快速登录
        - 参数：
        | url：平台地址  | mobile：手机号 | password：密码 | name：登陆后显示的拼音姓名 |
        '''
        logger.info("快速登录")
        self.open(url)
        self.click(self.common.get_ini("tab_fast_login"))
        self.type(self.common.get_ini("p_account"), mobile)
        self.type(self.common.get_ini("p_password"), password)
        self.click(self.common.get_ini("btn_fast_login"))
        assert self.checkIfFastLoginSuccess(name)

    def ums_changeIdentity(self, enterprise, role_type):
        '''
        - 功能：切换身份
        - 参数：
        | enterprise：切换企业  | role_type：角色类型 |
        '''
        logger.info("切换身份：企业-" + enterprise + " 角色-" + role_type)
        self.click(self.common.get_ini("main_show_name"))
        self.click(self.common.get_ini("change_identity"))
        self.click(self.common.get_ini("change_enterprise") % enterprise)
        self.click(self.common.get_ini("change_role") % role_type)
        self.click(self.common.get_ini("btn_change_ok"))
        #此处不能缺少
        time.sleep(1.5)
        self.click(self.common.get_ini("main_show_name"))
        assert self.checkIfChangeIdentitySuccess(role_type)

    def ums_open_wxw(self):
        '''
        打开微新闻工作台事件
        '''
        self.open_new_window(self.common.get_ini("wxw_title").decode("utf-8"))

    def wxw_list_inter(self,channel_name):
        '''
        微新闻频道列表事件
        channel_name:所需查看列表的频道名称
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
                                self.click("xpath=>//*[@id='periodicalTable']/tbody/tr[%d]/td[6]/div/button[1]"%(channel_name_all.index(el_channel_name)+2))
                                other_flg = True
                                break

    def checkIfFastLoginSuccess(self, name):
        '''
        - 功能：[检查点]校验快速登录是否成功
        - 参数：
        | name：登录后显示的名称  |
        '''
        logger.info("[检查点]校验快速登录是否成功")
        if self.get_text(self.common.get_ini("main_show_name")) == name + "欢迎您！":
            logger.info("快速登录成功：" + name)
            return True
        else:
            logger.info("快速登录失败：" + name)
            return False
        
    def checkIfChangeIdentitySuccess(self, role_type):
        '''
        - 功能：[检查点]校验身份切换是否成功
        - 参数：
        | role_type：角色类型  |
        '''
        logger.info("[检查点]校验身份切换是否成功")
        if self.get_text(self.common.get_ini("login_role")) == role_type:
            self.click(self.common.get_ini("main_show_name"))
            logger.info("身份切换成功至：" + role_type)
            return True
        else:
            self.click(self.common.get_ini("main_show_name"))
            logger.info("身份切换失败：" + role_type)
            return False


if __name__ == '__main__':
    run = PageBase()
    run.ums_open_browser('chrome','chromedriver')
    run.ums_login('http://6.test.ums86.com/index.jsp','610606','zc','test123')
    # run.ums_close_browser()