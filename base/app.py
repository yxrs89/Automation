#!/usr/bin/env python
# coding=utf-8
#Author:Paul J,Paul J
#Verson:3.0.0
from __future__ import print_function
from __future__ import unicode_literals
from appium.webdriver.common.touch_action import TouchAction
from robot.libraries.Screenshot import Screenshot
from Automation.utils.appUtils import *
from Automation.utils.util import *
from Automation.base.page import page
import os

class app(page):

    TIMEOUT = 30 #超时时间
    POLL_FREQUENCY = 0.05 #超时时间内的检查间隔

    def __init__(self):
        super(app, self).__init__()
        self.driver = None

    def open_app(self,app_name,**kwargs):
        '''
        - 功能：安装APP->启动Appium->启动APP
        - 参数如下：
        - app_name:应用安装包文件名（不带文件后缀）
        - noReset(可选)：不要在会话前重置应用状态,默认值为false
        - unicodeKeyboard(可选)：使用 Unicode 输入法。默认值false
        - resetKeyboard(可选)：设定了 unicodeKeyboard 关键字的 Unicode 测试结束后，重置输入法到原有状态。如果单独使用，将会被忽略，默认false
        - newCommandTimeout(可选)：设置命令超时时间，单位：秒。达到超时时间仍未接收到新的命令时 Appium 会假设客户端退出然后自动结束会话，默认300秒
        - sessionOverride（可选）: 每次启动允许会话覆盖，默认为true
        - RobotFramwork脚本写法示例如下：
        | open_app | testapp  |
        '''

        logger.info("#####当前操作：手机自动化初始化操作#####")
        #检查环境是否安装appium
        check_environment()
        #初始化设备及APP相关路径信息
        initialization_arrangement_case(app_name)
        #获取APP相关信息写入配置文件
        desired_capabilities = kwargs
        set_app_yaml(desired_capabilities)
        device_name = None
        if 'device_name' in desired_capabilities and desired_capabilities['device_name'] !='':
            device_name = desired_capabilities['device_name']
        set_device_yaml(device_name)
        #获取所需执行的设备信息
        device_arg = get_device_info()
        self.run_app = RunApp(device_arg)
        self.run_app.install_app()
        #启动appium
        self.driver = self.run_app.start_appium()


    def lock(self,secs=5):
        '''
        - 锁定屏幕（默认5秒，仅支持IOS）
        - 如：driver.lock(5)
        - RobotFramwork脚本写法示例如下：
        | lock | 5 |
        :param duration:
        '''
        self.driver.lock(secs)

    def background_app(self,secs):
        '''
        - 将应用切换至后台
        - 如：
        driver.background_app(5)  # 置于后台，持续5秒
        driver.background_app(-1) # 持续置于后台
        driver.background_app({'timeout': None}) # 持续置于后台
        - RobotFramwork脚本写法示例如下：
        | background_app | 5 |
        :param secs:
        '''
        self.driver.background_app(secs)

    def hide_keyboard(self):
        '''
        - 收起键盘
        - 如：driver.hide_keyboard()
        - RobotFramwork脚本写法示例如下：
        | hide_keyboard |
        '''
        self.driver.hide_keyboard()

    def start_activity(self,app_package, app_activity):
        '''
        - 启动 Activity(仅支持Android)
        - app_package:包名
        - app_activity:包activity
        - 如：driver.start_activity('com.example.android.apis', '.Foo')
        - RobotFramwork脚本写法示例如下：
        | start_activity | om.example.android.apis | .Foo |
        '''
        self.driver.start_activity(app_package, app_activity)

    def open_notifications(self):
        '''
        - 打开通知栏(仅支持Android)
        - 如：driver.open_notifications()
        - RobotFramwork脚本写法示例如下：
        | open_notifications |
        '''
        self.driver.open_notifications()

    def is_app_installed(self,bundle_id):
        '''
        - 应用是否已安装
        - bundle_id：应用ID
        - 如：driver.is_app_installed('com.example.android.apis')
        - RobotFramwork脚本写法示例如下：
        | is_app_installed | com.example.android.apis |
        '''
        self.driver.is_app_installed(bundle_id)

    def install_app(self,app_path):
        '''
        - 安装应用
        - app_path：APP路径
        - 如：driver.install_app('path/to/my.apk')
        - RobotFramwork脚本写法示例如下：
        | install_app | path/to/my.apk |
        '''
        self.driver.install_app(app_path)

    def shake(self):
        '''
        - 摇一摇
        - 如：driver.shake()
        - RobotFramwork脚本写法示例如下：
        | shake |
        '''
        self.driver.shake()

    def close_app(self):
        '''
        - 关闭应用
        - 如：driver.close_app();
        - RobotFramwork脚本写法示例如下：
        | close_app |
        :return:
        '''
        self.driver.close_app()

    def launch_app(self):
        '''
        - 启动应用
        - 注：配合desired capability中设置autoLaunch=false使用
        - 这个方法的使用场景是在你设置了 autoLaunch=false 后，用来继续执行初始化（"launch"）流程的。（译者注：举个例子，国产系统经常会在应用安装时弹出提示窗阻碍安装，此时可以通过 autoLaunch=false 来让应用安装后先执行你的脚本来关掉弹窗，然后再用这个函数来继续启动应用。）
        - 如：driver.launch_app()
        - RobotFramwork脚本写法示例如下：
        | launch_app |
        '''
        self.driver.launch_app()

    def reset(self):
        '''
        - 重置应用（清除缓存）
        - 如：driver.reset()
        - RobotFramwork脚本写法示例如下：
        | reset |
        '''
        self.driver.reset()

    def contexts(self):
        '''
        - 列出所有可用上下文
        - 如：driver.contexts
        - RobotFramwork脚本写法示例如下：
        | contexts |
        '''
        self.driver.contexts()

    def current_context(self):
        '''
        - 当前的上下文
        - 如：driver.current_context
        - RobotFramwork脚本写法示例如下：
        | current_context |
        '''
        self.driver.current_context()

    def switch_default_context(self):
        '''
        - 切换至默认的上下文
        - RobotFramwork脚本写法示例如下：
        | switch_default_context |
        :return:
        '''
        self.driver.switch_to.context(None)

    def app_strings(self):
        '''
        - 获得应用的字符串(这里实际指的是返回应用的多语言文本，即每个 string 变量及在指定语言上的显示内容。例如 {"action_forgot_password":"Forgot your password?"})
        - 如：driver.app_strings
        - RobotFramwork脚本写法示例如下：
        | app_strings |
        '''
        self.driver.app_strings()

    def send_key_event(self, arg):
        '''
        - 参考文献：http://blog.csdn.net/jlminghui/article/details/39268419
        - 操作实体按键
        - 如 driver.keyevent('entity_home')
        - RobotFramwork脚本写法示例如下：
        | app_strings |
        '''
        event_list = {'entity_home': 3, 'entity_back': 4, 'entity_menu': 82, 'entity_volume_up': 24,
                      'entity_volume_down': 25, "entity_enter": 66}
        if arg in event_list:
            self.driver.keyevent(int(event_list[arg]))

    def current_activity(self):
        '''
        - 当前Activity（仅支持Android）
        - 如：driver.current_activity
        - RobotFramwork脚本写法示例如下：
        | current_activity |
        '''
        self.driver.current_activity()

    def current_package(self):
        '''
        - 当前包名
        - 如：driver.current_package
        - RobotFramwork脚本写法示例如下：
        | current_package |
        '''
        self.driver.current_package()

    def action_press(self,x=None,y=None,locator=None,secs=TIMEOUT):
        '''
        - 坐标点击操作
        - x:x轴
        - y:y轴
        - RobotFramwork脚本写法示例如下：
        | action_press | 110 | 119 | xpath=>div[text()='测试'] |
        '''
        el = None
        if locator is not None:
            el = self.get_element(locator, secs)
        action = TouchAction(self.driver)
        action.press(el=el,x=x,y=y).release().perform()

    def swipe(self, slocation, elocation,duration=900):
        """
        - 滑动操作
        - 分别为:起始点x,y。结束点x,y。与滑动速度。滑动默认900
        - 将slocation和elocation以逗号进行1次分割
        - RobotFramwork脚本写法示例如下：
        | swipe | 110，120 | 119，122 |
        """
        sx, sy = slocation.split(',', 1)
        ex, ey = elocation.split(',', 1)
        self.driver.swipe(sx, sy, ex, ey, duration)

    def swipe_ratio(self,sx,sy,ex,ey):
        '''
        - 按比例滑动
        - sx:起始X轴比例
        - sy:起始Y轴比例
        - ex:结束X轴比例
        - ey:结束Y轴比例
        - RobotFramwork脚本写法示例如下：
        | swipe_ratio | 0.8 | 0.5 | 0.2 | 0.5 |
        '''
        width, height = self.get_window_size()
        self.swipe("%s,%s"%(str(sx * width), str(sy * height)),"%s,%s"%(str(ex * width), str(ey * height)))

    def swipe_left(self):
        '''
        - 页面左滑
        - RobotFramwork脚本写法示例如下：
        | swipe_left |
        '''
        self.swipe_ratio(0.8, 0.5, 0.2, 0.5)
        time.sleep(1)

    def swipe_right(self):
        '''
        - 页面右滑
        - RobotFramwork脚本写法示例如下：
        | swipe_right |
        '''
        self.swipe_ratio(0.2, 0.5, 0.8, 0.5)
        time.sleep(1)

    def swipe_up(self):
        '''
        - 上滑屏幕
        - RobotFramwork脚本写法示例如下：
        | swipe_up |
        '''
        self.swipe_ratio(0.5, 0.8, 0.5, 0.2)
        time.sleep(1)

    def swipe_down(self):
        '''
        - 下滑屏幕
        - RobotFramwork脚本写法示例如下：
        | swipe_down |
        '''
        self.swipe_ratio(0.5, 0.2, 0.5, 0.8)
        time.sleep(1)

    def pinch(self,locator,percent=200,steps=50,secs=TIMEOUT):
        '''
        - 捏手势
        - locator : 位置
        - percent（可选）: 放大百分比
        - steps（可选）：操作步数
        - RobotFramwork脚本写法示例如下：
        | pinch | 200 | 50 |
        '''
        el = self.get_element(locator, secs)
        self.driver.pinch(element=el,percent=percent,steps=steps)

    def zoom(self,locator,percent=200,steps=50,secs=TIMEOUT):
        '''
        - 放大屏幕
        - locator: 位置
        - percent（可选）: 放大百分比
        - steps（可选）：操作步数
        - RobotFramwork脚本写法示例如下：
        | zoom | xpath=>//div[text()='测试'] | 200 | 50 |
        '''
        el = self.get_element(locator,secs)
        self.driver.zoom(element=el,percent=percent,steps=steps)

    def scroll_element(self,locator,secs=TIMEOUT):
        '''
        - 滚动到指定元素
        - locator: 位置
        - secs: 超时时间
        - RobotFramwork脚本写法示例如下：
        | scroll_element | xpath=>//div[text()='测试'] |
        '''
        el = self.get_element(locator,secs)
        self.driver.execute_script("mobile:scroll",{"direction": "down", "element": el.id})

    def pull_file(self,path):
        '''
        - 拉取设备上的文件
        - path：文件路径
        - 如：driver.pull_file('Library/AddressBook/AddressBook.sqlitedb')
        - RobotFramwork脚本写法示例如下：
        | pull_file | Library/AddressBook/AddressBook.sqlitedb |
        '''
        self.driver.pull_file(path)

    def push_file(self,path,data):
        '''
        - 推送文件到设备上
        - path：预期推送到设备文件（所需写入文件）
        - 如：driver.push_file(path, data.encode('base64'))
        - RobotFramwork脚本写法示例如下：
        | pull_file | file.txt | data.encode('base64') |
        '''
        self.driver.push_file(path,data.encode('base64'))

    def update_settings(self,setting,setting_value):
        '''
        - appium服务器设置
        - setting: 具体详见http://appium.io/docs/en/advanced-concepts/settings/index.html
        - setting_value: True or False
        - RobotFramwork脚本写法示例如下：
        | update_settings | ignoreUnimportantViews | True |
        '''
        self.driver.update_settings({setting: setting_value})

    def get_window_size(self):
        """
        - 获取屏幕分辨率宽和高
        - {u'width': 1080, u'height': 1920}
        - RobotFramwork脚本写法示例如下：
        | get_window_size |
        """
        screen_size = self.driver.get_window_size()
        width = screen_size['width']
        height = screen_size['height']
        return width, height

    def toggle_location_services(self):
        """
        - 开关定位服务
        - RobotFramwork脚本写法示例如下：
        | toggle_location_services |
        """
        self.driver.toggle_location_services()

    def long_press(self, locator,duration,secs=TIMEOUT):
        """
        - 长按按钮事件
        - locator:元素位置
        - duration：持续时长（秒）
        - RobotFramwork脚本写法示例如下：
        | long_press | xpath=>//button[text()='测试'] | 1 |
        """
        el = self.get_element(locator,secs)
        elx = el.location.get('x')
        ely = el.location.get('y')
        self.driver.tap([(elx,ely)], duration*1000)

    def save_screenshot(self, file_path):
        """
        - 获取android设备截图
        - file_path: 文件保存路径
        - RobotFramwork脚本写法示例如下：
        | save_screenshot | d:/test.jpg |
        """
        self.driver.save_screenshot(file_path)

    def clear_process(self):
        '''
        - 清除appium进程
        - RobotFramwork脚本写法示例如下：
        | clear_process |
        '''
        self.run_app.clear_process()

    def clean_process_all(self):
        '''
        - 清楚所有进程
        - RobotFramwork脚本写法示例如下：
        | clean_process_all |
        '''
        cl = Cp()
        cl.clean_process_all()

    def clean_appium_node(self):
        '''
        - 关闭appium服务
        - RobotFramwork脚本写法示例如下：
        | clean_appium_node |
        '''
        self.run_app.kill_appiumServer()

    def Switch_to_WebView_or_App(self, context):
        '''
        - 切换到webview
        - RobotFramwork脚本写法示例如下：
        | Switch_to_WebView_or_App | context-1 |
        '''
        if context in self.driver.contexts:
            try:
                logger.info("当前context-" + self.driver.current_context + " 要转换的context-" + context)
                init_content = self.driver.current_context
                if self.driver.current_context != context:
                    self.driver.switch_to.context(context)
                    logger.info("转换过后的context：" + self.driver.current_context)
                    logger.info("转换后的页面代码：")
                    logger.info(self.driver.page_source)
                else:
                    logger.info("context相同，无需转换")
                return init_content
            except:
                logger.info("The current state is trying to %s" % context)
        else:
            raise TypeError(context + "不在contexts中")

    def reSwitchToWebview(self, context):
        '''
        - 重新切换webview
        - RobotFramwork脚本写法示例如下：
        | reSwitchToWebview | context-2 |
        '''
        self.Switch_to_WebView_or_App("NATIVE_APP") 
        self.Switch_to_WebView_or_App(context)

    def get_app_img_robot(self, file_path, name="screenshot",width="500px"):
        '''
        - 功能： 获取当前浏览器截图，如果截图失败，自动进行windows下截图，并将结果插入到robot结果报告中
        - 参数如下：
        - file_path：截图路径
        - name(可选): 图片基础文件名，如name=pic,后续生成图片将以此pic1、pic2、pic3……
        - width（可选）：图片宽度，默认为800px
        - RobotFramwork脚本写法示例如下：
        | get_windows_app_robot | D:/Screenshots/ | name="screenshot" | width="800px" |
        '''
        try:
            self.screenshot = Screenshot()
            path = self.screenshot._get_screenshot_path(name,file_path)
            self.save_screenshot(path)
            self.screenshot._embed_screenshot(path,width)
        except:
            logger.info("截图失败")

    def click_point(self, locator, index=1, secs=TIMEOUT):
        '''
        - 计算元素坐标并点击（只支持原生元素）
        - RobotFramwork脚本写法示例如下：
        | click_point | xpath=>//div[text()='测试'] | 1 |
        '''
        el = self.get_elements(locator,secs)[index - 1]
        dx = el.location.get('x')
        dy = el.location.get('y')
        logger.info("adb shell input tap " + str(dx) + " " + str(dy))
        os.popen("adb shell input tap " + str(dx) + " " + str(dy))
        time.sleep(0.5)

    def tap(self, locator, secs=TIMEOUT):
        '''
        - webview模式下，tap方式点击
        - RobotFramwork脚本写法示例如下：
        | tap | xpath=>//div[text()='测试'] |
        '''
        elem = self.get_element(locator, secs)
        logger.info("tap click：" + locator)
        self.driver.execute_script("arguments[0].dispatchEvent(new CustomEvent('tap', {detail: {},bubbles: true,cancelable: true}));", elem)

    def webviewTouchText(self, text, context=None, index=1, secs=TIMEOUT):
        '''
        - webview模式下，点击文字
        - text-需要点击的文字
        - index-第几个文字，默认1
        - context-点击完毕切回webview的名字，不切回则None
        - RobotFramwork脚本写法示例如下：
        | webviewTouchText | 测试测试文字 | 1 |
        '''
        self.Switch_to_WebView_or_App("NATIVE_APP")
        self.click_point("xpath=>//*[contains(@text,'%s') or contains(@content-desc,'%s')]" % (text, text), index)
        if context is not None:
            logger.info("需要切回webview")
            self.Switch_to_WebView_or_App(context)
