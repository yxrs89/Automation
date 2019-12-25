# -*- coding: utf-8 -*-
#Author:Paul J
#Verson:3.0.0
from __future__ import unicode_literals
from Automation.utils.util import logger,getPythonDir
from db import DatabaseClient
import time,datetime,os

try:
    import SSHLibrary
except:
    logger.warn("##### No sshlibrary package，need to download. #####")
    os.system(getPythonDir() + "/Scripts/pip install robotframework-sshlibrary -i https://pypi.douban.com/simple/")
    import SSHLibrary

class ssh(object):
    '''
    Desc:ssh管理类-基础类（使用时先实例化该类）
    '''
    def __init__(self, ip, port, username, password, keyfile=""):
        '''
        函数功能：构造函数
        参    数：ip-跳板机ip
        port-跳板机连接端口
        username-登陆跳板机用户名
        password-连接跳板机密码
        keyfile-登陆跳板机所需秘钥文件路径
        '''
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.keyfile = keyfile

    def connectLinuxHost(self, host_ip, timeout="10s"):
        '''
        预置条件：ssh类实例化
        函数功能：通过跳板机登陆远程主机（第一步）
        参    数：host_ip-远程主机ip
                  timeout-超时时间
        返回值：无
        '''
        self.sshClient = SSHLibrary.SSHLibrary()
        self.sshClient.open_connection(self.ip, port=self.port, timeout=timeout)
        if self.keyfile != "":
            logger.info('##### Use key mode to login. #####')
            self.sshClient.login_with_public_key(self.username, self.keyfile, password=self.password)
        else:
            logger.info('##### Use traditional mode to login. #####')
            self.sshClient.login(self.username, self.password, delay='1.9 seconds')
        self.sshClient.write(host_ip)
        result = self.sshClient.read(delay="0.3s")
        logger.info(result)
        if "successful" in result:
            logger.info("##### %s login successful. #####" % host_ip)
        else:
            count = 1
            while count <= 17:
                logger.info("##### Login failed, retry-%d…… #####" % count)
                time.sleep(0.4)
                result = self.sshClient.read()
                logger.info(result)
                if "successful" in result or "Last login:" in result:
                    break
                else:
                    count = count + 1

    def loginMySQLByJumper(self, user_name, password, DB_name, mysql_path=""):
        '''
        预置条件：ssh类实例化，已经连接到跳板机
        函数功能：通过跳板机连接数据库（第二步）
        参    数：user_name-数据库用户名
                  password-数据库密码
                  DB_name-数据库名
                  mysql_path-主机上，mysql所在路径
        返回值：无
        '''
        if mysql_path == None:
            mysql_path = ""
        loginCmd = mysql_path + "mysql -u%s -p%s" % (user_name, password)
        logger.info("##### Login Mysql command:%s #####" % loginCmd)
        self.sshClient.write(loginCmd)
        result = self.sshClient.read(delay="0.2s")
        logger.info(result)
        if "Welcome to" in result:
            logger.info("##### Login mysql by jumper successfully. #####")
        else:
            count = 1
            while count <= 20:
                logger.info("##### Login mysql failed,retry-%d #####" % count)
                time.sleep(0.5)
                result = self.sshClient.read()
                logger.info(result)
                if "Welcome to" in result:
                    break
                else:
                    count = count + 1
        self.sshClient.write("use " + DB_name + ";")
        result = self.sshClient.read(delay="0.3s")
        logger.info(result)

    def executeSqlQueryByJumper(self, sql, many = False):
        '''
        预置条件：ssh类实例化，已经连接到跳板机，已经登陆mysql
        函数功能：执行sql查询语句（第三步）
        参    数：sql-查询语句
         many-True/False，是否支持多行多列查询，默认false，只支持单行单列
        返回值：元祖类型，（查询到的行数，查询结果字符串）
        '''
        flag = 0 
        if sql[0:-1] == ";":
            pass
        else:
            sql = sql + ";"
        logger.info("##### Execute query sql: #####")
        #没有查询结果，就多试几次#
        while flag < 10:
            self.sshClient.write(sql)
            result = self.sshClient.read()
            time.sleep(1.2 * flag)
            #1.查询结果为空情况#
            if "Empty set" in result:
                logger.info("##### Query empty. #####")
                return "0"
            #2.查询结果不为空情况#
            else:
                #2.1 单行单列查询结果情况#
                if many == False:
                    result_list = result.split("\n")
                    for item in result_list:
                        if  "in set (" in item:
                            line_list = item.split(" ")
                            logger.info("##### Query %s records. #####" % line_list[0])
                            return (line_list[0], result)
                    flag = flag + 1
                    logger.info("##### Query empty,retry-%s, now result is %s #####" % (str(flag + 1), result))
                else:
                    #2.2 多行查询结果情况，做解析成多维元祖，跟传统的方式一致#
                    logger.info("##### Enter query many records mode. #####")
                    result_set = []
                    result_set_tmp = []
                    result_list =  result.split("\n")
                    #第一次过滤无效行#
                    for line in result_list:
                        if "+-" not in line and "in set (" not in line:
                            result_set_tmp.append(line.strip("\r"))
                    result_set_tmp = result_set_tmp[1:len(result_set_tmp)-2]
                    #分割列，去除空格#
                    for line in result_set_tmp:
                        line_set_tmp = []
                        line_tmp_list = line.split("|")
                        line_tmp_list = line_tmp_list[1:len(line_tmp_list)-1]
                        for item in line_tmp_list:
                            line_set_tmp.append(item.strip(" "))
                        result_set.append(line_set_tmp)
                    return result_set
        logger.error("##### Unknow error. #####")
        raise ValueError("##### Unknow error. #####")
        
    def executeSqlOptionByJumper(self, sql):
        '''
        预置条件：ssh类实例化，已经连接到跳板机，已经登陆mysql（第三步）
        函数功能：执行sql操纵语句
        参    数：sql-操纵语句
        返回值：无
        '''
        if sql[0:-1] == ";":
            pass
        else:
            sql = sql + ";"
        logger.info("##### Execute update sql: #####")
        self.sshClient.write(sql)
        result = self.sshClient.read()
        if "ERROR" in result:
            logger.error(result)
            raise ValueError("#### Execute update sql error. ####")

    def executeShellCommand(self, cmd):
        '''
        预置条件：ssh类实例化，已经连接到跳板机
        函数功能：shell命令（第二步）
        参    数：cmd-命令
        返回值：无
        '''
        logger.info("##### Execute shell command:" + cmd + " #####")
        self.sshClient.write(cmd)
        self.sshClient.read(delay="0.5s")
        if "tail" in cmd:
            #tail -200f xxxx情况下，需要ctrl + z结束日志打印#
            self.sshClient.write_bare("")
            self.sshClient.read(delay="0.5s")

    def __del__(self):
        '''
        Desc:在析构函数中关闭ssh连接
        '''
        logger.info('##### Close ssh client connection. #####')
        self.sshClient.close_connection()

