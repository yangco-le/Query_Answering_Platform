# 黄海石
from django.test import TestCase, Client
from django.urls import resolve, reverse
from .views import *
from .models import *
from sqlite3 import IntegrityError as Integrity1Error
from django.db.utils import IntegrityError as Integrity2Error


class TestUrl(TestCase):
    # 检测请求成功后，django是否返回了正确对应的视图函数
    def test_url_mainpage(self):
        view = resolve('/qas_system/')  # 从url路径得到对应的路径名字
        self.assertEqual(view.func, mainpage)  # 对应的函数

    def test_url_create_question(self):
        view = resolve('/qas_system/createq/')
        self.assertEqual(view.func, create_question)

    # def test_url_update_question(self):
    #    view = resolve('/qas_system/updateq/7/')
    #    self.assertEqual(view.func, update_question)

    def test_url_question_detail(self):
        view = resolve('/qas_system/question/7/')
        self.assertEqual(view.func, test_questionpage_ly)

    #

    def test_url_select(self):
        view = resolve('/qas_system/select/')
        self.assertEqual(view.func, select)

    def test_url_selecting(self):
        view = resolve('/qas_system/selecting/')
        self.assertEqual(view.func, selecting)

    def test_url_select_result(self):
        view = resolve('/qas_system/select/0/4/')
        self.assertEqual(view.func, select_result)

    def test_url_all_question(self):
        view = resolve('/qas_system/all_question/')
        self.assertEqual(view.func, all_question)

    def test_url_all_question2(self):
        view = resolve('/qas_system/all_question/2/')
        self.assertEqual(view.func, all_question2)

    ####

    def test_url_search(self):
        view = resolve('/qas_system/search/')
        self.assertEqual(view.func, search)

    def test_url_search_subject(self):
        view = resolve('/qas_system/search_subject/')
        self.assertEqual(view.func, search_subject)

    def test_url_search_keyword(self):
        view = resolve('/qas_system/search_keyword/')
        self.assertEqual(view.func, search_keyword)

    def test_url_login(self):
        view = resolve('/qas_system/login/')
        self.assertEqual(view.func, user_login)

    def test_url_register(self):
        view = resolve('/qas_system/register/')
        self.assertEqual(view.func, user_register)

    def test_url_logout(self):
        view = resolve('/qas_system/logout/')
        self.assertEqual(view.func, user_logout)

    def test_url_logout(self):
        view = resolve('/qas_system/logout/')
        self.assertEqual(view.func, user_logout)

    #####


class TestModel(TestCase):
    def setUp(self):
        pass

    def test_User(self):
        # 测试user_name的unique=True
        u1 = User(user_name='1a')
        u1.save()
        with self.assertRaises(Integrity2Error):
            with self.assertRaises(Integrity1Error):
                User.objects.create(user_name='1a')

    def test_Question(self):
        q = Question()
        self.assertEqual(q.page_views, 0)

    def test_Comment(self):
        c = Comment(comment_text='abc')
        self.assertEqual(c.comment_text, 'abc')

    def tearDown(self):
        pass


class TestView(TestCase):
    def test_select(self):
        c = Client()
        response = c.get(reverse('qas_system:select'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'select.html')

    def test_select_result(self):
        c = Client()
        response = c.get(reverse('qas_system:select_result',kwargs={'sequencing': 1, 'question_subject': 7}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'select_result.html')
        response2 = c.get(reverse('qas_system:select_result', kwargs={'sequencing': 5, 'question_subject': 7}))
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'mainpage.html')

    def test_selecting(self):
        c = Client()
        response = c.post(reverse('qas_system:selecting'), {'subject': 7, 'sequencing': 2})
        self.assertEqual(response.status_code, 302)
