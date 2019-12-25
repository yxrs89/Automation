# -*- coding: utf-8 -*-
#Author:Paul J
#Verson:3.0.0
"""
@author:Paul J
@time: 18/2/05 上午9:23
"""
from __future__ import unicode_literals
import os
import random
import sys
import re
import threading
import time
import xml.etree.cElementTree as ET
import platform
import util as U
from multiprocessing import Queue
from Automation.utils import adbUtils
from appium import webdriver
from Automation.utils.util import logger
from Automation.utils.adbUtils import ADB

try:
    import yaml
except:
    logger.info("#####无pyyaml模块，需要联网下载,现在开始自动下载#####")
    os.system(U.getPythonDir() + "/Scripts/pip install pyyaml -i https://pypi.douban.com/simple/")
PATH = lambda p: os.path.abspath(p)


def set_app_yaml(desired_capabilities):
    '''
    获取APP相关配置信息写入yaml中
    :return:
    '''
    logger.info("#####Init-3：获取APP相关配置信息写入yaml中#####")
    if 'noReset' in desired_capabilities and desired_capabilities['noReset'] !='':
        noReset_value = desired_capabilities['noReset'].capitalize()
    else:
        noReset_value = False
    if 'resetKeyboard' in desired_capabilities and desired_capabilities['resetKeyboard'] !='':
        resetKeyboard_value = desired_capabilities['resetKeyboard'].capitalize()
    else:
        resetKeyboard_value = True
    if 'unicodeKeyboard' in desired_capabilities and desired_capabilities['unicodeKeyboard'] !='':
        unicodeKeyboard_value = desired_capabilities['unicodeKeyboard'].capitalize()
    else:
        unicodeKeyboard_value = True
    if 'newCommandTimeout' in desired_capabilities and desired_capabilities['newCommandTimeout'] !='':
        newCommandTimeout_value = desired_capabilities['newCommandTimeout'].capitalize()
    else:
        newCommandTimeout_value = 300
    if 'sessionOverride' in desired_capabilities and desired_capabilities['sessionOverride'] !='':
        sessionOverride_value = desired_capabilities['sessionOverride'].capitalize()
    else:
        sessionOverride_value = True
    if 'recreateChromeDriverSessions' in desired_capabilities and desired_capabilities['recreateChromeDriverSessions'] !='':
        recreateChromeDriverSessions_value = desired_capabilities['recreateChromeDriverSessions'].capitalize()
    else:
        recreateChromeDriverSessions_value = True
    app_Activity = ""
    ini = U.ConfigIni_App()
    adb = ADB()
    logger.debug('#####apk_info获取执行参数----dump badging %s#####'%ini.get_ini("test_install_path","path"))
    apk_info = adb.aapt("dump badging %s "%ini.get_ini("test_install_path","path"))
    apk_info_list = list(apk_info.readlines())
    logger.debug('#####apk_list信息----%s#####'%apk_info_list)
    app_Package = re.findall(r'\'com\w*.*?\'', apk_info_list[0])[0].replace('\'','')
    logger.info("#####app_Package----%s#####"%app_Package)
    logger.info("#####package_name----%s#####"%ini.get_ini('test_package_name', 'package_name'))
    #更改test_info.ini文件中package_name名称
    ini.set_ini("test_package_name","package_name",app_Package)
    for i in range(0,len(apk_info_list)-1):
        if 'launchable-activity' in apk_info_list[i]:
             app_Activity = re.findall(r'\'com\w*.*?\'',apk_info_list[i])[0].replace('\'','')
             logger.info("#####launchable-activity----%s#####"%app_Activity)
    app_list = [{'appPackage': app_Package, 'appActivity': app_Activity, 'appWaitActivity': app_Activity, 'unicodeKeyboard': unicodeKeyboard_value, 'resetKeyboard': resetKeyboard_value, 'noReset': noReset_value, 'newCommandTimeout': newCommandTimeout_value, 'sessionOverride': sessionOverride_value, "recreateChromeDriverSessions":recreateChromeDriverSessions_value}]
    logger.info("#####app_list信息----%s#####"%app_list)
    with open(ini.get_ini('test_info', 'info'), 'w') as f:
        yaml.dump(app_list,f)
        f.close()


