'''
转接urls
author:liyang
'''


from django.urls import path

from . import views

urlpatterns = [
    path('', views.test_homepage_ly),
    path('createq/', views.create_question),  # 跳转创建问题页面
    path('question/<int:id>/', views.test_questionpage_ly),
    path('question-delete/<int:id>/', views.question_delete),
]