class SSHClient(DatabaseClient):
    '''
    SSH相关关键字方法-融合传统型和跳板机数据库操作（可作为Robot关键字使用）
    '''
    #SSH通过跳板机连接数据库#
    __sshclient_dict = {}
    #传统方式连接数据库#
    __dbclient_dict = {}
    
    def connectHost(self, tag, ip, port, username, password, host_ip="", keyfile=""):
        '''
        - 功能：连接跳板机或者linux服务器(第一步)
        - 参数如下：
        - tag：会话id（目的兼容连接多个跳板机）
        - ip：跳板机地址 
        - port：跳板机端口
        - username：跳板机登录名
        - password：跳板机登陆密码
        - host_ip：远程登陆机器ip，为空时则为仅连接linux服务器，不远程登陆
        - keyfile：登陆跳板机所需key文件路径，默认为空
        - RobotFramwork脚本写法示例如下：
        | connectHost | 38006 | xxxxx | 22222 | guozihhui | 124563 | 10.1.1.1 | d:\guozh.pem |
        '''
        #直连数据库情况下， 不需要连接linux服务器#
        if "TRADITION_WAY" in tag:
            logger.info("##### If direct to connect mysql,no need to login linux server. #####")
            return
        #实例化session，支持多个session#
        logger.info("##### Create session id:%s #####" % tag)
        self.__sshclient_dict[tag] = ssh(ip, port, username, password, keyfile)
        #1.需要通过跳板机远程登录#
        if "." in host_ip:
            self.__sshclient_dict[tag].connectLinuxHost(host_ip)
        #2.直连主机，无需跳板机#
        else:
            logger.info("##### Direct to connect linux server,ignore jumper. #####")
    
    def loginMysqlByServer(self, tag, user_name, password, DB_name, DB_ip=None, mysql_path=""):
        '''
        - 功能：通过跳板机登陆数据库（需要先连接跳板机-connectHost）(第二步)
        - 参数如下：
        - tag：会话id（目的兼容连接多个跳板机，如果包含TRADITION_WAY则为传统方式）
        - user_name：数据库登录名 
        - password：数据库密码
        - DB_name：数据库名
        - DB_ip：数据库ip（为了兼容传统连接方式，通过跳板机连接时可不传此参数）
        - mysql_path：主机上mysql所在路径
        - RobotFramwork脚本写法示例如下：
        | loginMysqlByServer | 38006 | flag | flag#1234 | zx_meeting | /opt/local/mysql/bin/ |
        '''
        #1.通过跳板机连接数据库方式#
        if "TRADITION_WAY" not in tag:
            self.__sshclient_dict[tag].loginMySQLByJumper(user_name, password, DB_name, mysql_path)
        #2.传统直连方式，仅先注册连接信息#
        else:
            if DB_ip is None or DB_ip == "":
                logger.error("##### Unknow mysql db ip. #####")
                raise ValueError("##### Unknow mysql db ip. #####")
            logger.info("##### Enter traditional connect to mysql mode,regist login infomation. #####")
            self.__dbclient_dict[tag] = {
                                         "DB_ip":DB_ip,
                                         "user_name":user_name,
                                         "password":password,
                                         "DB_name":DB_name
                                         }
        
    def dbOperationByServer(self, tag, sql):    
        '''
        - 功能：通过跳板机执行sql操纵语句（需要先登陆数据库-loginMysqlByJumper）(第三步)
        - 参数如下：
        - tag：会话id（目的兼容连接多个跳板机，如果包含TRADITION_WAY则为传统方式）
        - sql：数据库操纵语句
        - RobotFramwork脚本写法示例如下：
        | dbOperationByServer| 38006 | update guozh set name = 'haha'; |
        '''
        #1.通过跳板机操纵数据库方式#
        if "TRADITION_WAY" not in tag:
            self.__sshclient_dict[tag].executeSqlOptionByJumper(sql)
        #2.传统直连方式操作数据库#
        else:
            logger.info("##### Enter traditional connect to mysql mode,execute update sql. #####")
            self.dbOperation(self.__dbclient_dict[tag]["DB_name"],
                             self.__dbclient_dict[tag]["DB_ip"],
                             self.__dbclient_dict[tag]["user_name"],
                             self.__dbclient_dict[tag]["password"],
                             sql
                             )
        
    def checkDbSelectResultByServer(self, tag, sql, hope_record):
        '''
        - 功能：[检查点]查询结果有几条记录（需要先登陆数据库-loginMysqlByJumper）(第三步)
        - 参数如下：
        - tag：会话id（目的兼容连接多个跳板机，如果包含TRADITION_WAY则为传统方式）
        - sql：数据库查询语句
        - hope_record：期望查询的结果数
        - RobotFramwork脚本写法示例如下：
        | checkDbSelectResultByServer| 38006 | select * from table1 where name='guozh'; | 2 |
        '''
        #1.通过跳板机操纵数据库方式#
        if "TRADITION_WAY" not in tag:
            result = self.__sshclient_dict[tag].executeSqlQueryByJumper(sql)[0]
            if str(hope_record) == result:
                logger.info("##### Checkpoint successful. #####")
                return True
            else:
                count = 1
                while count <= 9:
                    logger.info("##### Check result not the same, retry-%d" % count)
                    time.sleep(0.8)
                    result = self.__sshclient_dict[tag].executeSqlQueryByJumper(sql)[0]
                    if str(hope_record) == result:
                        logger.info("##### Checkpoint successful. #####")
                        return True
                    else:
                        count = count + 1
                logger.info("##### Expect query " + hope_record +" records,but actual query " + result + " records. #####")
                return False
        #2.传统直连方式查询数据库结果#
        else:
            logger.info("##### Enter traditional connect to mysql mode,execute query sql. #####")
            return self.checkdbSelectResult(self.__dbclient_dict[tag]["DB_name"],
                                            self.__dbclient_dict[tag]["DB_ip"],
                                            self.__dbclient_dict[tag]["user_name"],
                                            self.__dbclient_dict[tag]["password"],
                                            sql,
                                            hope_record
                                            )
    
    def getItemByQuery(self, tag, sql, Many='False'):
        '''
        - 功能：通过sql语句查询，获得值（需要先登陆数据库-loginMysqlByJumper）(第三步)
        - 参数如下：
        - tag：会话id（目的兼容连接多个跳板机，如果包含TRADITION_WAY则为传统方式）
        - sql：数据库查询语句
        - Many：为'True'时，支持查询多行多列，默认为False，只支持单行单列
        - RobotFramwork脚本写法示例如下：
        | getItemByQuery | 38006 | select name from table1 where id='3800'; |
        '''
        #1.通过跳板机操纵数据库方式#
        if "TRADITION_WAY" not in tag:
            #1.1 单行单列模式下#
            if Many == 'False':
                result = self.__sshclient_dict[tag].executeSqlQueryByJumper(sql)
                if type(result) == tuple:
                    result_list = result[1].split("\n")
                    result = result_list[3].split("|")[1].lstrip ()
                    logger.info("##### Get query result:%s #####" % result)
                    return result
                else:
                    logger.error("##### Get query result empty. #####")
                    raise ValueError("##### Get query result empty. #####")
            #1.2 多行模式下#
            else:
                result = self.__sshclient_dict[tag].executeSqlQueryByJumper(sql, True)
                if type(result) == list:
                    i = 1
                    for line in result:
                        logger.info("##### Line-%d #####" % i)
                        for item in line:
                            logger.info("##### Get query result:%s" % item)
                        i = i + 1
                    return result
                else:
                    logger.error("##### Get query result empty. #####")
                    raise ValueError("##### Get query result empty. #####")
        #2.传统直连方式获得数据库结果#
        else:
            logger.info("##### Enter traditional connect to mysql mode,get query result. #####")
            result = self.getDbQuery(self.__dbclient_dict[tag]["DB_name"],
                                     self.__dbclient_dict[tag]["DB_ip"],
                                     self.__dbclient_dict[tag]["user_name"],
                                     self.__dbclient_dict[tag]["password"],
                                     sql
                                    )
            if result != (None,):
                if Many == 'False':
                    return result[0][0][0]
                else:
                    #内容转化成utf-8字符串#
                    result_set = []
                    for line in result[0]:
                        line_tmp = []
                        for item in line:
                            #长整形类型
                            if type(item) == long:
                                item = str(item).decode("utf-8")
                            #时间类型
                            if type(item) == datetime.datetime:
                                item = str(item).decode("utf-8")
                            line_tmp.append(item)
                        result_set.append(line_tmp)
                    return result_set
            else:
                logger.error("##### Get query no result. #####")
                raise ValueError("##### Get query no result. #####")
        
    def executeCommend(self, tag, *cmd):
        '''
        - 功能：在服务器执行命令（需要先连接服务器-connectHost）（第二步）
        - 参数如下：
        - tag：会话id（目的兼容连接多个主机）
        - cmd：要查询日志的命令，如tail - 50f /opt/log.log，可多个，如果日志文件是日期格式，如20170928，需传入**date**参数
        - RobotFramwork脚本写法示例如下：
        | executeCommend | host | tail - 50f /opt/log.log | tail - 50f /opt/log.log2 |
        '''
        cmd_list = []
        for item in cmd:
            if "**date**" in item:
                logger.info("##### The command has date flag,need to format. #####")
                dateStr = time.strftime('%Y%m%d', time.localtime(time.time()))
                item = item.replace("**date**", dateStr)
            cmd_list.append(item)
        for item in cmd_list:
            self.__sshclient_dict[tag].executeShellCommand(item)
            logger.info("##################################################")