def set_device_yaml(device):
    """
    获取当前设备的Android version并且保存到yaml里
    :return:
    """
    logger.info("#####Init-4：获取当前设备的Android version并且保存到yaml里#####")
    device_lst = []
    # for device in get_device():
    #     adb = adbUtils.ADB(device)
    #     logger.info(
    #         'get device:{},Android version:{}'.format(
    #             device, adb.get_android_version()))
    #     device_lst.append({'platformVersion': adb.get_android_version(
    #     ), 'deviceName': device, 'platformName': 'Android'})
    if device is None:
        device = get_device()[0]
    logger.info("#####设备device_ID----%s#####"%device)
    adb = adbUtils.ADB(device)
    logger.info(
        '#####get device:{},Android version:{}#####'.format(
            device, adb.get_android_version()))
    device_lst.append({'platformVersion': adb.get_android_version(
     ), 'deviceName': device, 'platformName': 'Android'})
    logger.info('#####设备具体信息----%s#####'%device_lst)
    ini = U.ConfigIni_App()
    with open(ini.get_ini('test_device', 'device'), 'w') as f:
        yaml.dump(device_lst, f)
        f.close()

def get_device_info():
    """
    获取当前电脑连接的devices
    :return: 返回设备列表
    """
    logger.info("#####Init-5：获取当前电脑连接的devices#####")
    device_list = []
    ini = U.ConfigIni_App()
    test_info = ini.get_ini('test_info', 'info')
    logger.info('#####获取appium_parameter路径----%s#####'%test_info)
    test_device = ini.get_ini('test_device', 'device')
    logger.info('#####获取device_info路径----%s#####'%test_device)
    with open(test_info) as f:
        test_dic = yaml.load(f)[0]
    with open(test_device) as f:
        for device in yaml.load(f):
            device_list.append(dict(test_dic.items() + device.items()))
    return device_list

def get_device():
    """
    :return: 返回Android设备列表
    """
    android_devices_list = []
    for device in U.cmd('adb devices'):
        if 'device' in device and 'devices' not in device:
            device = device.split('\t')[0]
            android_devices_list.append(device)
    print android_devices_list
    return android_devices_list

def check_environment():
    '''
    校验环境是否安装appium
    :return:
    '''
    logger.info("#####Init-1：校验环境是否安装appium,请耐心等待……#####")
    appium = U.cmd("appium -v")[0].strip()
    if '1.' not in appium:
        logger.error('#####appium not in computer#####')
        exit()
    else:
        logger.info('#####appium version {}#####'.format(appium))
    if not get_device():
        logger.error('#####the computer is not connected to any devices#####')
        exit()

def initialization_arrangement_case(app_name):
    '''
    app_name:app应用名
    初始化设备及APP相关路径信息
    :return:
    '''
    logger.info("#####Init-2：初始化设备及APP相关路径信息#####")
    main_view = os.path.split(os.path.realpath(sys.argv[0]))[0]
    logger.info("#####当前路径main_view:%s#####"%main_view)
    main_view = main_view.replace('\\', '/')
    if 'robot' in main_view:
        main_view = main_view.replace('robot','Automation/utils')
    if 'scripts' in main_view:
        main_view = main_view + '/..'
    ini = U.ConfigIni_App()
    ini.set_ini('test_device', 'device', main_view + '/../resource/app_data/device_config/device_info.yaml')
    logger.info("#####设备信息路径device_info:%s/../resource/app_data/device_config/device_info.yaml#####"%main_view)
    ini.set_ini('test_install_path', 'path', main_view + '/../resource/app_data/app_package/%s.apk'%app_name)
    logger.info("#####app包路径app_package_path:%s/../resource/app_data/app_package/%s.apk#####"%(main_view,app_name))
    ini.set_ini('test_info', 'info', main_view + '/../resource/app_data/appium_config/appium_parameter.yaml')
    logger.info("#####appium基本信息路径appium_parameter_path:%s/../resource/app_data/appium_config/appium_parameter.yaml#####"%main_view)
    ini.set_ini('test_case', 'log_file', main_view + '/../resource/app_data/result/')
    logger.info("#####日志文件路径log_file_path:%s/../resource/app_data/result/#####"%main_view)

