
简述
========

基于Scrapy的爬虫程序，爬取程序员客栈的用户资料( https://www.proginn.com/users/ )，爬取掘金网全部标签的文章(https://juejin.im/subscribe/all?sort=newest)，并存储于MongoDB

联系
============

* Devon
* QQ：849996781
* Email：k849996781@vip.qq.com
* 码云：https://gitee.com/devon888/events
* Github：https://github.com/kongdewen1994

要求
============

* Python 2.7或Python 3.4+
* 适用于Linux，Windows，Mac OSX
* Mongodb 3.x
* Scrapy 1.x

运行
=======

程序员客栈的用户资料::

    scrapy crawl user


    //--------------------数据格式如下-----------------------//
    {
        "_id" : ObjectId("5a657f7c0dd364221c83784b"),
        "dec" : "              ",
        "work_price" : "400",
        "work_time" : "可工作时间: 工作日16:00-22:00、周末08:00-18:00",
        "address" : "南京Java-江苏星网软件有限公司高级后端工程师-大大大蔡-程序员客栈",
        "skill_list" : [ 
            {
                "name" : "AmazeUI",
                "level" : "3"
            }
        ],
        "name" : "大大大蔡",
        "work_list" : [ 
            {
                "job" : "高级后端工程师",
                "cname" : "江苏星网软件有限公司",
                "dec" : "从2014年中至今，主要做行权方面的软件系统，包含“统计分析”、“数据可视化”、“系统接口”等，主要负责整理需求，设计文档，编写项目核心代码及后续系统优化等，并负责组内新员工的指导工作。",
                "time" : "2016-04-25 - 至今"
            }
        ],
        "avatar" : "https://programmerinn.b0.upaiyun.com/useralbum/132668/icon1326681510819060.jpg!mediumicon",
        "works" : [ 
            {
                "imgs" : [ 
                    "https://programmerinnfile.b0.upaiyun.com/default/132668/5a163fbd08682/48e2a8f6a13d5aea7e5e202ce7b6461c.png"
                ],
                "dec" : "某地区政务服务数据可视化分析系统。因政府内网办公系统，涉密，无互联网链接。",
                "name" : "数据可视化"
            }
        ],
        "edu_list" : [ 
            {
                "professional" : "计算机科学与技术",
                "school" : "徐州工程学院",
                "level" : "本科",
                "dec" : "大学期间主要学了计算机基础，编程基础，java和数据库相关的知识。",
                "time" : "2010-09-01 - 2014-06-30"
            }
        ]
    }


掘金网标签文章::

    scrapy crawl juejin

    //--------------------数据格式如下-----------------------//
    {
        "_id" : ObjectId("5a657f510dd36403a00bb18e"),
        "objectId" : "59ce63475188255e723bcef0",
        "title" : "关于数字货币钱包的基础密码学",
        "content" : "<div>......</div>",
        "tag" : [ 
            {
                "name" : "前端",
                "id" : "5597a05ae4b08a686ce56f6f"
            }
        ],
        "time" : "2017-09-29T15:14:15.276Z",
        "dec" : "通过区块链，人类历史上首次通过技术彻底、纯粹地保障「私有财产神圣不可侵犯」。…",
        "utime" : "2018-01-17T16:21:07.503Z"
    }


配置
=============

配置spider_scrapy/spider/settings.py::

    MONGO_HOST = "127.0.0.1"    #MongoDB数据库地址
    MONGO_PORT = 27017          #MongoDB数据库端口
    MONGO_DB = "test"           #MongoDB数据库名称

    JUEJIN_PAGE = 10            #掘金网每个标签要获取的文章数量
    USER_NUM = 100              #程序员客栈获取的用户数量