#测试桩#
if __name__ == '__main__':
    
    s=SSHClient()
    s.connectHost("server_host_1", "int-login.server.flaginfo.cn","22222","xxxxxxxxx","zbz5WRlocAdkaK46","10.0.0.209","F:\\FlagInfo_work\\xxxxxxxxx.pem")
#     #直连方式#
#     ssh_client = SSHClient()
#     ssh_client.connectHost(
#                            "TRADITION_WAY", 
#                            "int-login.server.flaginfo.cn", 
#                            "22222", 
#                            "xxxxxxxxx",
#                            "zbz5WRlocAdkaK46", 
#                            "10.100.11.185", 
#                            "F:\FlagInfo_work\xxxxxxxxx.pem"
#                            )
#     ssh_client.loginMysqlByServer(
#                                   "TRADITION_WAY",
#                                   "zx_meeting_core",
#                                   "zx_meeting_core#5402",
#                                   "zx_meeting_core",
#                                   DB_ip="10.0.0.135"
#                                   )
#     result = ssh_client.getItemByQuery("TRADITION_WAY", "select * from meeting_remark", "True")
#     print result[0][0]
#     print result[0][1]
#     print result[0][2]
#     print type(result[0][0])
#     print type(result[0][1])
#     print type(result[0][2])
#     print "#############################################################"
#     #毕格云#
#     ssh_client = SSHClient()
#     ssh_client.connectHost(
#                            "12345", 
#                            "int-login.server.flaginfo.cn", 
#                            "22222", 
#                            "xxxxxxxxx",
#                            "zbz5WRlocAdkaK46", 
#                            "10.100.11.185", 
#                            "F:\FlagInfo_work\xxxxxxxxx.pem"
#                            )
#     ssh_client.loginMysqlByServer(
#                                   "12345",
#                                   "flagtest",
#                                   "flag#5402",
#                                   "zx_meeting_core",
#                                   mysql_path="/opt/module/mysql-5.7.10/bin/"
#                                   )
#     result = ssh_client.getItemByQuery("12345", "select * from meeting_remark", "True")
#     print result[0][0]
#     print result[0][1]
#     print result[0][2]
#     print type(result[0][0])
#     print type(result[0][1])
#     print type(result[0][2])