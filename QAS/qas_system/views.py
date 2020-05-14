from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import QuestionPostForm, CommentForm, TipOffForm, UserPageForm, UserLoginForm
from . import models, forms
from .models import Question, Subject, Comment, Tipoff, User
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
# Create your views here.


def test_homepage_ly(request):
    '''
    测试主页
    author:liyang
    '''
    return render(request, 'test_ly.html')


def test_questionpage_ly(request, id):
    '''
    测试问题页
    author:liyang
    '''
    # 2020年5月11日 黄海石有改动

    question = models.Question.objects.get(id=id)

    # 每浏览一次 浏览量加一
    question.page_views += 1
    question.save(update_fields=['page_views'])

    comments = Comment.objects.filter(question=id)
    tipoffs = Tipoff.objects.filter(question=id)

    # 在html文件中实现：如果浏览的不是提问者，则不显示“删除问题”“修改问题”链接
    user = models.User.objects.get(id=request.session['user_id'])
    context = {'question': question, 'comments': comments, 'tipoffs': tipoffs, 'user': user}

    return render(request, 'question_detail.html', context)


def question_delete(request, id):
    '''
    删除问题后端
    author:liyang
    # 徐哲修改：与用户关联，用户只能删除自己创建的问题
    '''
    # 根据 id 获取需要删除的文章
    question = models.Question.objects.get(id=id)
    # 检查是否处于登陆状态
    if not request.session.get('is_login', None):
        return redirect('/qas_system/login/')
    if question.questioner.id != request.session['user_id']:
        return HttpResponse("你只能删除自己创建的问题。")
    # 调用.delete()方法删除文章
    question.delete()
    return redirect("/qas_system/")


def create_question(request):
    '''
    创建问题网页后端
    author：liyang
    # 徐哲修改：与用户关联，登陆的用户才能创建问题
    '''
    if not request.session.get('is_login', None):
        # 检查是否处于登陆状态
        return redirect('/qas_system/login/')
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        title = request.POST.get('question_title')
        text = request.POST.get('question_text')
        subject = request.POST.get('question_subject')
        # 判断提交的数据是否满足模型的要求
        if title.strip() and text.strip() and subject.strip():
            # 保存数据，但暂时不提交到数据库中
            new_q = models.Question()
            new_q.question_title = title
            new_q.question_text = text
            new_q.question_subject = models.Subject.objects.get(name=subject)
            new_q.questioner = (User(id=request.session['user_id']))
            new_q.pub_date = timezone.now()
            new_q.save()
            # print(new_q.question_text)
            # 完成后返回到文章列表
            return redirect('/qas_system/question/'+str(new_q.id))
        # 如果数据不合法，返回错误信息
        else:
            subjects = models.Subject.objects.all()
            question_post_form = QuestionPostForm()
            message = "表单内容有误，请重新填写。"
            context = {'question_post_form': question_post_form, 'subjects': subjects, 'message': message}
            return render(request, 'create_question.html', context)
        # 如果用户请求获取数据
    else:
        subjects = models.Subject.objects.all()
        # 创建表单类实例
        question_post_form = QuestionPostForm()
        # 赋值上下文
        context = {'question_post_form': question_post_form, 'subjects': subjects}
        # 返回模板
        return render(request, 'create_question.html', context)


