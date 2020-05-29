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

    def test_url_question_detail(self):
        view = resolve('/qas_system/question/7/')
        self.assertEqual(view.func, question_detail)

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
        response2 = c.post(reverse('qas_system:selecting'), {'subject': 7})
        self.assertEqual(response2.status_code, 200)
        response3 = c.post(reverse('qas_system:selecting'), {'sequencing': 2})
        self.assertEqual(response3.status_code, 200)


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


class TestComment(TestCase):
    # 测试评论、点赞函数（举报功能结构类似，无需重复测试）
    def setUp(self):
        Subject.objects.create(name='c')
        User.objects.create(user_name='dio')
        Question.objects.create(id=3, question_title='a', question_text='b',
                                question_subject=Subject.objects.get(name='c'),
                                questioner=User.objects.get(user_name='dio'))

    def test_question_comment(self):
        test_comment = {'comment_text': 'text'}
        response = self.client.post('/qas_system/question-comment/3', data=test_comment)
        self.assertEqual(response.status_code, 301)

    def test_question_good(self):
        response = self.client.get('/qas_system/question-good/3')
        self.assertEqual(response.status_code, 301)


class TestRegisterLogin(TestCase):
    # 测试登录和注册相关
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('qas_system:login')
        self.register_url = reverse('qas_system:register')
        self.logout_url = reverse('qas_system:logout')

    def test_register(self):
        user1 = {'username': 'user1', 'password1': 'user1', 'password2': 'user2',
                 'email': 'user1@qq.com', 'sex': '男', 'captcha': ''}
        response = self.client.post(self.register_url, data=user1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login(self):
        user2 = {'user_name': 'user2', 'password': 'user2', 'captcha': ''}
        response = self.client.post(self.login_url, data=user2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        return redirect('/qas_system/login/')


class TestForms(SimpleTestCase):
    def test_form_UserRegisterForm_empty(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)

    def test_form_UserRegisterForm_data_not_full(self):
        form = UserRegisterForm(data={'username': 'user1', 'password1': 'user1', 'password2': 'user1'})
        self.assertFalse(form.is_valid())

    def test_form_UserLoginForm_empty(self):
        form = UserLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_form_UserPageForm_empty(self):
        form = UserPageForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_form_QuestionPostForm_empty(self):
        form = QuestionPostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_form_CommentForm(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_form_TipOffForm(self):
        form = TipOffForm(data={})
        self.assertFalse((form.is_valid()))
        self.assertEqual(len(form.errors), 1)
