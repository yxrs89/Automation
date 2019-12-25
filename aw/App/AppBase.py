#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from robot.api import logger
from Automation.base.app import app
from Automation.utils.util import *
from Automation.utils.adbUtils import *

class AppBase(app):
    
    def __init__(self, path=None, title=None):
        super(AppBase, self).__init__()
        if path == None:
            path = abspath(__file__,'config/common.ini')
        if title == None:
            title = 'APP COMMON'
        self.APP_COMMON = ConfigIni(path, title)


    def installUmsApp(self, package_name):
        '''
        - 功能：安装一信通apk
        - 参数：
        | package_name：包名  |
        '''
        apk_path = abspath(__file__, '../../resource/apk/umsapp.apk')
        adb = ADB()
        if not adb.is_install(package_name):
            logger.info("开始安装一信通App，请等待……")
            os.system("adb install \"" + apk_path + "\"")
            if adb.is_install(package_name):
                logger.info("一信通安装成功")
            else:
                logger.info("一信通安装失败")
        else:
            logger.info("一信通已安装，清除用户数据")
            self.cleanAppData(package_name)
            time.sleep(3)

    def WeChat_enterOfficialAccounts(self, name):
        '''
        - 功能：进入指定的微信公众号
        - 参数：
        | name：微信公众号名称  |
        '''
        self.Mobile_Click_Text_Button("通讯录")
        self.Mobile_Click_Text_Button("公众号")
        if self.find_element("xpath=//*[@text='%s']" % name):
            self.Mobile_Click_Text_Button(name)
        else:
            self._info("公众号：" + name + " 未找到，下滑去找")
            count = 0
            while count < 13:
                self.Swipe_To_Up    ()
                if self.find_element("xpath=//*[@text='%s']" % name):
                    self._info("找到了")
                    self.Mobile_Click_Text_Button(name)
                    break
                else:
                    self._info("还是没找到，继续下滑找")
                    count = count + 1
 
    def loginUmsApp(self, account, password):
        '''
        - 功能：一信通登录
        - 参数：
        | account：登录名称  | password：登录密码  |
        '''
        for i in range(1):
            if self.find_element("xpath=//*[@text='%s']" % self.APP_COMMON.get_ini("BTN_ALLOW_TEXT").decode("utf-8"), 1.3):
                self.Mobile_Click_Text_Button(self.APP_COMMON.get_ini("BTN_ALLOW_TEXT").decode("utf-8"))
        for i in range(4):
            self.Swipeleft_old()
            time.sleep(0.9)
        self._info("输入账号：" + account)
        self.send_keys(self.APP_COMMON.get_ini("UMS_LOGIN_ACCOUNT").decode("utf-8"), account, False, False)
        self._info("输入密码：" + password)
        self.send_keys(self.APP_COMMON.get_ini("UMS_LOGIN_PASSWORD"), password, False, False)
        self._info("点击登录按钮")
        self.find_element(self.APP_COMMON.get_ini("UMS_LOGIN_BTN")).click()
        self.wait_until_page_contains_element(self.APP_COMMON.get_ini("UMS_TITLE"), timeout=20)
        
    def UmsApp_chooseEnterprise(self, name):
        '''
        - 功能：选择企业
        - 参数：
        | name：企业名称  |
        '''
        title = self.find_element(self.APP_COMMON.get_ini("UMS_TITLE"), 20 ).text
        if title == "企业列表":
            elems = self.find_elements(self.APP_COMMON.get_ini("UMS_ENTERPRISE_LIST"))
            for item in elems:
                if name in self.Get_Attribute_By_Element(item, "name"):
                    self._info("进入企业：" + name)
                    item.click()
                    for i in range(2):
                        if self.find_element("xpath=//*[@text='%s']" % self.APP_COMMON.get_ini("BTN_ALLOW_TEXT").decode("utf-8"), 1.5):
                            self.Mobile_Click_Text_Button(self.APP_COMMON.get_ini("BTN_ALLOW_TEXT").decode("utf-8"))
                    self.wait_until_page_contains_element(self.APP_COMMON.get_ini("UMS_WORK_LIST"), timeout=15)
                    break
            time.sleep(2)
        elif title == "工作台":
            self._info("已经选择过企业，无需再次选择")
            self.wait_until_page_contains_element(self.APP_COMMON.get_ini("UMS_WORK_LIST"), timeout=15)
        else:
            self._info("其他页面，请确认：" + title)
        
    def WorkPlatform_enterProgram(self, name):
        '''
        - 功能：从工作台进入项目
        - 参数：
        | name：项目名称  |
        '''
        elems = self.find_elements(self.APP_COMMON.get_ini("UMS_WORK_LIST"))
        for item in elems:
            if name in self.Get_Attribute_By_Element(item, "name"):
                self._info("进入项目：" + name)
                item.click()
                self.wait_until_page_contains_element(self.APP_COMMON.get_ini("MNEWS_PAGE_LIST"), timeout=20)
                time.sleep(3)
                return
        self._info("工作台未找到项目：" + name)
        
    def checkUmsAppLogin(self):
        '''
        - 功能：[检查点]检查一信通是否登录成功
        '''
        self._info("[检查点]检查一信通是否登录成功")
        try:
            title = self.find_element(self.APP_COMMON.get_ini("UMS_TITLE"), 20 )
            if title.text in ["企业列表","工作台"]:
                self._info("登录成功")
                return True
            else:
                self._info("登录失败")
                return False
        except:
            self._info("登录失败")
            return False
    
    def checkEnterPage(self, page_name):
        '''
        - 功能：[检查点]检查一信通是否登录成功
        '''
        self._info("[检查点]检查一信通是否登录成功")
        title = self.find_element(self.APP_COMMON.get_ini("UMS_TITLE"), 20 )
        result = self.Mobile_Get_Elements_Num(self.APP_COMMON.get_ini("UMS_MENU_LIST"))
        if title.text == page_name and result > 0:
            self._info("切换企业成功")
            return True
        else:
            self._info("切换企业失败")
            return False

if __name__ == '__main__':
    pass