from django.db import models
#-*- coding: utf8 -*-
# Create your models here.
from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
on_delete=models.DO_NOTHING,
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

#除了自己定义属性 常用的属性django.contrib.auth.models
#需要extend and customize user类
#对于改写代码的方法 官方教程是最权威的和兼容的
#类名首字母大写 attr名字全部小写

class Listener(models.Model):
    #只要保证用户名是不重名的 用户ID没必要定义
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    desciption = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    # 不需要many to many with musics


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    def __str__(self):
        return self.name


#假设一首歌只会被一个歌手演唱
class Singer(models.Model):
    name = models.CharField(max_length=30)
    keyword = models.CharField(max_length=100) #对歌手类型，风格的关键词描述
    #music = models.ForeignKey(Music) #一个歌手会唱很多歌曲 但是好像不用相互定义foreign key
    def __str__(self):
        return self.name

Song_choices = (
    (u'乡村/民谣', u'乡村/民谣'),
    (u'摇滚', u'摇滚'),
    (u'蓝调/爵士', u'蓝调/爵士'),
    (u'R&B', u'R&B'),
    (u'情歌/伤感', u'情歌/伤感'),
    (u'动感/舞曲', u'动感/舞曲'),
    (u'网络歌曲/电子乐', u'网络歌曲/电子乐'),
    (u'轻音乐/纯音乐', u'轻音乐/纯音乐'),
(u'not_classifed_yet', u'not_classifed_yet'),
)

class Music(models.Model):
    id = models.AutoField(primary_key=True) #有很多重名的歌曲 唯一id标识 #但是好像models.Model已经有id了
    name = models.CharField(max_length=100)
    #listener = models.ManyToManyField(Listener)
    #一首歌有很多听众 一个听众会收藏很多歌曲 删除 因为添加了歌单class
    #note 多对多的关系也不需要互相定义
    singer = models.ForeignKey(Singer,on_delete=models.CASCADE)  #每一个music只有一个歌手
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE) #每一个music只有一个出版商

    publication_date = models.DateField(default=datetime.date.today) #出版时间
    lyrics = models.CharField(max_length=100) #不知道这个支不支持歌词文件？
    audio = models.CharField(max_length=100)
    type = models.CharField(max_length=50,null=True,choices=Song_choices,default="not_classifed_yet")
    volume= models.IntegerField(default=0)
    def __str__(self):
        return self.name


class UserSongList(models.Model):
    id = models.AutoField(primary_key=True)
    songlistname = models.CharField(max_length=100)
    #一个用户有多个歌单 相同的歌曲可以归属于不同的歌单
    listener = models.ForeignKey(Listener,on_delete=models.CASCADE)
    music = models.ManyToManyField(Music,blank=True,null=True)
    def __str__(self):
        return self.songlistname
    #最终 指定歌单id 指定用户 有多首歌曲 在数据库中按照多条存放 删除的时候也好处理

#一个用户收听歌曲的log 并不一定收听完之后一定会点击收藏

class Mark(models.Model):
    id = models.AutoField(primary_key=True)
    listener = models.ForeignKey(Listener,on_delete=models.CASCADE)
    music = models.ForeignKey(Music,on_delete=models.CASCADE)
    mark = models.IntegerField()

#使用auto field 每次会自动连续生成id 而不用我自己输入 记住id的cursor到了什么位置