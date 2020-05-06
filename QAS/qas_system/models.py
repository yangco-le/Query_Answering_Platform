from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
# Create your models here.


class User(models.Model):
    '''
    用户
    属性：用户名，密码
    与User类为一对一关系
    '''
    user_name = models.CharField(verbose_name='用户名', max_length=30, blank=False, unique=True)
    password = models.CharField(verbose_name='密码', max_length=30, blank=False)
    avatar = models.ImageField(upload_to='avatar/', verbose_name='头像', blank=True, null=True)
    email = models.CharField(max_length=20, default='', verbose_name='邮箱', blank=True, null=True)
    bio = models.TextField(max_length=500, default='', verbose_name='个人简介', blank=True, null=True)
    college = models.CharField(max_length=30, default='', verbose_name='学院', blank=True, null=True)
    major = models.CharField(max_length=20, default='', verbose_name='专业', blank=True, null=True)
    grade = models.CharField(max_length=20, default='', verbose_name='年级', blank=True, null=True)
    sex = models.CharField(max_length=2, default='', verbose_name='性别', blank=True, null=True)

    def __str__(self):
        return self.user_name


class Subject(models.Model):
    '''
    科目
    '''
    name = models.CharField(max_length=30, unique=True, verbose_name='科目名称')

    def __str__(self):
        return self.name


class Question(models.Model):
    '''
    问题类
    外键：科目，提问者
    属性：标题，具体描述，提问日期，浏览量，点赞量，科目，提问者
    '''
    question_title = models.CharField(verbose_name='标题', max_length=30, blank=False)
    question_text = RichTextField(verbose_name='具体描述')
    question_subject = models.ForeignKey('Subject', verbose_name='科目', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True, verbose_name='提问日期')
    page_views = models.IntegerField(default=0, verbose_name='浏览量')
    questioner = models.ForeignKey('User', verbose_name='提问者', on_delete=models.CASCADE)
    good_num = models.IntegerField(default=0, verbose_name='点赞量')

    def __str__(self):
        return self.question_title

# 获取问题详情页面的地址
    def get_absolute_url(self):
        return reverse('qas_system:question_detail', args=[self.id])


class Comment(models.Model):
    '''
    评论类
    外键：评论者，问题
    属性：评论内容，评论时间，点赞量，评论者，问题
    '''
    question = models.ForeignKey('Question', verbose_name='问题', on_delete=models.CASCADE, related_name='comments')
    comment_text = RichTextField(verbose_name='评论内容')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='评论时间')
    good_num = models.IntegerField(default=0, verbose_name='点赞量')
    # 之前的版本里没有评论者 黄海石2020年5月5日修改
    comment_person = models.ForeignKey('User', verbose_name='评论者', on_delete=models.CASCADE)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.comment_text


class Tipoff(models.Model):
    '''
    举报类
    外键：问题
    属性：举报理由，举报时间
    '''
    question = models.ForeignKey('Question', verbose_name='问题', on_delete=models.CASCADE, related_name='tipoffs')
    reason = RichTextField(verbose_name='举报理由')
    tip_date = models.DateTimeField(auto_now=True, verbose_name='举报时间')

    class Meta:
        ordering = ('tip_date',)

    def __str__(self):
        return self.reason
