#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from Automation.aw.Page import Page



class TagDetail(object):
    if __name__ == '__main__':
        
        ul = Page()

        ul.ums_open_browser('chrome','chromedriver')
        ul.ums_login('http://6.test.ums86.com/index.jsp','610606','zc','test123')
#         ul.TL_setDbInfo("zx_magazine","10.0.0.115","zx_magazine","zx_magazine#5402")
#         ul.insertTmpTag()
        ul.TagMagager_addTag("郭郭频道","郭芊芊")
        ul.ums_close_windows()
        ul.TagMagager_showTagDetail("郭郭频道","郭芊芊")
        ul.ums_close_windows()
        ul.TagMagager_deleteTag("郭郭频道","郭芊芊")
        ul.ums_close_windows()
#         ul.delTmpTag()
        ul.ums_close_browser()