def update_question(request, id):
    '''
    修改问题网页后端
    author：liyang
    # 徐哲修改：与用户关联，用户只能修改自己创建的问题
    '''
    question = models.Question.objects.get(id=id)
    if not request.session.get('is_login', None):
        # 检查是否处于登陆状态
        return redirect('/qas_system/login/')
    if question.questioner.id != request.session['user_id']:
        return HttpResponse("你只能修改自己创建的问题。")
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        title = request.POST.get('question_title')
        text = request.POST.get('question_text')
        subject = request.POST.get('question_subject')
        # 判断提交的数据是否满足模型的要求
        if title.strip() and text.strip() and subject.strip():
            question.question_title = title
            question.question_text = text
            question.question_subject = models.Subject.objects.get(name=subject)
            question.save()
            # print(new_q.question_text)
            # 完成后返回到文章列表
            return redirect('/qas_system/question/'+str(question.id))
        # 如果数据不合法，返回错误信息
        else:
            subjects = models.Subject.objects.all()
            question_post_form = QuestionPostForm()
            message = "表单内容有误，请重新填写。"
            context = {'question_post_form': question_post_form, 'subjects': subjects, 'message': message, 'question':question}
            return render(request, 'update_question.html', context)
        # 如果用户请求获取数据
    else:
        subjects = models.Subject.objects.all()
        # 创建表单类实例
        question_post_form = QuestionPostForm()
        # 赋值上下文
        context = {'question_post_form': question_post_form, 'subjects': subjects, 'question':question}
        # 返回模板
        return render(request, 'update_question.html', context)


def select(request):
    # 问题筛选页面
    # 黄海石
    all_subject = Subject.objects.all()
    return render(request, 'select.html', {'all_subject': all_subject})


def selecting(request):
    # 黄海石
    try:
        a = request.POST['subject']
        b = request.POST['sequencing']
    except KeyError:
        # 如果用户没有选科目或排序方式，则重新返回问题筛选结果页面
        all_subject = Subject.objects.all()
        return render(request, 'select.html', {'all_subject': all_subject})
    return HttpResponseRedirect(reverse('qas_system:select_result', args=(int(b), int(a))))


def select_result(request, sequencing, question_subject):
    # 问题筛选结果页面
    # 黄海石
    if sequencing == 0:
        select_result_list = Question.objects.filter(question_subject_id=question_subject).order_by('-page_views')
    elif sequencing == 1:
        select_result_list = Question.objects.filter(question_subject_id=question_subject).order_by('-good_num')
    elif sequencing == 2:
        select_result_list = Question.objects.filter(question_subject_id=question_subject).order_by('-pub_date')
    else:
        # 如果sequencing为0,1,2以外的值，则返回问题筛选结果页面
        all_subject = Subject.objects.all()
        return render(request, 'select.html', {'all_subject': all_subject})
    context = {
        'select_result_list': select_result_list,
    }
    return render(request, 'select_result.html', context)


def all_question(request):
    # 浏览所有问题页面 按照时间顺序
    # 黄海石
    all_question_list = Question.objects.all().order_by('-pub_date')
    return render(request, 'all_question.html', {'all_question_list': all_question_list})


def question_comment(request, question_id):
    '''
    评论（问题）
    author: 徐哲
    '''
    question = get_object_or_404(Question, id=question_id)
    if not request.session.get('is_login', None):
        # 检查是否处于登陆状态
        return redirect('/qas_system/login/')

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.question = question
            new_comment.comment_person = (User(id=request.session['user_id']))
            new_comment.save()
            return redirect(question)
        else:
            return HttpResponse("内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")