class RunApp(object):
    def __init__(self, device_arg):
        """
        self.time:用于建立存放文件的目录
        """
        self.time = time.strftime(
            "%Y-%m-%d_%H_%M_%S",
            time.localtime(
                time.time()))
        for device in device_arg:
            self.device = device
            self.device_name = device['deviceName']
        # self.device = device_arg
        # self.device_name = device_arg['deviceName']
        logger.info('#####start test device:%s#####' % self.device_name)

        self.all_result_path = self.mkdir_file()
        """
        self.device元祖中包含了appium_parameter.yaml和device_info.yaml中两部分信息即设备号信息和appium启动信息
        """
        self.ia = InstallApp(self.all_result_path, self.device)

    def mkdir_file(self):
        """
        :return:创建日志存放文件夹
        """
        ini = U.ConfigIni_App()
        result_file = str(ini.get_ini('test_case', 'log_file'))
        result_file_every = result_file  + \
                            time.strftime("%Y-%m-%d_%H_%M_%S{}".format(random.randint(10, 99)),
                                          time.localtime(time.time()))
        logger.info('#####日志文件存放路径----%s#####'%result_file_every)
        file_list = [
            result_file,
            result_file_every,
            result_file_every + '/log',
            result_file_every + '/per',
            result_file_every + '/img',
            result_file_every + '/status']
        if not os.path.exists(result_file):
            os.mkdir(result_file)

        for file_path in file_list:
            if not os.path.exists(file_path):
                os.mkdir(file_path)
        return result_file_every

    def install_app(self):
        logger.info('#####开始安装被测应用,请稍后.....#####')
        self.ia.main()

    @U.l()
    def get_appium_port(self):
        """
        :return: 开启appium端口
        """
        sp = Sp(self.device_name,self.all_result_path)
        self.appium_port = sp.main()
        logger.info('#####Appium正在启动中，请稍后.....#####')
        time.sleep(15)
        return self.appium_port

    @U.l()
    def clear_process(self):
        """

        :return: 清理appium与logcat进程
        """
        cp = Cp()
        logger.info('#####正在清理appium与logcat进程，请稍后.....#####')
        cp.clean_process(self.appium_port, self.device)
        return self.appium_port

    def start_appium(self):
        """
        启动driver
        :return:
        """

        number_of_starts = 0
        self.appium_port = self.get_appium_port()
        while number_of_starts < 6:
            try:
                self.driver = webdriver.Remote(
                        'http://127.0.0.1:%s/wd/hub' %
                    self.appium_port, self.device)
                logger.info('######appium start %s success#####' % self.device)
                return self.driver
            except Exception as e:
                number_of_starts += 1
                logger.error('#####Failed to start appium :{}#####'.format(e))
                logger.error(
                    '#####Try restarting the appium :{},Trying the {} frequency#####'.format(self.device, number_of_starts))
                time.sleep(5)
        if number_of_starts > 5:
            logger.error('#####Can not start appium, the program exits#####')
            exit()


    def kill_appiumServer(self):

       #查找对应端口的pid
       cmd_find='netstat -aon | findstr %s' %4723

       result = os.popen(cmd_find)
       text = result.read()
       pid=text[-5:-1]

       #执行被占用端口的pid
       cmd_kill='taskkill -f -pid %s' %pid
       os.popen(cmd_kill)


