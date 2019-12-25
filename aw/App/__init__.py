#Author:Paul J
#  Copyright (c) 2010 Franz Allan Valencia See
#
#  Licensed under the Apache Lidcense, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from Automation.aw.App.AppBase import AppBase
from Automation.aw.App.DemoProjectApp.News import News

class App(       
                 News,
                 AppBase
                 ):
    """
    This is defind Library

    """


    ROBOT_LIBRARY_SCOPE = 'GLOBAL'


