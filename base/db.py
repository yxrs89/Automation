# -*- coding: utf-8 -*-
#Author:Paul J
#Verson:3.0.0
from __future__ import unicode_literals
import MySQLdb
from Automation.utils.util import logger

class db():
    '''
    mysql数据库相关类-基础类（使用时先实例化该类）
    '''
    #游标#
    cur = ""
    #数据库连接#
    conn = ""
    #查询或者影响的行数#
    result_line = 0
    
    def __init__(self, host, user, passwd, db, port=3306):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = int(port)

    def connentDB(self):
        '''
        预置条件：对象实例化
        函数功能：连接数据库
        参    数：host-ip地址
         port-mysql端口
         user-用户名
         passwd-密码
         db-数据库名
         charset-字符集
        返回值：无
        '''
        self.conn= MySQLdb.connect(host = self.host, 
                                   port = self.port, 
                                   user = self.user, 
                                   passwd = self.passwd, 
                                   db = self.db, 
                                   charset = "utf8"
                                   )
        self.cur = self.conn.cursor()
        logger.info("##### Connect MySql DB success. #####")
        
    def executeSQL(self, sql, param=None):
        '''
        预置条件：数据库连接成功
        函数功能：执行增删改相关操作
        参    数：param-参数，列表型
        返回值：无
        '''
        logger.info('##### Execcute update SQL:%s #####' % sql)
        if param is not None:
            count = 1
            param = tuple(param)
            for item in param:
                logger.info('##### Param-%s:%s #####' % (str(count), str(item)))
                count += 1
        self.result_line = self.cur.execute(sql, param)
        logger.info("##### Update lines:%s #####" % str(self.result_line))

    def executeBatchSql(self, sql):
        '''
        预置条件：数据库连接成功
        函数功能：批量执行增删改相关操作
        参    数：sql-sql语句，列表型，且为完整的sql
        返回值：无
        '''
        logger.info('##### Now batch execute. #####')
        for one in sql:
            self.executeSQL(one)
            self.commit()

    def getResultLine(self):
        '''
        预置条件：执行完查询或者操作语句
        函数功能：获取结果行数
        参    数：无
        返回值：查询结果行数
        '''
        return self.result_line

    def querySQL(self, sql, param=None):
        '''
        预置条件：数据库连接成功
        函数功能：执行查询操作
        参    数：param-参数，列表型
        返回值：查询结果集，如果为空，返回None
        '''
        logger.info('##### Execcute query SQL:%s #####' % sql)
        if param is not None:
            count = 1
            param = tuple(param)
            for item in param:
                logger.info('##### Query param-%s:%s #####' % (str(count), str(item)))
                count += 1
        self.cur.execute(sql, param)
        result = self.cur.fetchall()
        if result == ():
            logger.info('##### Query empty. #####')
            self.result_line = 0
            return None
        self.result_line = len(result)
        logger.info("##### Query lines:%s #####" % str(len(result)))
        return result

    def commit(self):
        '''
        预置条件：执行完数据库增删改操作
        函数功能：提交
        参    数：无
        返回值：无
        '''
        logger.info('##### Update commit. #####')
        self.conn.commit()
        
    def curClose(self):
        '''
        预置条件：数据库已经连接
        函数功能：关闭游标
        参    数：无
        返回值：无
        '''
        logger.info('##### Close cursor. #####')
        self.cur.close()
        self.cur = ""
        
    def connClose(self):
        '''
        预置条件：数据库已经连接
        函数功能：断开连接
        参    数：无
        返回值：无
        '''
        logger.info('##### Close corsor. #####')
        self.conn.close()
        self.conn = ""

