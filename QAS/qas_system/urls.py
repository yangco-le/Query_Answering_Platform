'''
转接urls
author:liyang
'''


from django.urls import path

from . import views

urlpatterns = [
    path('', views.test_homepage_ly),
    path('createq/', views.create_question),  # 跳转创建问题页面
    path('updateq/<int:id>', views.update_question), # 问题修改页面
    path('question/<int:id>/', views.test_questionpage_ly, name='question_detail'),
    path('question-delete/<int:id>/', views.question_delete),
    path('select/', views.select, name='select'),  # 问题筛选页面
    path('selecting/', views.selecting, name='selecting'),
    path('select/<int:sequencing>/<int:question_subject>/', views.select_result,  # 问题筛选结果页面 sequencing为0,1,2
         name='select_result'),  # 分别代表按浏览量降序、点赞量降序、发布时间降序排列
    path('all_question/', views.all_question),  # 浏览所有问题 按照时间顺序排列
    path('question-comment/<int:question_id>/', views.question_comment, name='question_comment'), # 问题评论
    path('question-tipoff/<int:question_id>/', views.question_tipoff, name='question_tipoff'), # 举报问题
]