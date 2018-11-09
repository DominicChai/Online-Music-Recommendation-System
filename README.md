# Online-Music-Recommendation-System
 Use HTML, CSS, J-Query and React, Bootstrap architecture as frontend, use Django(in Python) as backend and design an user-based recommend algorithm

# 框架以及编程语言: 网页版

* 后端：Django(Python 3.7 in PyCharm) Python
* 主要Python库: os用于文件路径管理, numpy用于评分矩阵的存储和计算，math用于定义协同过滤中的余弦相似度
* 数据库：SQLite
* 前端：HTML5, CSS, Javascript用于生成音乐播放器对象, J-Query用于和Django以JSON进行交互，局部更新页面信息，在页面中追加新的HTML元素

# 业务需求

1）管理端
* 歌曲添加，新的用户和各种对象的增删改查所有基本操作
Note：通过http://127.0.0.1:8000/admin/ 直接访问即可

* 歌曲推荐：基于用户打分矩阵的协同过滤算法，计算用户之间的cosine相似度，反差表进行推荐
Note：解决冷启动问题：初始用户给他推荐当前曲库中收听量排名最高的歌曲

2）客户端

* 用户注册
* 用户登录：登陆之后使用session保持登录状态
* 用户登出
* 歌曲查询：按照歌曲关键字进行查询/按照歌手名字进行查询
* 歌曲播放：JS动态生成歌曲播放器
Note：浏览器缓存 可以用进度条控制进度 歌词随着歌曲滚动高亮显示
* 歌曲打分（如1-5分）
* 歌单管理：创建新的歌单
* 收藏歌曲：向已有的歌单中选择一个歌单，添加歌曲
* 创建并上传自己的音乐文件
 
# 	数据库设计

音乐（歌曲名称和基本信息 歌词 歌曲类别）
用户：基本用户和管理员

Note: 用户和音乐具有收听，收藏的多对多的关系，引入新的对象：歌单，歌单和用户具有一对多的关系（一个用户可以创建多个歌单，一个歌单只属于一个用户），但是此时音乐和歌单还有多对多的关系（一个歌单可以收藏多个音乐，一个音乐可以属于不同用户的不同歌单），于是引入新的对象：歌单中收藏的音乐，来消除音乐和歌单的多对多关系

出版商：一个出版商（例如：滚石唱片）可以出版多首音乐，一首音乐因为版权问题仅仅属于一家唱片公司
歌手：一个歌手演唱多首歌曲，一首音乐被一位歌手演唱（这里我们简化业务：不存在歌手们合唱的情况）
歌单：一个用户可以为自己创建不同的歌单（这里我们简化业务：歌单不能被不同的用户共享）
歌曲评分：每一个用户可以为每一个歌曲根据喜好程度打出1-5不同的分值

# 部分源代码文件结构：
 
Django框架采用MVC模式（Model，View和Control）
所以如上图对应的在models.py定义了不同的对象/数据库模型，并且实现了对象和数据库的关联映射，在urls.py中定义了不同的request的格式，在views.py中存储了对应不同的request不同的视图和数据库操作（例如查询，选择，排序，推荐等），最终views里面的视图函数
1.	将数据传给HTML，返回template下的HTML文件
2.	将从数据库中获取的JSON文件传给template下的HTML文件中的JS，JS局部更新页面

Note：HTML文件中嵌入了主要的J-Query代码
Note：主要的CSS代码，音乐播放器的JS代码，音乐的音频文件和音乐的歌词文件，在static之下，如下图：
 