class DatabaseClient(object):
    '''
    数据库相关关键字方法-传统型（可作为Robot关键字使用）
    '''
    
    def dbOperation(self, db_name, db_ip, db_user, db_password, sql, db_port=3306):
        '''
        - 功能：数据库操作
        - 参数如下：
        - db_name：数据库名 
        - db_ip：数据库ip 
        - db_user：数据库用户名
        - db_password：数据库密码 
        - sql：sql语句 
        - db_port：MySql端口，默认3306
        - RobotFramwork脚本写法示例如下：
        | dbOperation | wxw | 10.0.0.8 | guozh | pass123 |  INSERT INTO `wjd_pay` VALUES ('6666', '6666', '${order_id}', '119.84', null, '1', 'oRVSLuHFtAuvLfE8QlIsNCIqdTO8', null, null, '0', '0', null); |
        '''
        #数据库连接#
        dbo = db(db_ip, db_user, db_password, db_name,int(db_port))
        dbo.connentDB()
        #执行sql#
        dbo.executeSQL(sql),
        dbo.commit()
        #关闭连接#
        dbo.curClose()
        dbo.connClose()

    def getDbQuery(self, db_name, db_ip, db_user, db_password, sql, db_port=3306):
        '''
        - 功能：数据库查询操作，返回查询结果集(二维元祖)
        - 参数如下：
        - db_name：数据库名 
        - db_ip：数据库ip 
        - db_user：数据库用户名
        - db_password：数据库密码 
        - sql：sql查询语句 
        - db_port：MySql端口，默认3306
        - RobotFramwork脚本写法示例如下：
        | ${result} | getDbQuery | wxw | 10.0.0.8 | guozh | pass123  | select * from guozh |
        '''
        #数据库连接#
        dbo = db(db_ip, db_user, db_password, db_name,int(db_port))
        dbo.connentDB()
        #执行sql#
        result = dbo.querySQL(sql),
        #关闭连接#
        dbo.curClose()
        dbo.connClose()
        if result[0] == None:
            logger.info("##### Get query resut empty. #####")
            return ""
        else:
            return result

    def checkdbSelectResult(self, db_name, db_ip, db_user, db_password, sql, hope_record="1", db_port=3306):
        '''
        - 功能：数据库查询操作
        - 参数如下：
        - db_name：数据库名 
        - db_ip：数据库ip 
        - db_user：数据库用户名
        - db_password：数据库密码 
        - sql：查询sql语句 
        - hope_record：期望查询到的结果数，字符型，默认值"1"
        - db_port：MySql端口，默认3306
        - RobotFramwork脚本写法示例如下：
        | ${查询结果} | checkdbSelectResult | wxw | 10.0.0.8 | guozh | pass123 | select * from wjd_pay where wx_order_id like 'wjd19370707%' | 1 |
        '''
        #数据库连接#
        dbo = db(db_ip, db_user, db_password, db_name, int(db_port))
        dbo.connentDB()
        result = dbo.querySQL(sql)
        #1.查询结果为空的情况#
        if result is None:
            #1.1 就希望为空#
            if hope_record == "0":
                logger.info("##### Expect empty,actual empty. #####")
                dbo.curClose()
                dbo.connClose()
                return True
            else:
                #1.2 不希望为空#
                logger.info("##### Expect query %s records,but actual empty. #####" % hope_record)
                dbo.curClose()
                dbo.connClose()
                return False
        #2.查询结果不为空的情况#
        else:
            #2.1 希望记录与实际一致#
            if int(hope_record) == len(result):
                logger.info("##### Expect is the same as actual records. #####")
                dbo.curClose()
                dbo.connClose()
                return True
            else:
                #2.1 希望记录与实际不一致#
                logger.info("Expect query %s records,but actual query %s records." % (hope_record, str(len(result))) )
                dbo.curClose()
                dbo.connClose()
                return False

#测试桩#
if __name__ == '__main__':
    db = db("10.0.0.78",  "zx_magazine", "zx_magazine#5402", "zx_magazine",3306)
    db.connentDB()
    while True:
        lists = db.querySQL("select * from magazine_module")
        print lists
        # db.executeSQL("delete from magazine_label where label_name = %s", ("guozh",))
    db.commit()
    db.curClose()
    db.connClose()
#     db.executeSQL("insert into guozh_test values(%s, %s)", ("guom", "222"))
#     db.commit()
#     db.curClose()
#     db.connClose()
#     print "end"
      

    