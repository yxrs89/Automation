#!/usr/bin/env python
# coding=utf-8
# Author:Paul J
# Verson:3.0.0
from __future__ import unicode_literals
import os, time
from Automation.utils.util import getPythonDir, logger
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import *
from robot.libraries.Screenshot import Screenshot
from selenium.webdriver.common.keys import Keys

global_driver = None  # 修饰器所用变量


def robust(actual_do):
    '''
    修饰器方法：当页面自动化用例失败时，打印页面源码
    :param actual_do:
    :return:
    '''

    def add_robust(*args, **keyargs):
        try:
            return actual_do(*args, **keyargs)
        except Exception, e:
            logger.warn('Error execute: %s' % actual_do.__name__)
            logger.warn(e)
            try:
                pass
                # 该方法暂时关闭
                # logger.info("#####当前页面的页面源码：#####")
                # logger.info(global_driver.page_source)
                # logger.info("##########")
            except:
                pass

    return add_robust


class page(object):
    '''
    - Pyse framework for the main class, the original selenium provided by the method of the two packaging,making it easier to use.
    - 主要封装selelnium常用方法
    '''

    TIMEOUT = 10  # 超时时间
    POLL_FREQUENCY = 0.05  # 超时时间内的检查间隔

    def __init__(self):
        self.driver = None  # 初始化driver为空

    def open_browser(self, browser, browser_driver_path=None, browser_path=None, chrome_headless=False,
                     download_directory=None):
        '''
        - 功能：创建webdrivere,选择浏览器类型和浏览器地址
        - 参数如下：
        - browser:浏览器类型 如：firefox,chrome,Internet Explprer,opera,phantomjs，需下载相应driver
        - browser_driver_path(可选):浏览器对应driver的路径，如果driver已经配置到环境变量中该参数可以不填
        - chrome_headless(可选)：无浏览器模式运行
        - RobotFramwork脚本写法示例如下：
        | open_browser | chrome | C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe | True |
        '''

        # firefox浏览器
        if browser == "firefox" or browser == "ff":
            if browser_driver_path == None:
                browser_driver_path = "geckodriver"
            driver = webdriver.Firefox(executable_path=browser_driver_path)
        # chrome浏览器
        elif browser == "chrome":
            if browser_driver_path == None:
                browser_driver_path = "chromedriver"

            # 浏览器自定义配置
            options = webdriver.ChromeOptions()
            options.add_argument("disable-infobars")
            if chrome_headless:
                options.add_argument("--headless")
            # chrome浏览器路径
            if browser_path != None:
                options.binary_location = browser_path
            # 浏览器默认下载路径
            prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_directory}
            options.add_experimental_option('prefs', prefs)
            driver = webdriver.Chrome(executable_path=browser_driver_path, chrome_options=options)
        # IE浏览器
        elif browser == "internet explorer" or browser == "ie":
            if browser_driver_path == None:
                browser_driver_path = "IEDriverServer.exe"
            driver = webdriver.Ie(executable_path=browser_driver_path)
        # opera浏览器
        elif browser == "opera":
            if browser_driver_path == None:
                browser_driver_path = "operadriver.exe"
            driver = webdriver.Opera(executable_path=browser_driver_path)
        # phantomjs无GUI浏览器
        elif browser == "phantomjs":
            if browser_driver_path == None:
                browser_driver_path = "phantomjs"
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0")
            driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=browser_driver_path)
        # edge浏览器
        elif browser == 'edge':
            if browser_driver_path == None:
                browser_driver_path = "MicrosoftWebDriver.exe"
            driver = webdriver.Edge(executable_path=browser_driver_path)
        try:
            self.driver = driver
            global global_driver
            global_driver = self.driver
        except Exception:
            raise NameError(
                "#####Not found %s browser,You can enter 'ie', 'ff', 'opera', 'phantomjs', 'edge' or 'chrome'#####" % browser)

    def locator_split(self, locator):
        '''
        - 功能：将所传locator位置信息以=>分割，分解后by表示位置信息，value表示不同方式对应值
        - 位置信息包括（推荐使用Xpath）：id,name,class,tag_name,link_text,xpath,css,partial_link_text
        - 参数如下：
        - locator:位置信息
        - RobotFramwork脚本写法示例如下：
        | locator_split | id=>wxw_id |
        | locator_split | name=>微新闻 |
        | locator_split | class=>wxw_class |
        | locator_split | tag_name=>wxw_tag |
        | locator_split | link_text=>wxw/login.do |
        | locator_split | xpath=>//a[text()='wxw'] |
        | locator_split | css=>#wxw_css |
        | locator_split |  partial_link_text=>wxw_partial_link_text |
        '''
        if "=>" not in locator:
            raise NameError("##### Positioning syntax errors, lack of '=>'#####")
        by = locator.split("=>")[0]
        value = locator.split("=>")[1]
        return by, value

    def explicit_wait(self, secs=TIMEOUT, poll_frequency=POLL_FREQUENCY):
        '''
        - 功能：初始化显性等待
        - 参数如下：
        - secs(可选)：最长超时时间,默认单位秒，默认30s
        - poll_frequency(可选)：超时时间内检查间隔，默认单位秒，默认0.05s
        - RobotFramwork脚本写法示例如下：
        | explicit_wait | 60 | 0.05 |
        '''
        _wait = WebDriverWait(driver=self.driver, timeout=secs, poll_frequency=poll_frequency)
        return _wait

    def title_is(self, title):
        '''
        - 功能：判断title是否符合预期,返回结果为True或False
        - 参数如下：
        - title:标题
        - RobotFramwork脚本写法示例如下：
        | title_is | wxw_title |
        '''
        try:
            logger.info('#####标题title:%s#####' % title)
            return EC.title_is(title)(self.driver)
        except Exception, e:
            logger.error(e)

    def title_contains(self, title):
        '''
        - 功能：判断title是否包含预期字符，返回结果为True或False
        - 参数如下：标题
        - RobotFramwork脚本写法示例如下：
        | title_contains | wxw_title |
        '''
        try:
            logger.info('#####标题title:%s#####' % title)
            return EC.title_contains(title)(self.driver)
        except Exception, e:
            logger.error(e)

    # @robust
    get_element_success_flag = 0

    def get_element(self, locator, secs=TIMEOUT):
        '''
        - 功能：获取某个元素(会一直等待元素出现，限定时间内不出现视为找不到）
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | get_element | xpath=>//a[text()='wxw'] | secs=60 |
        '''
        logger.info("##### get element:" + locator + ' #####')
        self.get_element_success_flag = 0
        element = None

        def __get_element_inner(locator, secs):
            WebDriverWait(self.driver, 5, 1).until(EC.presence_of_element_located((self.locator_split(locator))))
            element = self.explicit_wait(secs).until(EC.visibility_of_element_located(self.locator_split(locator)))
            element.location
            return element

        try:
            element = __get_element_inner(locator, secs)
            return element
        except:
            self.get_element_success_flag = 1
            count = 0
            t0 = time.time()
            t1 = time.time()
            while self.get_element_success_flag == 1 and t1 - t0 < secs:
                logger.info("#####Retry get element-%d----%s: #####" % (count, locator))
                try:
                    element = __get_element_inner(locator, secs)
                    # 成功，退出
                    self.get_element_success_flag = 0
                    logger.info("##### Retry get element succcess! #####")
                    return element
                    # break
                except Exception, e:
                    # 失败，继续
                    logger.warn(e)
                    self.get_element_success_flag = 1
                    count = count + 1
                    time.sleep(0.6)
                    t1 = time.time()
            if self.get_element_success_flag == 1 and t1 - t0 >= secs:
                raise TimeoutException("元素不可获取----%s，尝试次数-%d, 尝试耗时----%s" % (locator, count, t1 - t0))

    # @robust
    get_elements_success_flag = 0

    def get_elements(self, locator, secs=TIMEOUT):
        '''
        - 功能：获取元素集合(会一直等待元素出现，限定时间内不出现视为找不到）
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | get_elements | xpath=>//a[text()='wxw'] | secs=60 |
        '''
        logger.info("##### get elements:" + locator + ' #####')
        self.get_elements_success_flag = 0
        elements = None

        def __get_elements_inner(secs, locator):
            elements = self.explicit_wait(secs).until(EC.presence_of_all_elements_located(self.locator_split(locator)))
            # 校验是不是瞬时元素，让异常在底层抛出#
            for item in elements:
                item.location
            return elements

        try:
            elements = __get_elements_inner(secs, locator)
            return elements
        except:
            self.get_elements_success_flag = 1
            count = 0
            t0 = time.time()
            t1 = time.time()
            while self.get_elements_success_flag == 1 and t1 - t0 < secs:
                logger.info("#####Retry get element-%d----%s: #####" % (count, locator))
                try:
                    elements = __get_elements_inner(secs, locator)
                    # 成功，退出
                    self.get_elements_success_flag = 0
                    logger.info("##### Retry get elements succcess! #####")
                    return elements
                except Exception, e:
                    # 失败，继续
                    logger.warn(e)
                    self.get_elements_success_flag = 1
                    count = count + 1
                    time.sleep(0.6)
                    t1 = time.time()
            if self.get_elements_success_flag == 1 and t1 - t0 >= secs:
                raise TimeoutException("元素不可获取----%s，尝试次数-%d, 尝试耗时----%s" % (locator, count, t1 - t0))

    def element_present(self, locator, secs=TIMEOUT):
        '''
        - 功能：在限定时间内，判断某个元素是否存在，如果存在返回True，如果不存在返回False
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | element_present | xpath=>//a[text()='wxw'] | secs=60 |
        '''
        try:
            flag = self.explicit_wait(secs).until(EC.presence_of_element_located(self.locator_split(locator)))
            logger.info("#####元素----%s存在#####" % locator)
        except:
            flag = False
            logger.info('#####元素----%s在指定时间内未找到或不存在，请检查该元素是否存在！#####' % locator)
        return flag

    def element_not_present(self, locator, secs=TIMEOUT):
        '''
        - 功能：在限定时间内，检查元素是否消失（不存在），如果不存在返回True，如果存在返回False
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | element_not_present | xpath=>//a[text()='wxw'] | secs=60 |
        '''
        try:
            flag = self.explicit_wait(secs).until_not(EC.presence_of_element_located(self.locator_split(locator)))
            logger.info("#####元素----%s不存在#####" % locator)
        except:
            flag = False
            logger.info('#####元素----%s在指定时间内找到或存在，请检查该元素是否存在,判断是否正确！#####' % locator)
        return flag

    def element_located_visiable(self, locator, secs=TIMEOUT):
        '''
        - 功能：在限定时间内，检查元素是否存在且可视，如果存在且可视返回True，如果不存在或不可视返回False
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | element_located_visiable | xpath=>//a[text()='wxw'] | secs=60 |
        '''
        try:
            element = self.explicit_wait(secs).until(EC.visibility_of_element_located(self.locator_split(locator)))
            logger.info("#####元素----%s存在且可见#####" % locator)
        except:
            element = False
            logger.warn('#####元素----%s在指定时间内找到或存在，请检查该元素是否存在,判断是否正确！#####' % locator)
        return element

    def element_visiable(self, locator, secs=TIMEOUT):
        '''
        - 功能：在限定时间内，检查元素是否可视，如果可视返回True，如果不可视返回False
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | element_visiable | xpath=>//a[text()='wxw'] | secs=60 |
        '''
        try:
            element = self.explicit_wait(secs).until(EC.visibility_of(locator))
            logger.info("#####元素----%s可见#####" % locator)
        except TimeoutException:
            element = False
            logger.warn('#####元素----%s在指定时间内不可见，请检查该元素是否可见！#####' % locator)
        return element

    @robust
    def text_present_in_element(self, locator, text, secs=TIMEOUT):
        '''
        - 功能：在限定时间内判断某个元素标签中的文本之中是否存在text字符串，返回True或False
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - text: 文本信息
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | text_present_in_element | xpath=>//div[text()='wxw'] | 微新闻 | secs=60 |
        '''
        try:
            flag = self.explicit_wait(secs).until(EC.text_to_be_present_in_element(self.locator_split(locator), text))
        except TimeoutException:
            flag = False
        return flag

    @robust
    def text_present_in_element_value(self, locator, text, secs=TIMEOUT):
        '''
        - 功能：在限定时间内判断某个元素对象的value属性中是否存在text字符串，返回True或False
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - text: 文本信息
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | text_present_in_element_value | xpath=>//div[text()='wxw'] | 微新闻 | secs=60 |
        '''
        try:
            flag = self.explicit_wait(secs).until(
                EC.text_to_be_present_in_element_value(self.locator_split(locator), text))
        except TimeoutException:
            flag = False
        return flag

    @robust
    def element_clickable(self, locator, secs=TIMEOUT):
        '''
        - 功能：在限定时间内,检查元素是否可以被点击，返回element对象
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | element_clickable | xpath=>//a[text()='wxw'] | secs=60 |
        '''
        self.explicit_wait(secs).until(EC.presence_of_element_located((self.locator_split(locator))))
        element = self.explicit_wait(secs).until(EC.element_to_be_clickable(self.locator_split(locator)))
        return element

    def element_selected(self, locator, secs=TIMEOUT):
        '''
        - 功能：在限定时间内，检查元素对象是否被选中，被选中返回True,未被选中返回False
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | element_selected | xpath=>//select[text()='wxw'] | secs=60 |
        '''
        try:
            flag = self.explicit_wait(secs).until(EC.element_to_be_selected(locator))
            logger.info("#####元素----%s被选中#####" % locator)
        except Exception, e:
            flag = False
            logger.error(e)
            logger.warn('#####元素----%s在指定时间内未被选中，请检查该元素是否选中！#####' % locator)
        return flag

    def element_located_selected(self, locator, secs=TIMEOUT):
        '''
        - 功能：在限定时间内，检查元素对象是否存在并被选中，存在且选中返回True,不存在或者未被选中返回False
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | element_located_selected | xpath=>//select[text()='wxw'] | secs=60 |
        '''
        try:
            flag = self.explicit_wait(secs).until(EC.element_located_to_be_selected(self.locator_split(locator)))
            logger.info("#####元素----%s存在并选中#####" % locator)
        except Exception, e:
            flag = False
            logger.error(e)
            logger.warn('#####元素----%s在指定时间不存在或未被选中，请检查该元素是否存在或被选中！#####' % locator)
        return flag

    def alert_present(self, secs=TIMEOUT):
        '''
        - 功能：在限定时间内，检查当前页面是否存在alert值，存在返回True,不存在返回False
        - 参数如下：
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | alert_present  | secs=60 |
        '''
        try:
            alert = self.explicit_wait(secs).until(EC.alert_is_present())
            logger.info('#####查询到alert框存在！####')
            return alert
        except Exception, e:
            logger.error(e)
            logger.warn('#####在指定时间不存在弹出框提示，请检查该元素是否存在弹出框提示！#####')

    def open(self, url):
        '''
        - 功能：打开页面
        - 参数如下：
        - url:页面地址
        - RobotFramwork脚本写法示例如下：
        | open | http://www.baidu.com |
        '''
        try:
            logger.info('#####浏览器正在打开地址%s' % url)
            self.driver.get(url)
            logger.info('#####打开页面成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####页面打开失败，请检查页面地址:%s是否可以访问！#####' % url)

    def max_window(self):
        '''
        - 功能：设置浏览器最大化
        - 参数如下：
        - url:页面地址
        - RobotFramwork脚本写法示例如下：
        | max_window |
        '''
        try:
            self.driver.maximize_window()
            logger.info('#####设置浏览器最大化成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####页面最大化失败，请检查页面最大化失败原因！#####')

    def set_window(self, wide, high):
        '''
        - 功能：设置浏览器宽和高
        - 参数如下：
        - wide:宽度，单位px
        - high：高度,单位px
        - RobotFramwork脚本写法示例如下：
        | set_window | 300 | 600 |
        '''
        try:
            self.driver.set_window_size(wide, high)
            logger.info('#####设置浏览器大小成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####设置页面大小失败，请检查页面大小设置失败原因！#####')

    def type(self, locator, text, secs=TIMEOUT):
        '''
        - 功能： 页面输入操作
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - text:输入内容
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | type | xpath=>//input[text()='wxw_name'] | 张三 | secs=60 |
        '''
        self.scroll_click(locator, secs)
        try:
            logger.info("#####正在清理输入框#####")
            self.clear(locator)
            logger.info("#####type: " + locator + "   text: " + text + '#####')
            self.get_element(locator, secs).send_keys(text)
            logger.info("#####输入操作成功！#####")
        except Exception, e:
            logger.error(e)
            logger.warn('#####输入方法执行失败，请查看元素----%s是否可以找到或输入内容：%s是否合法#####' % (locator, text))

    def clear(self, locator, force=False, count=20, secs=TIMEOUT):
        '''
        - 功能： 清空操作
        - 参数如下：
        - force：是否启用强制删除模式
        - count：如果启用强制删除模式，删除次数
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | clear | xpath=>//input[text()='wxw_name'] | secs=60 |
        '''
        try:
            logger.info('#####正在执行清空操作#####')
            self.get_element(locator).clear()
            if force == True:
                elem = self.get_element(locator, 2)
                for i in range(count):
                    self.click(locator)
                    for i in range(6):
                        elem.send_keys(Keys.BACKSPACE)
            logger.info('#####清空操作成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####清空操作失败,请检查元素----%s是否存在' % locator)

    click_success_flag = 0

    def click(self, locator, secs=TIMEOUT):
        '''
        - 功能： 点击操作
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | click | xpath=>//button[text()='wxw_name'] | secs=60 |
        '''
        logger.info("#####click: " + locator + '#####')
        self.click_success_flag = 0
        try:
            self.element_clickable(locator, secs).click()
            logger.info("#####点击操作成功！#####")
        except Exception, e:
            # logger.warn(e)
            self.click_success_flag = 1
            count = 0
            # import time
            t0 = time.time()
            t1 = time.time()
            while self.click_success_flag == 1 and t1 - t0 < secs:
                logger.info("#####Retry click-%d----%s: #####" % (count, locator))
                if self.element_present(locator, 3) and self.element_located_visiable(locator, 2):
                    pass
                try:
                    self.element_clickable(locator, 2).click()
                    # 成功，退出
                    self.click_success_flag = 0
                    logger.info("##### Retry click succcess! #####")
                    break
                except Exception, e:
                    # 失败，继续
                    logger.warn(e)
                    self.click_success_flag = 1
                    count = count + 1
                    time.sleep(0.6)
                    t1 = time.time()
            if self.click_success_flag == 1 and t1 - t0 >= secs:
                raise TimeoutException("元素不可点击----%s，尝试次数-%d, 尝试耗时----%s" % (locator, count, t1 - t0))

    def scroll_click(self, locator, secs=TIMEOUT):
        '''
        - 功能： 页面自动滑动到元素可见后点击操作
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | scroll_click | xpath=>//button[text()='wxw_name'] | secs=60 |
        '''
        try:
            target = self.get_element(locator, secs)
            self.driver.execute_script("arguments[0].scrollIntoView(false);", target)
            self.click(locator, secs)
            logger.info("#####滑动点击成功！#####")
        except Exception, e:
            logger.error(e)
            logger.warn("#####滑动点击失败!请检查元素----%s是否存在#####" % locator)

    def right_click(self, locator, secs=TIMEOUT):
        '''
        - 功能： 右击操作
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | right_click | xpath=>//button[text()='wxw_name'] | secs=60 |
        '''
        try:
            el = self.element_clickable(locator, secs)
            ActionChains(self.driver).context_click(el).perform()
            logger.info("#####右击操作成功！#####")
        except Exception, e:
            logger.error(e)
            logger.warn("#####右击失败!请检查元素----%s是否存在#####" % locator)

    def select_by_value(self, locator, value, secs=TIMEOUT):
        '''
        - 功能： 通过select框value值进行选择操作
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - value：所选select框中元素的value值
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | select_by_value | xpath=>//select[text()='wxw_name'] | option2 | secs=60 |
        '''
        try:
            el = self.get_element(locator, secs)
            Select(el).select_by_value(value)
            logger.info('#####选择框选择操作成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn("#####选择框选择操作失败!请检查元素----%s是否存在或选择value值----%s是否合法#####" % (locator, value))

    def select_by_text(self, locator, text, secs=TIMEOUT):
        '''
        - 功能： 通过select框text值进行选择操作
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - text：所选select框中元素的text值
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | select_by_text | xpath=>//select[text()='wxw_name'] | 位置2 | secs=60 |
        '''
        try:
            el = self.get_element(locator, secs)
            Select(el).select_by_visible_text(text)
            logger.info('#####选择框选择操作成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####选择框选择操作失败!请检查元素----%s是否存在或选择text值----%s是否合法#####' % (locator, text))

    def move_to_element(self, locator, secs=TIMEOUT):
        '''
        - 功能： 鼠标移动至某个元素
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | move_to_element | xpath=>//button[text()='wxw_name'] | secs=60 |
        '''
        try:
            el = self.get_element(locator, secs)
            ActionChains(self.driver).move_to_element(el).perform()
            logger.info('#####鼠标移动至元素----%s操作成功！#####' % locator)
        except Exception, e:
            logger.error(e)
            logger.warn('#####鼠标移动元素失败!请检查元素----%s是否存在#####' % locator)

    def move_to_element_offset_click(self, locator, secs=TIMEOUT):
        '''
        - 功能： 鼠标移动至某个元素左击事件
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | move_to_element_offset_click | xpath=>//button[text()='wxw_name'] | secs=60 |
        '''
        try:
            el = self.get_element(locator, secs)
            ActionChains(self.driver).move_to_element(el).click().perform()
            logger.info('#####鼠标移动至元素----%s左击操作成功！#####' % locator)
        except Exception, e:
            logger.error(e)
            logger.warn('#####鼠标移动元素----%s左击失败!请检查元素是否存在#####' % locator)

    def move_to_element_offset_right_click(self, locator, dx, dy, secs=TIMEOUT):
        '''
        - 功能： 鼠标将某个元素移动到指定坐标上右击事件
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - dx:横坐标
        - dy:纵坐标
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | move_to_element_offset_right_click | xpath=>//icon[text()='wxw_name'] | 300 | 600 | secs=60 |
        '''
        try:
            el = self.element_clickable(locator, secs)
            ActionChains(self.driver).move_to_element_with_offset(el, dx, dy).context_click().perform()
            logger.info('#####鼠标移动至元素----%s移动到坐标-(%s,%s)右击操作成功！#####' % (locator, dx, dy))
        except Exception, e:
            logger.error(e)
            logger.warn('#####鼠标移动元素----%s至坐标-(%s,%s)右击失败!请检查元素是否存在#####' % (locator, dx, dy))

    def double_click(self, locator, secs=TIMEOUT):
        '''
        - 功能： 双击事件
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | double_click | xpath=>//icon[text()='wxw_name'] | secs=60 |
        '''
        try:
            el = self.element_clickable(locator, secs)
            ActionChains(self.driver).double_click(el).perform()
            logger.info('#####鼠标双击操作成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####鼠标双击操作失败，请检查元素-%是否存在！#####' % locator)

    def drag_and_drop(self, el_locator, ta_locator, secs=TIMEOUT):
        '''
        - 功能： 元素拖动事件（从源头位置拖动到目标位置）
        - 参数如下：
        - el_locator：源位置信息（建议使用Xpath方式），用法见如下表格
        - ta_locator：目标位置信息（建议使用Xpath方式），用法见如下表格
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | drag_and_drop | xpath=>//div[text()='源头'] |  xpath=>//div[text()='目标'] | secs=60 |
        '''
        try:
            el = self.element_located_visiable(el_locator, secs)
            ta = self.element_located_visiable(ta_locator, secs)
            ActionChains(self.driver).drag_and_drop(el, ta).perform()
            logger.info('#####元素拖拽事件操作成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####元素拖拽事件操作失败,请检查元素----%s和%s是否存在！#####' % (el_locator, ta_locator))

    def click_link_text(self, text):
        '''
        - 功能： 点击链接文本事件
        - 参数如下：
        - text：链接对应文本
        - RobotFramwork脚本写法示例如下：
        | click_link_text | 链接文本 |
        '''
        try:
            self.driver.find_element_by_partial_link_text(text).click()
            logger.info('#####元素点击链接文本操作成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####元素点击文本事件操作失败，请检查文本内容----%s是否合法!' % text)

    def close(self):
        '''
        - 功能： 关闭windows窗口事件
        - RobotFramwork脚本写法示例如下：
        | close |
        '''
        try:
            self.driver.close()
            logger.info('#####窗口关闭成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####窗口关闭失败!#####')

    def quit(self):
        '''
        - 功能： 销毁driver驱动事件
        - RobotFramwork脚本写法示例如下：
        | quit |
        '''
        try:
            self.driver.quit()
            logger.info('#####驱动driver销毁成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####驱动driver销毁失败！#####')

    def submit(self, locator, secs=TIMEOUT):
        '''
        - 功能： 表单提交事件
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | submit | xpath=>//form[text()='wxw_name'] | secs=60 |
        '''
        try:
            el = self.get_element(locator, secs)
            el.submit()
            logger.info('#####submit提交事件成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####submit提交事件失败,请检查元素----%s是否存在！#####' % locator)

    def F5(self):
        '''
        - 功能： 页面刷新事件
        - RobotFramwork脚本写法示例如下：
        | F5 |
        '''
        try:
            self.driver.refresh()
            logger.info('#####页面刷新事件成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn('#####页面刷新事件失败！#####')

    def js(self, script, jquery_switch=False, wait=2):
        '''
        - 功能： 执行JS脚本事件
        - 参数如下：
        - script：js语句
        - jquery_switch: jquery注入开关，默认为false,当为true时给页面注入jquery
        - wait:执行js后等待时间，默认等待2秒
        - RobotFramwork脚本写法示例如下：
        | js | window.scrollTo(200,1000); |
        '''
        try:
            import time
            if jquery_switch == True:
                self.driver.execute_script(
                    ";(function(d,s){d.body.appendChild(s=d.createElement('script')).src='http://code.jquery.com/jquery-1.9.1.min.js '})(document);")
                time.sleep(2.5)
            js = self.driver.execute_script(script)
            logger.info('#####执行js脚本成功！#####')
            time.sleep(wait)
            return js
        except Exception, e:
            logger.error(e)
            logger.warn('#####执行js脚本失败，请检查脚本----%s是否有效#####' % script)

    def get_attribute(self, locator, attribute, secs=TIMEOUT):
        '''
        - 功能： 获取元素属性事件
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - attribute: 元素属性，如type/value/name等
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | get_attribute | css=>#el | type | secs=60 |
        '''
        try:
            el = self.get_element(locator, secs)
            el_attribute = el.get_attribute(attribute)
            logger.info("#####获取元素属性成功#####")
            return el_attribute
        except Exception, e:
            logger.error(e)
            logger.info("获取元素属性失败，请检查元素----%s和属性----%s是否存在" % (locator, attribute))

    def get_text(self, locator, secs=TIMEOUT):
        '''
        - 功能： 获取元素文本事件
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | get_text | xpath=>//div[@name='gettext'] | secs=60 |
        '''
        try:
            el = self.get_element(locator, secs)
            el_text = el.text
            logger.info("#####获取元素文本事件成功!#####")
            return el_text
        except Exception, e:
            logger.error(e)
            logger.warn("#####获取元素文本事件失败，请检查元素----%s是否存在#####" % locator)

    def get_display(self, locator, secs=TIMEOUT):
        '''
        - 功能： 获取元素是否展现，返回True或False
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - secs(可选):超时时间，默认单位秒，默认时长30s
        - RobotFramwork脚本写法示例如下：
        | get_display | xpath=>//div[@name='getdisplay']  | secs=60 |
        '''
        try:
            el = self.get_element(locator, secs)
            logger.info("#####获取元素展现事件成功!#####")
            return el.is_displayed()
        except Exception, e:
            logger.error(e)
            logger.warn("#####获取元素展现事件失败，请检查元素----%s是否存在#####" % locator)

    def get_title(self):
        '''
        - 功能： 获取当前windows框的title标题值
        - RobotFramwork脚本写法示例如下：
        | get_title |
        '''
        try:
            title = self.driver.title
            logger.info("#####获取浏览器当前页title标题值成功！#####")
            return title
        except Exception, e:
            logger.error(e)
            logger.warn("#####获取浏览器当前页title标题值失败！#####")

    def get_url(self):
        '''
        - 功能： 获取当前windows框的URL地址值
        - RobotFramwork脚本写法示例如下：
        | get_url |
        '''
        try:
            current_url = self.driver.current_url
            logger.info("#####获取当前浏览器url成功！#####")
            return current_url
        except Exception, e:
            logger.error(e)
            logger.warn("#####获取当前浏览器url失败！#####")

    def get_windows_img(self, file_path):
        '''
        - 功能： 获取当前windows截图
        - 参数如下：
        - file_path：截图路径
        - RobotFramwork脚本写法示例如下：
        | get_windows_img | D:/Screenshots/foo.png |
        '''
        try:
            self.driver.get_screenshot_as_file(file_path)
            logger.info("#####截图成功，截图路径----%s#####" % file_path)
        except Exception, e:
            logger.error(e)
            logger.warn("#####截图失败，请检查截图路径----%s#####" % file_path)

    def get_windows_img_robot(self, file_path, name="screenshot", width="800px"):
        '''
        - 功能： 获取当前浏览器截图，如果截图失败，自动进行windows下截图，并将结果插入到robot结果报告中
        - 参数如下：
        - file_path：截图路径
        - name(可选): 图片基础文件名，如name=pic,后续生成图片将以此pic1、pic2、pic3……
        - width（可选）：图片宽度，默认为800px
        - RobotFramwork脚本写法示例如下：
        | get_windows_img_robot | D:/Screenshots/ | name="screenshot" | width="800px" |
        '''
        try:
            self.screenshot = Screenshot()
            path = self.screenshot._get_screenshot_path(name, file_path)
            self.get_windows_img(path)
            self.screenshot._embed_screenshot(path, width)
            logger.info("#####浏览器截图方法成功！#####")
        except:
            logger.warn("#####浏览器截图方法失败，开始使用windows截图方法！#####")
            self.screenshot.take_screenshot(name, width)

    def implicitly_wait(self, secs):
        '''
        - 功能： 隐式等待，属于全局参数，所有等待超时时间都为影视等待时间
        - 参数如下：
        - secs: 隐式等待时间，单位秒
        - RobotFramwork脚本写法示例如下：
        | implicitly_wait | 30 |
        '''
        self.driver.implicitly_wait(secs)

    def accept_alert(self):
        '''
        - 功能： 确定alert弹框事件
        - RobotFramwork脚本写法示例如下：
        | accept_alert |
        '''
        try:
            self.driver.switch_to.alert.accept()
            logger.info("#####alert弹框确定事件操作成功！#####")
        except Exception, e:
            logger.error(e)
            logger.warn("#####alert弹框确定事件操作失败！#####")

    def dismiss_alert(self):
        '''
        - 功能： 取消alert弹框事件
        - RobotFramwork脚本写法示例如下：
        | accept_alert |
        '''
        try:
            self.driver.switch_to.alert.dismiss()
            logger.info('#####alert弹框取消事件操作成功！#####')
        except Exception, e:
            logger.error(e)
            logger.warn("#####alert弹框取消事件操作成功！#####")

    def switch_to_frame(self, locator):
        '''
        - 功能： 切换到指定框架事件
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - RobotFramwork脚本写法示例如下：
        | switch_to_frame | xpath=>iframe[@id='one'] |
        '''
        try:
            by, value = self.locator_split(locator)
            _wait = self.explicit_wait(15)
            _wait.until(EC.frame_to_be_available_and_switch_to_it((by, value)))
            logger.info("#####切换到指定框架成功！#####")
        except Exception, e:
            logger.error(e)
            logger.warn("#####切换到指定框架失败，请检查框架元素----%s是否正确#####" % locator)

    def switch_to_frame_out(self):
        '''
        - 功能： 切换到最上一层默认框架
        - RobotFramwork脚本写法示例如下：
        | switch_to_frame_out |
        '''
        try:
            self.driver._switch_to.default_content()
            logger.info("#####切换到默认框架成功！#####")
        except Exception, e:
            logger.error(e)
            logger.warn("####切换到默认框架失败！#####")

    def get_all_handles(self):
        '''
        - 功能：获取windows所有的句柄，可以理解为浏览器每个tab的session
        - RobotFramwork脚本写法示例如下：
        | get_all_handles |
        '''
        try:
            window_handles = self.driver.window_handles
            logger.info("#####获取所有handle会话成功！#####")
            return window_handles
        except Exception, e:
            logger.error(e)
            logger.warn("#####获取所有handle会话失败！#####")

    def get_current_window_handle(self):
        '''
        - 功能：获取当前windows显示框的句柄，可以理解为浏览器当前tab的session
        - RobotFramwork脚本写法示例如下：
        | get_all_handles |
        '''
        try:
            current_window_handle = self.driver.current_window_handle
            logger.info("#####获取当前handle会话成功！#####")
            return current_window_handle
        except Exception, e:
            logger.error(e)
            logger.warn("#####获取当前handle会话失败！#####")

    def switch_to_window(self, window_name):
        '''
        - 功能：切换到某个window窗口会话中
        - 参数如下：
        - window_name：所需切换windows的handle值
        - RobotFramwork脚本写法示例如下：
        | switch_to_window | windows[1] |
        - 注：示例中windows[1]为windows handle对象
        '''
        try:
            self.driver._switch_to.window(window_name)
            logger.info("#####切换windows窗口会话成功！#####")
        except Exception, e:
            logger.error(e)
            logger.warn("#####切换windows窗口会话失败，请检查窗口名----%s是否存在！#####" % window_name)

    def open_new_window(self, locator):
        '''
        - 功能：点击某个元素跳转并自动切换到新的windows窗口中，适用于点击新开窗口元素
        - 参数如下：
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - RobotFramwork脚本写法示例如下：
        | open_new_window | xpath=>//a[@id='new_window'] |
        '''
        try:
            original_windows = self.driver.current_window_handle
            self.click(locator)
            all_handles = self.get_all_handles()
            for handle in all_handles:
                if handle != original_windows:
                    self.switch_to_window(handle)
            logger.info("#####在新标签页打开页面成功！#####")
        except Exception, e:
            logger.error(e)
            logger.warn("#####在新标签页打开页面失败，请检查元素----%s是否存在#####" % locator)

    def get_cookies(self):
        '''
        - 功能：获取浏览器中cookies，自动拼接成Cookie:XXXX
        - RobotFramwork脚本写法示例如下：
        | get_cookies |
        '''
        try:
            cookies_list = self.driver.get_cookies()
            Cookie = ""
            for index, item in enumerate(cookies_list):
                if "name" and "value" in item:
                    Cookie = Cookie + "%s=%s;" % (item['name'], item['value'])
            logger.info('#####获取cookie成功!#####')
            return Cookie
        except Exception, e:
            logger.error(e)
            logger.warn('#####获取cookie失败!#####')

    def get_verification_code(self, locator, file_path=None, secs=TIMEOUT):
        '''
        - 功能：验证码获取
        - 参数如下
        - locator：位置信息（建议使用Xpath方式），用法如下表格：
        | ID方式 | id=>wxw_id |
        | Name方式 | name=>微新闻 |
        | Class方式 | class=>wxw_class |
        | Tag_Name方式 | tag_name=>wxw_tag |
        | Link_Text方式 | link_text=>wxw/login.do |
        | Xpath方式 | xpath=>//a[text()='wxw'] |
        | Css方式 | css=>#wxw_css |
        | Partial_Link_Text方式 |  partial_link_text=>wxw_partial_link_text |
        - file_path: 验证码截图路径（可选），默认不填写保存至程序resource目录
        - RobotFramwork脚本写法示例如下：
        | get_verification_code | xpath=>//img[@id='codeImg'] |
        '''
        try:
            from PIL import Image
            import pytesseract
        except:
            logger.info("无PILLOW/pytesseract模块，需要联网下载")
            os.system(getPythonDir() + "/Scripts/pip install PILLOW -i https://pypi.douban.com/simple/")
            os.system(getPythonDir() + "/Scripts/pip install pytesseract -i https://pypi.douban.com/simple/")
            from PIL import Image
            import pytesseract

        if file_path == None:
            main_view = os.path.split(os.path.realpath(__file__))[0]
            main_view = main_view.replace('\\', '/')
            if 'robot' in main_view:
                main_view = main_view.replace('robot', 'Automation/base')
            file_path = main_view + '/../resource/codescreenshot.png'
        self.get_windows_img(file_path)
        element = self.get_element(locator, secs)  # 定位验证码
        location = element.location
        size = element.size
        coderange = (
            int(location['x']), int(location['y']), int(location['x'] + size['width']),
            int(location['y'] + size['height']))
        i = Image.open(file_path)
        frame4 = i.crop(coderange)
        frame4.save(file_path)
        i2 = Image.open(file_path)
        text = pytesseract.image_to_string(i2).strip()  # 使用image_to_string识别验证码
        return text

    def get_page_source(self):
        logger.info("#####################当前页面的页面源码：####################")
        logger.info(self.driver.page_source)
        logger.info("########################################################")

    def close_windows(self):
        logger.info("###### 关闭窗口 ######")
        current_window_handle = None
        while True:
            handle = self.get_all_handles()
            if len(handle) > 1:
                self.switch_to_window(handle.pop())
                self.close()
            else:
                current_window_handle = handle[0]
                break
        self.switch_to_window(current_window_handle)