def question_tipoff(request, question_id):
    '''
    举报问题
    author: 徐哲
    '''
    question = get_object_or_404(Question, id=question_id)
    if not request.session.get('is_login', None):
        # 检查是否处于登陆状态
        return redirect('/qas_system/login/')

    # 处理 POST 请求
    if request.method == 'POST':
        tipoff_form = TipOffForm(request.POST)
        if tipoff_form.is_valid():
            new_tipoff = tipoff_form.save(commit=False)
            new_tipoff.question = question
            new_tipoff.tipoff_person = (User(id=request.session['user_id']))
            new_tipoff.save()
            return redirect(question)
        else:
            return HttpResponse("内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("举报仅接受POST请求。")


def question_good(request, question_id):
    '''
    给问题点赞
    author: 徐哲
    '''
    question = get_object_or_404(Question, id=question_id)
    if not request.session.get('is_login', None):
        # 检查是否处于登陆状态
        return redirect('/qas_system/login/')
    # 处理 POST 请求
    if request.method == 'POST':
        question.good_num += 1
        question.save()
        return redirect(question)
    else:
        return HttpResponse("点赞仅接受POST请求。")


def search(request):
    '''
    # 问题搜索页面
    # 尹俊同
    '''
    return render(request, 'search.html',)


def search_subject(request):
    '''
    # 按科目搜索问题
    # 尹俊同
    '''
    sc = request.GET.get('search', None)
    context = None
    if sc:
        print(sc)
        question_list = Question.objects.filter(question_subject__name=sc)
        context = {'question_list': question_list}
    return render(request, 'search_subject.html', context)


def search_keyword(request):
    '''
    # 按关键词搜索问题
    # 尹俊同
    '''
    sc = request.GET.get('search', None)
    context = None
    if sc:
        print(sc)
        question_list = Question.objects.filter(question_title__icontains=sc)
        context = {'question_list': question_list}
    return render(request, 'search_keyword.html', context)


def userpage(request):
    '''
    显示用户主页
    郦洋
    '''
    # 徐哲修改了id的传入方式
    user = models.User.objects.get(id=request.session['user_id'])
    if request.method == "GET":
        return render(request, 'personal_homepage.html', {'user': user})


def userpage_edit(request):
    '''
    个人信息编辑
    郦洋
    '''
    # 徐哲修改了id的传入方式
    user = models.User.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        user_form = UserPageForm(request.POST, request.FILES)
        if user_form.is_valid():
            # 取得清洗后的合法数据
            user_cd = user_form.cleaned_data
            user.bio = user_cd['bio']
            user.sex = user_cd['sex']
            user.grade = user_cd['grade']
            user.college = user_cd['college']
            user.major = user_cd['major']
            user.email = user_cd['email']
            if 'avatar' in request.FILES:
                user.avatar = user_cd["avatar"]
            user.save()
            # 带参数的 redirect()
            return redirect('/qas_system/userpage/')
        else:
            return HttpResponse("信息输入有误。请重新输入~")
    else:
        user_form = UserPageForm()
        # 赋值上下文
        context = {'user_form': user_form, 'user': user}
        # 返回模板
        return render(request, 'personal_homepage_edit.html', context)


def userpage_related_discuss(request):
    # 查看参与的讨论，分为提问和回答
    # 黄海石
    # 徐哲修改了id的传入方式
    my_ask = Question.objects.filter(questioner_id=request.session['user_id']).order_by('-pub_date')
    my_answer_detail = Comment.objects.filter(comment_person=request.session['user_id']).order_by('-pub_date')
    return render(request, 'personal_related_discuss.html',
                  {'my_ask': my_ask, 'my_answer_detail': my_answer_detail})


def user_login(request):
    '''
    用户登陆
    徐哲
    在login.html中添加到新用户注册的路径 尹俊同
    '''
    if request.session.get('is_login', None):  # 防止重复登录
        return redirect('/qas_system/')
    if request.method == "POST":
        login_form = forms.UserLoginForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(user_name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login_new.html', locals())
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.user_name
                return redirect('/qas_system/userpage/')
            else:
                message = '密码不正确！'
                return render(request, 'login_new.html', locals())
        else:
            return render(request, 'login_new.html', locals())
    login_form = forms.UserLoginForm()
    return render(request, 'login_new.html', locals())


def user_register(request):
    '''
    用户注册
    尹俊同
    '''
    if request.session.get('is_login', None):
        return redirect('/qas_system/')

    if request.method == 'POST':
        register_form = forms.UserRegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(user_name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'register.html', locals())

                new_user = models.User()
                new_user.user_name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/qas_system/login/')
        else:
            return render(request, 'register.html', locals())
    register_form = forms.UserRegisterForm()
    return render(request, 'register.html', locals())


def user_logout(request):
    '''
    用户登出
    徐哲
    '''
    if not request.session.get('is_login', None):
        # 检查是否处于登陆状态
        return redirect('/qas_system/login/')
    request.session.flush()
    return redirect('/qas_system/login/')


def userpage_collect_question(request):
    # 查看收藏的问题
    # 黄海石
    u = User.objects.get(id=request.session['user_id'])
    my_collect = u.collect_question.all()
    return render(request, 'personal_collect_question.html', {'my_collect': my_collect})