'''
转接urls
'''


from django.urls import path

from . import views

urlpatterns = [
    path('', views.test_ly),
    path('createq/', views.create_question),  # 跳转创建问题页面
]