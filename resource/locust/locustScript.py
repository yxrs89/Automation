# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Automation.base.http import http
from Automation.utils.util import ConfigIni,abspath,Coroutine
from Automation.utils.DateUtil import DateUtil
from locust import TaskSet, task, HttpLocust
import json,time
#读取locust执行配置文件#
path = abspath(__file__, 'config.ini')
cfg = ConfigIni(path, "config")
#定义响应结果文件#
time_now = int(time.time())
dt = DateUtil()
time_str = dt.Format_Time(time_now)
log_file = abspath(__file__, './log/response_log_%s.txt' % time_str)
#实例化对象#
check = http()      #需要使用响应键值对校验
log = Coroutine()   #需要使用写到日志文件
#接口信息获取#
uri = cfg.get_ini("uri")
if cfg.get_ini("data") != "None":
    data = cfg.get_ini("data")
else:
    data = None
header = json.loads(cfg.get_ini("header"))
method = cfg.get_ini("type")
if cfg.get_ini("checkpoint") != "None":
    checkpoint_list = cfg.get_ini("checkpoint").decode("utf-8")
else:
    checkpoint_list = None

class UserBehavior(TaskSet):
    @task
    def test_function(self):
        
        if method == "POST":
            with self.client.post(uri, data=data,headers=header, catch_response = True) as response:
                #httpcode检查点失败#
                if response.status_code != 200:
                    log.writeLog(log_file, uri + "\t" + method + "\t" + response.content + "\t" + str(response.status_code) + "\n")
                    response.failure('##### Failed! #####')
                #httpcode检查点成功#
                else:
                    #是否校验json响应键值对#
                    if checkpoint_list is not None:
                        check_result = check.checkJsonResult(response.content, checkpoint_list)
                        #校验响应键值对#
                        if check_result == True:
                            log.writeLog(log_file, uri + "\t" + method + "\t" + response.content + "\t" + "Checkpoint Success" + "\n")
                            response.success()
                        else:
                            log.writeLog(log_file, uri + "\t" + method + "\t" + response.content + "\t" + "Checkpoint Failed" + "\n")
                            response.failure('##### Failed! #####')
                    else:
                        log.writeLog(log_file, uri + "\t" + method + "\t" + response.content + "\t" + "Success" + "\n")
                        response.success()
        else:
            with self.client.get(uri, headers=header, catch_response = True) as response:
                #httpcode检查点失败#
                if response.status_code != 200:
                    log.writeLog(log_file, uri + "\t" + method + "\t" + response.content + "\t" + str(response.status_code) + "\n")
                    response.failure('##### Failed! #####')
                #httpcode检查点成功#
                else:
                    #是否校验json响应键值对#
                    if checkpoint_list is not None:
                        check_result = check.checkJsonResult(response.content, checkpoint_list)
                        #校验响应键值对#
                        if check_result == True:
                            log.writeLog(log_file, uri + "\t" + method + "\t" + response.content + "\t" + "Checkpoint Success" + "\n")
                            response.success()
                        else:
                            log.writeLog(log_file, uri + "\t" + method + "\t" + response.content + "\t" + "Checkpoint Failed" + "\n")
                            response.failure('##### Failed! #####')
                    else:
                        log.writeLog(log_file, uri + "\t" + method + "\t" + response.content + "\t" + "Success" + "\n")
                        response.success()
        
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    host = cfg.get_ini("url")
    min_wait = int(cfg.get_ini("min_wait"))
    max_wait = int(cfg.get_ini("max_wait"))