# author: liyang、xuzhe

# 引入表单类
from django import forms
# 引入文章、用户模型
from .models import Question, User
# 引入评论、举报模型
from .models import Comment, Tipoff


# 写文章的表单类
class QuestionPostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = Question
        # 定义表单包含的字段
        fields = ('question_title', 'question_text', 'question_subject')


# 评论的表单类
class CommentForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = Comment
        # 定义表单包含的字段
        fields = ['comment_text']


class TipOffForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = Tipoff
        # 定义表单包含的字段
        fields = ['reason']


class UserPageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'bio', 'sex', 'grade', 'college', 'major', 'email')