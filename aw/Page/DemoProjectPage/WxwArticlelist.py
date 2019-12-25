#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:Paul J
from __future__ import unicode_literals
#from time import sleep
#from WxwChannellist import WxwChannellist
from collections import OrderedDict
from Automation.utils.util import *
from Automation.aw.Page.PageBase import PageBase

class WxwArticlelist(PageBase):
    
    def __init__(self, path=None,title=None):
        super(WxwArticlelist, self).__init__()
        if path == None:
            path = abspath(__file__,'../config/DemoProjectPage/articlelist.ini')
        if title == None:
            title = 'articlelist'
        self.articlelist = ConfigIni(path,title)

    def wxw_article_add(self,channel_name,article_name,article_font,article_fontsize,article_attach,article_text,**kwargs):
        '''
        - 事件:微新闻文章新增事件
        - 参数：
        | channel_name(必填):进入列表名称 | article_name(必填):文章标题 | article_font(必填):文章字体(已知字体如:黑体) |
        | article_fontsize(必填):文章字体大小(已知字号如：16px) | article_attach(必填):附件(本地图片英文路径) | article_text(必填)：文章内容 |
        | custom_properties(可选):自定义属性(推荐、热门、跳转、置顶) | forword_url(可选):跳转网址 | article_type:文章展示类型(图文新闻,多图新闻,默认不填文字新闻) |
        | article_image(可选):图文图片(根据文章展示类型上传图片,不同类型图片数量不同,传本地图片英文路径) | article_source(可选):文章来源 | article_Author(可选):发布者 |
        | navigation_id(可选):栏目 | associated_tag(可选):关联标签(栏目中存在才需传参) |
        '''
        self.wxw_list_inter(channel_name)
        self.click(self.articlelist.get_ini("article_manage"))
        self.click(self.articlelist.get_ini("article_add"))
        self.type(self.articlelist.get_ini("article_title_input"),article_name)
        #选择字体
        self.click(self.articlelist.get_ini("article_font_select"))
        self.click("xpath=>//div[@id='edui93_content']/div/div/div/div[text()='%s']"%article_font)
        #选择大小
        self.click(self.articlelist.get_ini("article_fontsize_select"))
        self.click("xpath=>//div[@id='edui108_content']/div/div/div/div[text()='%s']"%article_fontsize)
        #输入正文内容
        self.switch_to_frame(self.articlelist.get_ini("article_text_iframe"))
        self.js("document.getElementsByClassName('view')[1].innerText='%s'"%article_text)
        self.switch_to_frame_out()
        #正文中上传图片
        self.click(self.articlelist.get_ini("article_attach_button"))
        self.switch_to_frame(self.articlelist.get_ini("article_attach_iframe"))
        self.js(self.articlelist.get_ini("article_attach_enable"))
        self.type(self.articlelist.get_ini("article_attach_input"),article_attach)
        self.click(self.articlelist.get_ini("article_attach_upload").decode("utf-8"))
        #判断图片是否上传成功
        if self.element_present(self.articlelist.get_ini("article_attach_success")):
            self.switch_to_frame_out()
            self.click(self.articlelist.get_ini("article_attach_confirm"))
        #自定义属性
        if 'custom_properties' in kwargs:
            if kwargs['custom_properties'] != '':
                custom_properties = kwargs['custom_properties'].split(',')
                for el_custom_properties in custom_properties:
                    if el_custom_properties == '推荐':
                        self.click(self.articlelist.get_ini("article_top_checkbox"))
                    elif el_custom_properties == '热门':
                        self.click(self.articlelist.get_ini("article_hot_checkbox"))
                    elif el_custom_properties == '跳转':
                        self.click(self.articlelist.get_ini("article_forward_checkbox"))
                    elif el_custom_properties == '置顶':
                        self.click(self.articlelist.get_ini("article_scroll_checkbox"))
        #跳转网址
        if 'forword_url'in kwargs:
            if kwargs['forword_url'] != '':
                self.type(self.articlelist.get_ini("article_forwordurl_input"),kwargs['forword_url'])
        #文章展示类型
        if 'article_type' in kwargs:
             if kwargs['article_type'] != '':
                 if kwargs['article_type'] == '图文新闻':
                     self.click(self.articlelist.get_ini("article_graphic_radio"))
                 elif kwargs['article_type'] == '多图新闻':
                     self.click(self.articlelist.get_ini("article_images_radio"))
        #图文图片
        if "article_image" in kwargs:
            if kwargs['article_image'] != '':
                article_image = kwargs['article_image'].split(',')
                i=1
                #有几张图片就上传几张
                for el_article_image in article_image:
                    if i == 1:
                        self.js(self.articlelist.get_ini("article_imageone_enable"))
                        self.type(self.articlelist.get_ini("article_imageone_input"),el_article_image)
                    elif i == 2:
                        self.js(self.articlelist.get_ini("article_imagetwo_enable"))
                        self.type(self.articlelist.get_ini("article_imagetwo_input"),el_article_image)
                    elif i == 3:
                        self.js(self.articlelist.get_ini("article_imagethree_enable"))
                        self.type(self.articlelist.get_ini("article_imagethree_input"),el_article_image)
                    i = i + 1
        #文章来源
        if "article_source" in kwargs:
            if kwargs['article_source'] != '':
                self.type(self.articlelist.get_ini("article_source_input"),kwargs['article_source'])
        #发布者
        if "article_Author" in kwargs:
            if kwargs['article_Author'] != '':
                self.type(self.articlelist.get_ini("article_author_input"),kwargs['article_Author'])
        #栏目
        if "navigation_id" in kwargs:
            if kwargs['navigation_id'] != '':
                self.select_by_text(self.articlelist.get_ini("article_navigation_select"),kwargs['navigation_id'])
        #关联标签
        if "associated_tag" in kwargs:
            if kwargs['associated_tag'] != '':
                associated_tag = kwargs['associated_tag'].split(',')
                for el_associated_tag in associated_tag:
                    self.click("xpath=>//div[@id='labels_article']/label[text()='%s']"%el_associated_tag)
        self.click(self.articlelist.get_ini("article_submit_button"))
        self.click(self.articlelist.get_ini("article_submit_confirm"))
        assert self.element_present("xpath=>//*[@id='listTable']/tbody/tr[2]/td[3]/a[text()='%s']"%article_name)

    def wxw_article_mod(self,channel_name,navigation_mod_id,article_mod_name,article_name,article_font,article_fontsize,article_attach,article_text,**kwargs):
        '''
        - 事件:微新闻文章修改事件
        - 参数：
        | channel_name(必填):进入列表名称 | navigation_mod_id:所属栏目 | article_mod_name:文章标题或编号 |
        | article_name(必填):文章标题 | article_font(必填):文章字体(已知字体如:黑体) | article_fontsize(必填):文章字体大小(已知字号如：16px) |
        | article_attach(必填):附件(本地图片英文路径) | article_text(必填)文章内容 | custom_properties(可选):自定义属性(推荐、热门、跳转、置顶) |
        | forword_url(可选):跳转网址 | article_type:文章展示类型(图文新闻,多图新闻,默认不填文字新闻) | article_image(可选):图文图片(根据文章展示类型上传图片,不同类型图片数量不同,传本地图片英文路径) | article_source(可选):文章来源 |
        | article_Author(可选):发布者 | navigation_id(可选):栏目 | associated_tag(可选):关联标签(栏目中存在才需传参) |
        '''
        self.wxw_article_searchopera(channel_name,navigation_mod_id,article_mod_name)
        article_num_all = self.get_elements(self.articlelist.get_ini("article_num_all"))
        article_name_all = self.get_elements(self.articlelist.get_ini("article_name_all"))
        flag = True
        for el_article_num in article_num_all:
            if el_article_num.text == article_mod_name:
                self.click("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[10]/div/a[1]"%(article_num_all.index(el_article_num)+2))
                flag = False
                break
        if flag:
            for el_article_name in article_name_all:
                if el_article_name.text == article_mod_name:
                    self.click("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[10]/div/a[1]"%(article_name_all.index(el_article_name)+2))
                    break
        self.type(self.articlelist.get_ini("article_title_input"),article_name)
        #自定义属性
        if 'custom_properties' in kwargs:
            if kwargs['custom_properties'] != '':
                custom_properties = kwargs['custom_properties'].split(',')
                for el_custom_properties in custom_properties:
                    if el_custom_properties == '推荐':
                        self.click(self.articlelist.get_ini("article_top_checkbox"))
                    elif el_custom_properties == '热门':
                        self.click(self.articlelist.get_ini("article_hot_checkbox"))
                    elif el_custom_properties == '跳转':
                        self.click(self.articlelist.get_ini("article_forward_checkbox"))
                    elif el_custom_properties == '置顶':
                        self.click(self.articlelist.get_ini("article_scroll_checkbox"))
        #文章展示类型
        if 'article_type' in kwargs:
            if kwargs['article_type'] != '':
                if kwargs['article_type'] == '图文新闻':
                    self.click(self.articlelist.get_ini("article_graphic_radio"))
                elif kwargs['article_type'] == '多图新闻':
                    self.click(self.articlelist.get_ini("article_images_radio"))
                elif kwargs['article_type'] == '文字新闻':
                    self.click(self.articlelist.get_ini("article_text_radio"))
        #图文图片
        if "article_image" in kwargs:
            if kwargs['article_image'] != '':
                # 判断是否已有图片，有的话先删除
                if self.element_present(self.articlelist.get_ini("article_image_delall"),3):
                    article_image_delall = self.get_elements(self.articlelist.get_ini("article_image_delall"))
                    for el_article_image_del in article_image_delall:
                        el_article_image_del.click()
                article_image = kwargs['article_image'].split(',')
                i=1
                #有几张图片就上传几张
                for el_article_image in article_image:
                    if i == 1:
                        self.js(self.articlelist.get_ini("article_imageone_enable"))
                        self.type(self.articlelist.get_ini("article_imageone_input"),el_article_image)
                    elif i == 2:
                        self.js(self.articlelist.get_ini("article_imagetwo_enable"))
                        self.type(self.articlelist.get_ini("article_imagetwo_input"),el_article_image)
                    elif i == 3:
                        self.js(self.articlelist.get_ini("article_imagethree_enable"))
                        self.type(self.articlelist.get_ini("article_imagethree_input"),el_article_image)
                    i = i + 1

        #不存在跳转
        if self.element_present(self.articlelist.get_ini("article_forword_check"),5):
            #选择字体
            self.click(self.articlelist.get_ini("article_font_select"))
            self.click("xpath=>//div[@id='edui93_content']/div/div/div/div[text()='%s']"%article_font)
            #选择大小
            self.click(self.articlelist.get_ini("article_fontsize_select"))
            self.click("xpath=>//div[@id='edui108_content']/div/div/div/div[text()='%s']"%article_fontsize)
            #输入正文内容
            self.switch_to_frame(self.articlelist.get_ini("article_text_iframe"))
            #清空文本框
            self.js("document.getElementsByClassName('view')[1].innerText=''")
            self.js("document.getElementsByClassName('view')[1].innerText='%s'"%article_text)
            self.switch_to_frame_out()
            #正文中上传图片
            self.click(self.articlelist.get_ini("article_attach_button"))
            self.switch_to_frame(self.articlelist.get_ini("article_attach_iframe"))
            self.js(self.articlelist.get_ini("article_attach_enable"))
            self.type(self.articlelist.get_ini("article_attach_input"),article_attach)
            self.click(self.articlelist.get_ini("article_attach_upload").decode("utf-8"))
            #判断图片是否上传成功
            if self.element_present(self.articlelist.get_ini("article_attach_success")):
                self.switch_to_frame_out()
                self.click(self.articlelist.get_ini("article_attach_confirm"))
        else:
            #跳转网址
            if 'forword_url'in kwargs:
                if kwargs['forword_url'] != '':
                     self.type(self.articlelist.get_ini("article_forwordurl_input"),kwargs['forword_url'])
        # 文章来源
        if "article_source" in kwargs:
            if kwargs['article_source'] != '':
                self.type(self.articlelist.get_ini("article_source_input"),kwargs['article_source'])
        # 发布者
        if "article_Author" in kwargs:
            if kwargs['article_Author'] != '':
                self.type(self.articlelist.get_ini("article_author_input"),kwargs['article_Author'])
        # 栏目
        if "navigation_id" in kwargs:
            if kwargs['navigation_id'] != '':
                self.select_by_text(self.articlelist.get_ini("article_navigation_select"),kwargs['navigation_id'])
        # 关联标签
        if "associated_tag" in kwargs:
            if kwargs['associated_tag'] != '':
                associated_tag = kwargs['associated_tag'].split(',')
                for el_associated_tag in associated_tag:
                    self.click("xpath=>//div[@id='labels_article']/label[text()='%s']"%el_associated_tag)
        self.click(self.articlelist.get_ini("article_submit_button"))
        self.click(self.articlelist.get_ini("article_submit_confirm"))
        #校验是否新增成功
        self.ums_close_windows()
        result_flag = self.wxw_article_search(channel_name,navigation_mod_id,article_name)
        assert result_flag



    def wxw_article_publish(self,channel_name,navigation_id,article_name):
        '''
        - 事件:微新闻文章发布事件
        - 参数：
        | channel_name：频道名称 | navigation_id：所属栏目 | article_name：文章标题或编号 |
        '''
        self.wxw_article_searchopera(channel_name,navigation_id,article_name)
        article_num_all = self.get_elements(self.articlelist.get_ini("article_num_all"))
        article_name_all = self.get_elements(self.articlelist.get_ini("article_name_all"))
        flag = True
        for el_article_num in article_num_all:
            if el_article_num.text == article_name:
                if self.element_present("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[9]/span[text()='未发布']"%(article_num_all.index(el_article_num)+2),3):
                    self.click("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[10]/div/a[@title='发布']"%(article_num_all.index(el_article_num)+2))
                    flag = False
                break
        if flag:
            for el_article_name in article_name_all:
                if el_article_name.text == article_name:
                    if self.element_present("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[9]/span[text()='未发布']"%(article_num_all.index(el_article_num)+2),3):
                        self.click("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[10]/div/a[@title='发布']"%(article_name_all.index(el_article_name)+2))
                    break
        self.click(self.articlelist.get_ini("article_publishsureup_button"))
        self.click(self.articlelist.get_ini("article_publishok_button"))
        assert self.element_present("xpath=>//a[@title='%s']/parent::td/parent::tr/td[9 and contains(text(),已发布)]"%article_name)

    def wxw_article_off(self,channel_name,navigation_id,article_name):
        '''
        - 事件:微新闻文章下架事件
        - 参数：
        | channel_name：频道名称 | navigation_id：所属栏目 | article_name：文章标题或编号 |

        '''
        self.wxw_article_searchopera(channel_name,navigation_id,article_name)
        article_num_all = self.get_elements(self.articlelist.get_ini("article_num_all"))
        article_name_all = self.get_elements(self.articlelist.get_ini("article_name_all"))
        flag = True
        for el_article_num in article_num_all:
            if el_article_num.text == article_name:
                if self.element_present("xpath=>//*[@id='listTable']/tbody/tr[%s]/td[9 and contains(text(),'已发布')]"%(article_num_all.index(el_article_num)+2),3):
                    self.click("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[10]/div/a[2]"%(article_num_all.index(el_article_num)+2))
                    flag = False
                break
        if flag:
            for el_article_name in article_name_all:
                if el_article_name.text == article_name:
                    if self.element_present("xpath=>//*[@id='listTable']/tbody/tr[%s]/td[9 and contains(text(),'已发布')]"%(article_num_all.index(el_article_num)+2),3):
                        self.click("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[10]/div/a[2]"%(article_name_all.index(el_article_name)+2))
                    break
        self.click(self.articlelist.get_ini("article_publishsuredown_input"))
        assert self.element_present("xpath=>//a[@title='%s']/parent::td/parent::tr/td[9 and contains(text(),未发布)]"%article_name)


    def wxw_article_del(self,channel_name,navigation_id,article_name):
        '''
        - 事件:微新闻文章删除事件
        - 参数：
        | channel_name：频道名称 | navigation_id：所属栏目 | article_name：文章标题或编号 |
        '''
        self.wxw_article_searchopera(channel_name,navigation_id,article_name)
        article_num_all = self.get_elements(self.articlelist.get_ini("article_num_all"))
        article_name_all = self.get_elements(self.articlelist.get_ini("article_name_all"))
        flag = True
        for el_article_num in article_num_all:
            if el_article_num.text == article_name:
                if self.element_present("//*[@id='listTable']/tbody/tr[%d]/td[9 and contains(text(),'已发布')]"%(article_num_all.index(el_article_num)+2)):
                    self.click("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[10]/div/a[@title='下架']"%(article_num_all.index(el_article_num)+2))
                    self.click(self.articlelist.get_ini("article_publishsuredown_input"))
                self.click("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[10]/div/a[2]"%(article_num_all.index(el_article_num)+2))
                flag = False
                break
        if flag:
            for el_article_name in article_name_all:
                if el_article_name.text == article_name:
                    if self.element_present("//*[@id='listTable']/tbody/tr[%d]/td[9 and contains(text(),'已发布')]"%(article_num_all.index(el_article_num)+2)):
                        self.click("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[10]/div/a[@title='下架']"%(article_num_all.index(el_article_num)+2))
                        self.click(self.articlelist.get_ini("article_publishsuredown_input"))
                    self.click("xpath=>//*[@id='listTable']/tbody/tr[%d]/td[10]/div/a[2]"%(article_name_all.index(el_article_name)+2))
                    break
        self.click(self.articlelist.get_ini("article_delsure_input"))
        self.click(self.articlelist.get_ini("article_delok_button"))
        assert self.element_not_present("xpath=>//*[@id='listTable']/tbody/tr[2]/td[2 and text()='%s']"%article_name) or self.element_present(self.articlelist.get_ini("article_searchnone_img"))

    def wxw_article_delall(self,channel_name):
        '''
        - 事件:微新闻文章全部删除事件
        - 参数：
        | channel_name：频道名称  |
        '''
        self.wxw_list_inter(channel_name)
        self.click(self.articlelist.get_ini("article_manage"))
        while self.element_present(self.articlelist.get_ini("article_oneline_modbutton").decode("utf-8"),3):
            if self.element_present(self.articlelist.get_ini("article_oneline_publish").decode("utf-8"),2):
                self.click(self.articlelist.get_ini("article_oneline_off").decode("utf-8"))
                self.click(self.articlelist.get_ini("article_publishsuredown_input"))
            self.click(self.articlelist.get_ini("article_onedel_button").decode("utf-8"))
            self.click(self.articlelist.get_ini("article_delsure_input"))
            self.click(self.articlelist.get_ini("article_delok_button"))
        assert self.element_present(self.articlelist.get_ini("article_searchnone_img"))

    def wxw_article_search(self,channel_name,navigation_id,article_name):
        '''
        - 事件:微新闻文章搜索事件
        - 参数：
        | channel_name：频道名称 | navigation_id：所属栏目 | article_name：文章标题或编号 |
        '''
        #搜索结果
        result_flag = False
        self.wxw_article_searchopera(channel_name,navigation_id,article_name)
        # 首页是否存在
        #标志首页是否包含所需文章
        home_flg = False
        #判断首页是否有所需要的文章名称
        #标识选用文章标题还是编号进行搜索
        search_home_flag = True
        article_num_all = self.get_elements(self.articlelist.get_ini("article_num_all"))
        article_name_all = self.get_elements(self.articlelist.get_ini("article_name_all"))
        for el_article_num in article_num_all:
            if el_article_num.text == article_name:
                search_home_flag = False
                home_flg = True
                result_flag = True
                break
        if search_home_flag:
            for el_article_name in article_name_all:
                if el_article_name.text == article_name:
                    home_flg = True
                    result_flag = True
                    break
        #如果首页没有
        if not home_flg:
            other_flg = False
            #获取所有列表分页数量
            article_changepage_all = self.get_elements(self.articlelist.get_ini("article_changepage_all"))
            if len(article_changepage_all)>0:
                for el_article_changepage in article_changepage_all:
                    if not other_flg:
                        self.click(self.articlelist.get_ini("article_list_next").decode('utf-8'))
                        search_other_flag = True
                        article_num_all = self.get_elements(self.articlelist.get_ini("article_num_all"))
                        article_name_all = self.get_elements(self.articlelist.get_ini("article_name_all"))
                        for el_article_num in article_num_all:
                            if el_article_num.text == article_name:
                                search_other_flag = False
                                other_flg = True
                                result_flag = True
                                break
                        if search_other_flag:
                            for el_article_name in article_name_all:
                                if el_article_name.text == article_name:
                                    other_flg = True
                                    result_flag = True
                                    break
        return result_flag
        assert result_flag


    def wxw_article_searchopera(self,channel_name,navigation_id,article_name):
        self.wxw_list_inter(channel_name)
        self.click(self.articlelist.get_ini("article_manage"))
        #搜索所要更改文章
        self.select_by_text(self.articlelist.get_ini("article_navigationid_select"),navigation_id)
        self.type(self.articlelist.get_ini("article_search_input"),article_name)
        self.click(self.articlelist.get_ini("article_search_button"))



