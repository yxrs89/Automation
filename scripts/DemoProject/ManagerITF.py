#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Automation.aw.Interface import Interface
import unittest


class InterfaceTest(unittest.TestCase):

    def setUp(self):
        global ul   
        ul = Interface()
            
    def testITF1_SelectAllChannels(self):
        result = ul.ITF_SelectAllChannels("http://wxw.test.umss.cn", "43")
        assert ul.checkItfResult(result,
                          "navigationName=>事实军事", 
                          "navigationName=>都市人家", 
                          "periodicalName=>郭郭频道" 
                          )
        
    def testITF2_SelectArticleByIds(self):
        result = ul.ITF_SelectArticleByIds("http://wxw.test.umss.cn","2115", "2695")
        assert ul.checkItfResult(result,
                          "articleAuthor=>老郭",
                          "articleContent=><p>程序员生活在南京软件大道，这是一个忙碌的地方。</p>", 
                          "articleTitle=>论python程序员的自我修养", 
                          "articleAuthor=>小郭",
                          "articleContent=><p>98岁的抗战老兵郭二发，曾参加过淞沪会战、南京保卫战、武汉会战，是一位久经沙场的抗日老兵，曾担任排长、少校营长，186团上校团长。</p>",
                          "articleTitle=>淞沪会战老兵潸然泪下"
                           )

    def testITF3_SelectArticleByChannel(self):
        result = ul.ITF_SelectArticleByChannel("http://wxw.test.umss.cn", spId="43", periodicalId="911", navigationId="779", page="1", pageSize="10")
        assert ul.checkItfResult(result,
                          "articleAuthor=>老郭",
                          "articleContent=><p>程序员生活在南京软件大道，这是一个忙碌的地方。</p>", 
                          "articleTitle=>论python程序员的自我修养", 
                          "articleAuthor=>小郭",
                          "articleContent=><p>98岁的抗战老兵郭二发，曾参加过淞沪会战、南京保卫战、武汉会战，是一位久经沙场的抗日老兵，曾担任排长、少校营长，186团上校团长。</p>",
                          "articleTitle=>淞沪会战老兵潸然泪下"
                           )
        
    def testITF4_SetHotArticleRule(self):
        result = ul.ITF_SetHotArticleRule("http://wxw.test.umss.cn","43", "当月", "1")
        assert ul.checkItfResult(result,
                          "articleContent=><p>测试文章</p>", 
                          "articleTitle=>测试文章", 
                          "articleTitle=>11111111111111111"
                          )

    def testITF5_SelectColumnByChannel(self):
        result = ul.ITF_SelectColumnByChannel("http://wxw.test.umss.cn","911")
        assert ul.checkItfResult(result,
                          "arcitleCount=>2",
                          "navigationName=>都市人家", 
                          "navigationName=>事实军事", 
                          "url=>http://mil.sohu.com/"
                         )

    def testITF6_SelectCycleImageArticle(self):
        result = ul.ITF_SelectCycleImageArticle("http://wxw.test.umss.cn", 
                                                "43", 
                                                "60", 
                                                periodicalId="911", 
                                                navigationId="779", 
                                                pageSize="", 
                                                keywords="程序"
                                                )
        assert ul.checkItfResult(result,
                          "articleContent=><p>程序员生活在南京软件大道，这是一个忙碌的地方。</p>",
                          "periodicalName=>郭郭频道",
                          "articleTitle=>论python程序员的自我修养", 
                          "navigationName=>都市人家"
                          )

    def tearDown(self):
        pass

if __name__ =='__main__':
    unittest.main()