class InstallApp:
    def __init__(self, all_result_path, device):
        """
        Queue模块是用于进程间通信的模块

        :param all_result_path: 本次测试创建的文件夹
        :param device: 设备id
        """
        self.all_result_path = all_result_path
        self.device = device
        self.device_name = self.device['deviceName']
        self.adb = adbUtils.ADB(self.device_name)
        self.queue = Queue(10)

    @U.l()
    def __uidump(self):
        """
        获取当前Activity控件树
        :return:xml在电脑内的地址存储地址
        """
        save_path = self.all_result_path + "/dump.xml"
        self.adb.get_focused_package_xml(save_path)
        return save_path

    @U.l()
    def __element(self):
        """
        同属性单个元素，返回单个坐标元组
        button_list:常见的确认,同意,按钮控件id
        """
        button0 = 'com.android.packageinstaller:id/ok_button'
        button1 = 'com.android.packageinstaller:id/btn_allow_once'
        button2 = 'com.android.packageinstaller:id/bottom_button_two'
        button3 = 'com.android.packageinstaller:id/btn_continue_install'
        button4 = 'android:id/button1'
        button5 = 'vivo:id/vivo_adb_install_ok_button'
        button_list = [button0, button1, button2, button3, button4, button5]
        self.__uidump()
        self.pattern = re.compile(r"\d+")
        if not os.path.exists(self.all_result_path + "/dump.xml"):
            logger.warn('Failed to get xml')
            return None

        tree = ET.ElementTree(file=self.all_result_path + "/dump.xml")
        tree_iter = tree.iter(tag="node")
        for elem in tree_iter:
            if elem.attrib["resource-id"] in button_list:
                bounds = elem.attrib["bounds"]
                coord = self.pattern.findall(bounds)
                x_point = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                y_point = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                return x_point, y_point
        else:
            return None

    def tap(self):
        """
        点击动作
        :return:
        """
        coordinate_points = self.__element()
        if coordinate_points is not None:
            self.adb.touch_by_element(coordinate_points)

    def tap_all(self):
        """
        不间断获取xml,并且点击。配合多线程使用
        :return:
        """
        while True:
            self.tap()
            if not self.queue.empty():
                break

    @U.l()
    def __install_app(self, package_name, app_file_path):
        """

        :param package_name: 应用的报名:com:x.x
        :param app_file_path: 应用的安装路径,注意需要绝对路径
        :return:
        """
        self.adb.quit_app(
            'com.android.packageinstaller')  # kill安装程序,用于处理oppo的一个bug
        if self.queue.empty():
            """
            控制每次是否重装应用
            通过parameter_configuration中noReset控制，为true时不每次安装，为false每次重装
            """
            if not self.device['noReset']:
                if self.adb.is_install(package_name):
                    logger.info(
                        'del {}-{}'.format(self.device, package_name))
                    self.adb.remove_app(package_name)
            install_num = 0
            while install_num < 4:
                install_info = self.adb.install_app(app_file_path).stdout.readlines()
                logger.info('#####install_info:%s#####'%install_info)
                if self.adb.is_install(package_name):
                    self.queue.put(1)
                    break
                else:
                    logger.error('######Reinstalling %s %s##### '%(package_name,self.device))
                    install_num += 1
            else:
                raise AssertionError('Reinstalling app error')

            # kill安装程序,用于处理oppo的一个bug
            self.adb.quit_app('com.android.packageinstaller')

    def main(self):
        """
        开启多线程:
                线程1:安装应用
                线程2:获取当前页面是否有可点击的按钮
        :return:
        """
        ini = U.ConfigIni_App()
        install_file = ini.get_ini('test_install_path', 'path')
        package_name = ini.get_ini('test_package_name', 'package_name')
        logger.info('#####安装文件install_file----%s#####'%install_file)
        logger.info('#####应用包名package_name----%s#####'%package_name)
        threads = []

        click_button = threading.Thread(target=self.tap_all, args=())
        threads.append(click_button)
        install_app = threading.Thread(
            target=self.__install_app, args=(
                package_name, install_file))
        threads.append(install_app)
        process_list = range(len(threads))

        for i in process_list:
            threads[i].start()
        for i in process_list:
            threads[i].join()

        self.adb.shell('"rm -r /data/local/tmp/*.xml"')

class Sp:
    def __init__(self, device_name,all_result_path):
        self.__device_name = device_name
        self.__all_result_path = all_result_path


    def __start_driver(self, aport, bpport):
        """
        清理logcat与appium所有进程
        :return:
        """
        if platform.system() == 'Windows':
            # 在win10启动appium有bug,暂时处理方案
            cport = random.randint(8800, 8888)
            import subprocess
            logger.info("#####appium -p %s -bp %s -U %s --chromedriver-port %s#####" %(aport, bpport, self.__device_name, cport))
            with open("%s/log/appium_log.log"%self.__all_result_path,'w+') as appium_log:
                subprocess.Popen("appium -p %s -bp %s -U %s --chromedriver-port %s" %
                             (aport, bpport, self.__device_name, cport), shell=True,stdout=appium_log)
            #通过读取日志文件判断appium服务器是否启动完毕，未启动完毕超时
            # self.__is_appium_start(appium_log,40)
        else:
            appium = U.cmd("appium -p %s -bp %s -U %s" %
                           (aport, bpport, self.__device_name))  # 启动appium
            while True:
                appium_line = appium.stdout.readline().strip()
                logger.debug(appium_line)
                time.sleep(1)
                if 'listener started' in appium_line or 'Error: listen' in appium_line:
                    break

    def __is_appium_start(self,filepath,timeout=40):
        '''
        检测appium服务是否完全启动
        filepath:日志文件路径
        timeout:查询超时时间
        :param filepath:
        :param timeout:
        :return:
        '''
        p = 0
        flag = True
        with open(filepath, 'r+') as f:
            f.seek(p, 0)
            time_start=time.time()
            print time_start
            while True and flag:
                lines = f.readlines()
                if lines:
                    for i in range(0,len(lines)):
                        if 'Appium REST http interface listener started on' in lines[i]:
                            print lines[i]
                            f.close()
                            flag = False
                    p = f.tell()
                    f.seek(p, 0)
                time_end = time.time()
                if float("%.f"%(time_end - time_start)) > timeout:
                    logger.error("######Appium启动失败，正在尝试重新启动#####")
                    f.close()
                    break
                time.sleep(2)


    def start_appium(self):
        """
        启动appium
        p:appium port
        bp:bootstrap port
        :return: 返回appium端口参数
        """

        aport = random.randint(4700, 4900)
        bpport = random.randint(4700, 4900)
        logger.info(
            '#####start appium :p %s bp %s device:%s#####' %
            (aport, bpport, self.__device_name))
        self.__start_driver(aport, bpport)
        time.sleep(10)
        return aport

    def main(self):
        """

        :return: 启动appium
        """
        return self.start_appium()

