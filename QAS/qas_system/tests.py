from django.test import TestCase, Client, SimpleTestCase
from django.urls import resolve, reverse
from .views import *
from .models import *
from .forms import *
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
        # 测试评论的创建
        c = Comment(question=Question(id=3), comment_text='abc', pub_date='2020-02-02 20:20:20', comment_person=User(id=5))
        self.assertEqual(c.comment_text, 'abc')
        self.assertEqual(c.pub_date, '2020-02-02 20:20:20')
        self.assertEqual(c.question.id, 3)
        self.assertEqual(c.comment_person.id, 5)

    def test_Good(self):
        # 测试问题赞的创建
        g = Good(good_by=User(user_name='lex'), good_question=Question(id=2))
        self.assertEqual(g.good_by.user_name, 'lex')
        self.assertEqual(g.good_question.id, 2)

    def test_Cgood(self):
        # 测试评论赞的创建
        cg = Cgood(good_by=User(user_name='dio'), good_comment=Comment(id=8))
        self.assertEqual(cg.good_by.user_name, 'dio')
        self.assertEqual(cg.good_comment.id, 8)

    def tearDown(self):
        pass


class TestSelect(TestCase):
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


class TestQuestion(TestCase):
    # 测试问题相关函数
    def setUp(self):
        pass

    def test_create_question(self):
        test_question1 = {'question_title': 'a', 'question_text': 'b', 'question_subject': 'c'}
        response = self.client.post('/qas_system/createq/', data=test_question1)
        self.assertEqual(response.status_code, 302)

    def test_update_question(self):
        Subject.objects.create(name='c')
        User.objects.create(user_name='dio')
        Question.objects.create(id=3, question_title='a', question_text='b',
                                question_subject=Subject.objects.get(name='c'),
                                questioner=User.objects.get(user_name='dio'))
        test_question2 = {'question_title': 'd', 'question_text': 'e', 'question_subject': 'f'}
        q = Question.objects.get(id=3)
        response = self.client.post('/qas_system/updateq/3', data=test_question2)
        self.assertEqual(response.status_code, 302)


'''
class TestRegisterLogin(TestCase):
    # 测试登录和注册相关
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('qas_system:login')
        self.register_url = reverse('qas_system:register')
        self.user1 = User.objects.create(user_name='user1', password='user1')

    def test_login(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'xxx.html')

        question = Question.objects.create(questioner=self.user1, name='question1')
        response = self.client.post(self.register_url, {'': '', '': '', '': ''})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user1.user_name, 'user1')

        question1 = Question.objects.create(question_title='hahaha', questioner='user1')
        response = self.client.delete(self.login_url, )

        url = reverse('qas_system:logout')
        response = self.client.post(url, {'question_title': 'question2', '': ''})

        question2 = Question.objects.get(id=1)
        self.assertEqual(question2.question_title, 'question2')
'''


class TestForms(SimpleTestCase):

    def test_form_UserRegisterForm_data_not_full(self):
        form = UserRegisterForm(data={'username': 'user1', 'password1': 'user1', 'password2': 'user1'})
        self.assertFalse(form.is_valid())

    def test_form_UserRegisterForm_no_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)

    def test_form_UserLoginForm_no_captcha(self):
        form = UserLoginForm(data={'username': 'user1', 'password': 'user1'})
        self.assertFalse(form.is_valid())

    def test_form_UserPageForm_not_exist(self):
        form = UserPageForm(data={'avatar': '桐谷和人', 'bio': '随便添加的用户', 'sex': '男', 'grade': '大二',
                                  'college': '电子信息与电气工程学院', 'major': '信息安全', 'email': 'None'})
        self.assertFalse(form.is_valid())

    def test_form_UserPageForm_initial(self):
        form = UserPageForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 7)
