# -*- coding: utf-8 -*-
# Author:Paul J
# Verson:3.0.0
import base64, ConfigParser, os, sys, csv, threading, random, string, subprocess
import tempfile, traceback, logging.config, time
from robot.api import logger as logger_robot

'''
设置全局编码
'''
reload(sys)
sys.setdefaultencoding('utf8')


def cmd(cmd):
    try:
        out_temp = tempfile.SpooledTemporaryFile(bufsize=10 * 1000)
        fileno = out_temp.fileno()
        p = subprocess.Popen(cmd, shell=True, stdout=fileno, stderr=fileno)
        p.wait()
        out_temp.seek(0)
        return out_temp.readlines()
    except Exception, e:
        logger.error(traceback.format_exc())
    finally:
        if out_temp:
            out_temp.close()


def abspath(py_file, conf_dir=None):
    if conf_dir == None:
        conf_dir = ""
    return os.path.normpath(
        os.path.join(os.path.normpath(
            os.path.dirname(os.path.realpath(py_file))), conf_dir))


def getPythonDir():
    '''
    获得python的安装路径
    '''
    python_path = sys.prefix.strip("'")
    return python_path


def l():
    """
    打印log
    文件名+函数名,return
    :return:
    """

    def log(func):
        def wrapper(*args, **kwargs):
            t = func(*args, **kwargs)
            filename = str(sys.argv[0]).split('/')[-1].split('.')[0]
            # E:/Auto_Analysis-master/public/GetCase.py 以/来分割取最后一个，以.来分割取第一个GetCase
            logger.info('{}:{}, return:{}'.format(filename, func.__name__, t))
            return t

        return wrapper

    return log


