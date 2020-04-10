from django.db import models

# Create your models here.


class User(models.Model):
    '''
    用户
    属性：用户名，密码
    '''
    user_name = models.CharField(verbose_name='用户名', max_length=30, blank=False)
    password = models.CharField(verbose_name='密码', maxlength=30, blank=False)


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
    question_text = models.TextField(verbose_name='具体描述')
    question_subject = models.ForeignKey('Subject', verbose_name='科目', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True, verbose_name='提问日期')
    page_views = models.IntegerField(default=0, verbose_name='浏览量')
    questioner = models.ForeignKey('User', verbose_name='提问者', on_delete=models.CASCADE)
    good_num = models.IntegerField(default=0, verbose_name='点赞量')

    def __str__(self):
        return self.question_title


class Comment(models.Model):
    '''
    评论类
    外键：评论者，问题
    属性：评论内容，评论时间，点赞量，评论者，问题
    '''
    reviewer = models.ForeignKey('User', verbose_name='评论者', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', verbose_name='问题', on_delete=models.CASCADE)
    comment_text = models.TextField(verbose_name='评论内容')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='评论时间')
    good_num = models.IntegerField(default=0, verbose_name='点赞量')

    def __str__(self):
        return self.comment_text