class Cp(object):
    def __darwin(self, port, device):
        # for line in U.cmd(
        #     "lsof -i tcp:%s | grep node|awk '{print $2}'" %
        #         str(port)):
        #     U.cmd('kill -9 %s' % line.strip())
        #     U.Logging.debug('CleanProcess:Darwin:kill appium')
        for line in U.cmd(
                "ps -A | grep logcat | grep %s" % device):
            U.cmd('kill -9 %s' % line.strip())
            logger.debug('#####CleanProcess:Darwin:kill logcat#####')

    def __linux(self, port, device):
        # linux必须最高权限才可获取到端口
        # for line in U.cmd(
        #     "lsof -i:%s |awk '{print $2}'" %
        #         str(port)):
        #     U.cmd('kill -9 %s' % line.strip())
        #     U.Logging.debug('CleanProcess:linux:kill appium')
        for line in U.cmd(
            "ps -ef | grep logcat | grep %s|awk '{print $2}'" %
                device):
            U.cmd('kill -9 %s' % line.strip())
            logger.debug('#####CleanProcess:linux:kill logcat#####')

    def __darwin_all(self, ):
        for line in U.cmd(
                "ps -A | grep logcat|awk '{print $1}'"):
            U.cmd('kill -9 %s' % line.strip())
            logger.debug('#####CleanProcess:Darwin:kill logcat#####')
        for line in U.cmd(
                "ps -A | grep appium|awk '{print $1}'"):
            U.cmd('kill -9 %s' % line.strip())
            logger.debug('#####CleanProcess:Darwin:kill appium#####')

    def __linux_all(self):
        for line in U.cmd(
                "ps -ef | grep logcat|grep -v grep|awk '{print $2}'"):
            U.cmd('kill -9 %s' % line.strip())
            logger.debug('#####CleanProcess:linux:kill logcat#####')

        for line in U.cmd(
                "ps -ef |grep appium |grep -v grep|awk '{print $2}'"):
            U.cmd('kill -9 %s' % line.strip())
            logger.debug('#####CleanProcess:linux:kill appium#####')

    def __windows(self,port):
        # todo windows未完成
        for line in U.cmd(
                'netstat -aon|findstr %s | findstr \"LISTENING\"'%port):
            pid = line.strip().split(' ')[-1]
            # process_name = U.cmd(
            #     'tasklist|findstr {}'.format(pid)).stdout.read().split(' ')[0]
            # U.cmd('taskkill /f /t /im {}'.format(process_name))
            U.cmd('taskkill -f -pid %s' %pid)

    def clean_process(self, port, device):
        """
        清理logcat与appium指定进程
        :return:
        """
        if platform.system() == 'Darwin':
            self.__darwin(port, device)
        elif platform.system() == 'Linux':
            self.__linux(port, device)
        elif platform.system() == 'Windows':
            self.__windows(port)
        else:
            logger.debug(
                '#####CleanProcess:Not identifying your operating system#####')

    def clean_process_all(self, ):
        """
        清理logcat与appium所有进程
        :return:
        """
        if platform.system() == 'Darwin':
            self.__darwin_all()
        elif platform.system() == 'Linux':
            self.__linux_all()
        else:
            logger.debug(
                '#####CleanProcess:Not identifying your operating system#####')

if __name__ == "__main__":
    # test = RunApp([{'deviceName':'abc'}])
    print platform.system()