def setup_logging(
        default_path=os.path.dirname(__file__) + '/../resource/log/log_config/logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration
    """
    try:
        import yaml
    except:
        logger.warn("##### No yaml package,need to download. #####")
        os.system(getPythonDir() + "/Scripts/pip install pyyaml -i https://pypi.douban.com/simple/")
        import yaml
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read(),Loader=yaml.FullLoader)
        config['handlers']['info_file_handler']['filename'] = os.path.dirname(__file__) + '/../resource/log/info.log'
        config['handlers']['error_file_handler']['filename'] = os.path.dirname(__file__) + '/../resource/log/errors.log'
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


'''
初始化LOG方法
'''
setup_logging()
logger_sys = logging.getLogger("Automation")


class logger():
    '''
          封装log方法，调用log类的方法和robot的log方法
    '''

    @staticmethod
    def write_info_log(msg):
        '''
        info级别日志，打印robot时，直接按格式重写
        '''
        import datetime
        nowTime = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S.%f')[0:-3]
        print "%s :  INFO : %s".decode("utf-8") % (nowTime, msg)

    @staticmethod
    def info(msg, html=False, also_console=False):
        logger_sys.info(msg)
        logger_robot.info(msg, html, also_console)
        # 为了防止log文件中日志重复，故info级别日志重写#
        # logger().write_info_log(msg)

    @staticmethod
    def error(msg):
        logger_sys.error(msg)
        logger_robot.error(msg)

    @staticmethod
    def warn(msg):
        logger_sys.warn(msg)
        logger_robot.warn(msg)

    @staticmethod
    def debug(msg):
        logger_sys.debug(msg)
        logger_robot.debug(msg)


class ConfigIni():
    '''
    读取ini文件相关方法
    '''

    def __init__(self, path, title):
        self.path = path
        self.title = title
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)

    def get_ini(self, value):
        return self.cf.get(self.title, value)

    def set_ini(self, title, value, text):
        self.cf.set(title, value, text)
        return self.cf.write(open(self.path, "wb"))

    def add_ini(self, title):
        self.cf.add_section(title)
        # 'wb'不能丢，会报IOError: File not open for writing#
        return self.cf.write(open(self.path, 'wb'))

    def get_options(self, data):
        # 获取所有的section
        options = self.cf.options(data)
        return options


class ConfigIni_App():
    '''
    读取ini文件相关方法（App自动化专用）
    '''

    def __init__(self):
        self.current_directory = os.path.split(
            os.path.realpath(sys.argv[0]))[0]
        # E:\\Auto_Analysis-master\\lib
        self.path = os.path.split(__file__)[0].replace('utils', 'resource/app_data/test_info.ini')
        # E:/Auto_Analysis-master/data/test_info.ini
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)

    def get_ini(self, title, value):
        return self.cf.get(title, value)

    def set_ini(self, title, value, text):
        self.cf.set(title, value, text)
        return self.cf.write(open(self.path, "wb"))

    def add_ini(self, title):
        self.cf.add_section(title)
        return self.cf.write(open(self.path))

    def get_options(self, data):
        # 获取所有的section
        options = self.cf.options(data)
        return options


class Coding():
    '''
    编码转换相关工具
    '''

    def base64_file_encode(self, file):
        '''
        读取文件内容转换为base64编码
        '''
        f = open(r'%s' % file, 'rb')  # 二进制方式打开文件
        ls_f = base64.b64encode(f.read())  # 读取文件内容转换为base64编码
        f.close()
        return ls_f


class StringUtil2():
    '''
    字符串判断辅助工具类
    '''

    def StringContain(self, str, substring):
        "判断str中是否包含substring"
        if substring in str:
            return True
        else:
            return False

    def ReplacePathChar(self, str_path, str1, str2):
        "图片路径中，将//替换成/时用，robot上会有编码问题"
        return str_path.replace(str1, str2)

    def GenPassword(self, length):
        '''
        动态字符串生成器
        '''
        # 随机出数字的个数
        numOfNum = random.randint(1, length - 1)
        numOfLetter = length - numOfNum
        # 选中numOfNum个数字
        slcNum = [random.choice(string.digits) for i in range(numOfNum)]
        # 选中numOfLetter个字母
        slcLetter = [random.choice(string.ascii_letters) for i in range(numOfLetter)]
        # 打乱这个组合
        slcChar = slcNum + slcLetter
        random.shuffle(slcChar)
        # 生成密码
        genPwd = ''.join([i for i in slcChar])
        return genPwd


class Coroutine(object):
    '''
    协程相关方法
    '''
    # 测试配置文件路径#
    test_data_name = ""

    def thread_run(self, func_name, parem_group=[]):
        '''
        - 功能：多线程启动脚本
        - 参数：func_name：需要执行多线程方法的函数名
              parem_group：方法参数，参数不得大于10个
        '''
        threads = []
        for one_group_params in parem_group:
            if len(one_group_params) >= 10:
                logger.error("##### Parameter too many.(need < 10) #####")
                raise ValueError("##### Parameter too many.(need < 10) #####")
            if len(one_group_params) == []:
                t = threading.Thread(func_name)
            if len(one_group_params) == 1:
                t = threading.Thread(target=func_name, args=(one_group_params[0]))
            if len(one_group_params) == 2:
                t = threading.Thread(target=func_name, args=(one_group_params[0], one_group_params[1]))
            if len(one_group_params) == 3:
                t = threading.Thread(target=func_name,
                                     args=(one_group_params[0], one_group_params[1], one_group_params[2]))
            if len(one_group_params) == 4:
                t = threading.Thread(target=func_name, args=(
                    one_group_params[0], one_group_params[1], one_group_params[2], one_group_params[3]))
            if len(one_group_params) == 5:
                t = threading.Thread(target=func_name, args=(
                    one_group_params[0], one_group_params[1], one_group_params[2], one_group_params[3],
                    one_group_params[4]))
            if len(one_group_params) == 6:
                t = threading.Thread(target=func_name, args=(
                    one_group_params[0], one_group_params[1], one_group_params[2], one_group_params[3],
                    one_group_params[4],
                    one_group_params[5]))
            threads.append(t)
        logger.info("##### Execute thread function:%s #####" % func_name)
        # 线程开始#
        for i in threads:
            i.start()
        # wait for all#
        for i in threads:
            # 线程结束#
            i.join()

    def run(self, func_name, parem_group=[]):
        '''
        - 功能：多协程启动脚本
        - 参数：func_name：需要执行多线程方法的函数名
              parem_group：方法参数，参数不得大于10个
        '''
        try:
            import gevent
            from gevent import monkey
        except:
            logger.warn("##### No gevent package,need to download. ######")
            os.system(getPythonDir() + "/Scripts/pip install gevent -i https://pypi.douban.com/simple/")
            import gevent
            from gevent import monkey

        monkey.patch_socket()

        tmp_list = []
        for one_group_params in parem_group:
            if len(one_group_params) >= 10:
                logger.error("##### Parameter too many.(need < 10) #####")
                raise ValueError("##### Parameter too many.(need < 10) #####")
            if len(one_group_params) == []:
                t = gevent.spawn(func_name)
            if len(one_group_params) == 1:
                t = gevent.spawn(func_name, one_group_params[0])
            if len(one_group_params) == 2:
                t = gevent.spawn(func_name, one_group_params[0], one_group_params[1])
            if len(one_group_params) == 3:
                t = gevent.spawn(func_name, one_group_params[0], one_group_params[1], one_group_params[2])
            if len(one_group_params) == 4:
                t = gevent.spawn(func_name, one_group_params[0], one_group_params[1], one_group_params[2],
                                 one_group_params[3])
            if len(one_group_params) == 5:
                t = gevent.spawn(func_name, one_group_params[0], one_group_params[1], one_group_params[2],
                                 one_group_params[3], one_group_params[4])
            if len(one_group_params) == 6:
                t = gevent.spawn(func_name, one_group_params[0], one_group_params[1], one_group_params[2],
                                 one_group_params[3], one_group_params[4], one_group_params[5])
            tmp_list.append(t)
        logger.info("##### Execute gevent function:%s #####" % func_name)
        gevent.joinall(tmp_list)

    def getTestData(self, test_data_name):
        '''
        - 功能：从配置文件中获取测试数据
        - 参数：test_data_name-测试配置文件路径
        '''
        logger.info("##### Data configure file path:%s #####" % test_data_name)
        csvFile = open(test_data_name, "r")
        reader = csv.reader(csvFile)
        csv_list = []
        # 把每一行加到列表中#
        for line in reader:
            # 忽略第一行标题#
            if reader.line_num == 1:
                continue
            # 计算并发执行数#
            for i in range(int(line[4])):
                csv_list.append(line[:len(line) - 1])
        csvFile.close()
        return csv_list

    def writeLog(self, log_path, text):
        '''
        - 功能：写文件到日志中
        - 参数：text-日志信息
               log_path-日志文件路径
        '''
        f = open(log_path, "a")
        logger.write_info_log(text)
        # logger.info(text)
        f.write(text)
        f.close()


class AirTest():
    '''
    AirTest脚本命令行执行
    '''

    def AirTestRunner(self, sn, script_path, log_path):
        '''
        - 功能：运行AirTest脚本
        - 参数：sn-设备号
               script_path-air脚本路径
               log_path-日志路径
        '''
        logger.info("##### Execute AirTest script. #####")
        cmd1 = 'AirtestIDE runner "%s"  --device Android://127.0.0.1:5037/%s --log "%s"' % (script_path, sn, log_path)
        logger.info("##### Execute command: %s #####" % cmd1)
        os.system(cmd1.decode("utf8").encode("gbk"))
        os.popen("taskkill /F /IM adb.exe")
        cmd2 = 'AirtestIDE reporter %s --log_root %s --outfile %s' % (
            script_path, log_path, log_path + os.sep + "log.html")
        logger.info("##### Execute generate report command:%s #####" % cmd2)
        os.system(cmd2.decode("utf8").encode("gbk"))
        time.sleep(3)

    def checkAirTestResult(self, log_path, sid, check_desc=""):
        '''
        - 功能：[检查点]校验AirTest脚本执行结果
        - 参数：log_path-日志路径
              sid-日志文件夹序号
              check_desc-校验脚本是否正确执行完毕的断言叙述（默认为空）
        '''
        logger.info("##### [CheckPoint]check execute result. #####")
        check_flag = 0
        try:
            f = open(log_path + os.sep + "log.html")
            for line in f.readlines():
                if "[Failed]" in line:
                    logger.error("##### Exist failed checkpoint,please to to 【%s】 to see detail. #####" % sid)
                    return False
                # 校验脚本是否正确执行完#
                if check_desc != "" and check_desc is not None:
                    # 找到脚本结束标记了！#
                    if check_desc in line:
                        check_flag = 1
            # 校验脚本是否正确执行完#
            if check_desc != "" and check_desc is not None:
                # 通过标记发现，脚本执行结束#
                if check_flag == 1:
                    logger.info("##### Script execute finished. Checkpoint successfully. #####")
                    return True
                # 没有发现脚本执行结束标记#
                else:
                    logger.error("##### Unfind finished flag,please to to 【%s】 to see detail. #####" % sid)
                    return False
            else:
                logger.info("##### Checkpoint successfully. #####")
                return True
        except Exception, e:
            logger.info(e)
            logger.error("##### Resolve AirTest log file error,please go to 【%s】 to see detail. #####" % sid)
            return False


if __name__ == '__main__':
    setup_logging()
    logger_sys = logging.getLogger(__name__)
