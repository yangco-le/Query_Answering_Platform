from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import QuestionPostForm, CommentForm, TipOffForm, UserPageForm, UserLoginForm
from . import models, forms
from .models import Question, Subject, Comment, Tipoff, User, Good, Cgood
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages


def mainpage(request):
    '''
    首页
    :param request: 请求
    '''
    return render(request, 'mainpage.html')


def question_detail(request, id):
    '''
    问题详情页
    :param request: 请求
    :param id: 问题主键值
    '''
    question = models.Question.objects.get(id=id)
    # 每浏览一次 浏览量加一
    question.page_views += 1
    question.save(update_fields=['page_views'])
    comments = Comment.objects.filter(question=id)
    tipoffs = Tipoff.objects.filter(question=id)
    form = CommentForm()
    # 在html文件中实现：如果浏览的不是提问者，则不显示“删除问题”“修改问题”链接
    try:
        user = models.User.objects.get(id=request.session['user_id'])
        good_created = Good.objects.filter(good_question_id=id, good_by_id=request.session['user_id']).first()
    except KeyError:
        user = None
        good_created = None
    # 检查用户是否对问题点过赞，决定点赞按钮的底色
    context = {'question': question, 'comments': comments, 'tipoffs': tipoffs, 'user': user, 'form': form,
               'good_created': good_created}
    return render(request, 'question_detail.html', context)


def question_delete(request, id):
    '''
    删除问题后端
    与用户关联，用户只能删除自己创建的问题
    :param request: 请求
    :param id: 问题主键值
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
    与用户关联，登陆的用户才能创建问题
    :param request: 请求
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
            user = models.User.objects.get(id=request.session['user_id'])
            context = {'question_post_form': question_post_form, 'subjects': subjects, 'message': message, 'user': user}
            return render(request, 'create_question.html', context)
        # 如果用户请求获取数据
    else:
        subjects = models.Subject.objects.all()
        # 创建表单类实例
        question_post_form = QuestionPostForm()
        # 赋值上下文
        user = models.User.objects.get(id=request.session['user_id'])
        context = {'question_post_form': question_post_form, 'subjects': subjects, 'user': user}
        # 返回模板
        return render(request, 'create_question.html', context)


def update_question(request, id):
    '''
    修改问题网页后端
    与用户关联，用户只能修改自己创建的问题
    :param request: 请求
    :param id: 问题主键值
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
            user = models.User.objects.get(id=request.session['user_id'])
            context = {'question_post_form': question_post_form, 'subjects': subjects, 'message': message,
                       'question':question, 'user': user}
            return render(request, 'update_question.html', context)
        # 如果用户请求获取数据
    else:
        subjects = models.Subject.objects.all()
        # 创建表单类实例
        question_post_form = QuestionPostForm()
        # 赋值上下文
        user = models.User.objects.get(id=request.session['user_id'])
        context = {'question_post_form': question_post_form, 'subjects': subjects, 'question':question, 'user': user}
        # 返回模板
        return render(request, 'update_question.html', context)


def select(request):
    '''
    问题筛选
    :param request: 请求
    '''
    all_subject = Subject.objects.all()
    return render(request, 'select.html', {'all_subject': all_subject})


def selecting(request):
    '''
    问题筛选
    :param request: 请求
    '''
    try:
        a = request.POST['subject']
        b = request.POST['sequencing']
    except KeyError:
        # 如果用户没有选科目或排序方式，则重新返回问题筛选结果页面
        all_subject = Subject.objects.all()
        return render(request, 'select.html', {'all_subject': all_subject})
    return HttpResponseRedirect(reverse('qas_system:select_result', args=(int(b), int(a))))


def select_result(request, sequencing, question_subject):
    '''
    问题筛选结果页面
    :param request: 请求
    :param sequencing: 排序方式 0，1，2分别代表按浏览量降序、点赞量降序、发布时间降序排列
    :param question_subject: 科目代码
    '''
    if sequencing == 0:
        select_result_list = Question.objects.filter(question_subject_id=question_subject).order_by('-page_views')
    elif sequencing == 1:
        select_result_list = Question.objects.filter(question_subject_id=question_subject).order_by('-good_num')
    elif sequencing == 2:
        select_result_list = Question.objects.filter(question_subject_id=question_subject).order_by('-pub_date')
    else:
        # 如果sequencing为0,1,2以外的值，则返回主页
        return render(request, 'mainpage.html')
    all_subject = Subject.objects.all()
    try:
        user = models.User.objects.get(id=request.session['user_id'])
    except KeyError:
        user = None
    context = {
        'select_result_list': select_result_list,
        'sequencing': sequencing,
        'all_subject': all_subject,
        'this_subject': question_subject,
        'user': user
    }
    return render(request, 'select_result.html', context)


def all_question(request):
    '''
    浏览所有问题页面 按照时间顺序
    :param request: 请求
    '''
    all_question_list = Question.objects.all().order_by('-pub_date')
    all_subject = Subject.objects.all()
    try:
        user = models.User.objects.get(id=request.session['user_id'])
    except KeyError:
        user = None
    return render(request, 'all_question.html', {'all_question_list': all_question_list, 'all_subject': all_subject,
                                                 'user':user})


def all_question2(request, sequencing):
    '''
    浏览所有问题页面 3种排列顺序
    :param request: 请求
    :param sequencing: 排序方式 0，1，2分别代表按浏览量降序、点赞量降序、发布时间降序排列
    '''
    if sequencing == 0:
        all_question_list = Question.objects.all().order_by('-page_views')
    elif sequencing == 1:
        all_question_list = Question.objects.all().order_by('-good_num')
    elif sequencing == 2:
        all_question_list = Question.objects.all().order_by('-pub_date')
    else:
        # 如果sequencing为0,1,2以外的值，则返回主页
        return render(request, 'mainpage.html')
    all_subject = Subject.objects.all()
    try:
        user = models.User.objects.get(id=request.session['user_id'])
    except KeyError:
        user = None
    return render(request, 'all_question.html', {'all_question_list': all_question_list, 'all_subject': all_subject,
                                                 'user': user, 'sequencing': sequencing})


def question_comment(request, question_id):
    '''
    评论（问题）
    :param request: 请求
    :param question_id: 问题主键值id
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
    :param request: 请求
    :param question_id: 问题主键值id
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
    :param request: 请求
    :param question_id: 问题主键值id
    '''
    question = Question.objects.filter(id=question_id).first()
    like_query = Good.objects.filter(good_question_id=question_id, good_by_id=request.session['user_id']).first()
    if not request.session.get('is_login', None):
        # 检查是否处于登陆状态
        return redirect('/qas_system/login/')
    if like_query is not None:
        # 检查是否点过赞
        return redirect(question)
    # 处理 GET 请求
    if request.method == 'GET':
        question.good_num += 1
        question.save()
        good = Good(good_question=question, good_by=(User(id=request.session['user_id'])))
        good.save()
        return redirect(question)
    else:
        return HttpResponse("点赞仅接受GET请求。")


def comment_good(request, question_id, comment_id):
    '''
    给评论点赞
    :param request: 请求
    :param question_id: 问题主键值id
    :param comment_id: 评论主键值id
    '''
    question = Question.objects.filter(id=question_id).first()
    comment = Comment.objects.filter(id=comment_id).first()
    like_query = Cgood.objects.filter(good_comment_id=comment_id, good_by_id=request.session['user_id']).first()
    if not request.session.get('is_login', None):
        # 检查是否处于登陆状态
        return redirect('/qas_system/login/')
    if like_query is not None:
        # 检查是否点过赞
        return redirect(question)
    # 处理 GET 请求
    if request.method == 'GET':
        comment.good_num += 1
        comment.save()
        cgood = Cgood(good_comment=comment, good_by=(User(id=request.session['user_id'])))
        cgood.save()
        return redirect(question)
    else:
        return HttpResponse("点赞仅接受GET请求。")


def search(request):
    '''
    问题搜索页面
    :param request: 请求
    '''
    return render(request, 'search.html',)


def search_subject(request):
    '''
    按科目搜索问题
    :param request: 请求
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
    按关键词搜索问题
    :param request: 请求
    '''
    try:
        user = models.User.objects.get(id=request.session['user_id'])
    except KeyError:
        user = None
    sc = request.GET.get('search', None)
    context = None
    if sc:
        print(sc)
        question_list = Question.objects.filter(question_title__icontains=sc)
        context = {'question_list': question_list, 'user': user}
    return render(request, 'search_keyword.html', context)


def search_both(request):
    '''
    搜索函数，按科目和关键词搜索
    :param request: 请求
    '''
    try:
        user = models.User.objects.get(id=request.session['user_id'])
    except KeyError:
        user = None
    method = request.GET.get('type', None)
    if method == '0':

        sc = request.GET.get('search', None)
        context = None
        if sc:
            print(sc)
            question_list = Question.objects.filter(question_subject__name=sc)
            context = {'question_list': question_list, 'user': user}
        return render(request, 'search_subject.html', context)
    elif method == '1':
        sc = request.GET.get('search', None)
        context = None
        if sc:
            print(sc)
            question_list = Question.objects.filter(question_title__icontains=sc)
            context = {'question_list': question_list, 'user': user}
        return render(request, 'search_keyword.html', context)
    else:
        # 如果method为0,1以外的值，则返回主页
        return render(request,  'mainpage.html')


def userpage(request):
    '''
    显示用户主页
    :param request: 请求
    '''
    # 徐哲修改了id的传入方式
    try:
        user = models.User.objects.get(id=request.session['user_id'])
    except KeyError:
        return HttpResponse("请先登录！")
    if request.method == "GET":
        return render(request, 'personal_homepage.html', {'user': user})


def userpage_edit(request):
    '''
    个人信息编辑
    :param request: 请求
    '''
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
    '''
    查看参与的讨论，分为提问和回答
    :param request: 请求
    '''
    try:
        user = User.objects.get(id=request.session['user_id'])
    except KeyError:
        return HttpResponse("请先登录！")
    my_ask = Question.objects.filter(questioner_id=request.session['user_id']).order_by('-pub_date')
    my_answer_detail = Comment.objects.filter(comment_person=request.session['user_id']).order_by('-pub_date')
    return render(request, 'personal_related_discuss.html',
                  {'my_ask': my_ask, 'my_answer_detail': my_answer_detail, 'user': user})


def user_login(request):
    '''
    用户登陆
    在login.html中添加到新用户注册的路径
    :param request: 请求
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
                return render(request, 'login.html', locals())
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.user_name
                return redirect('/qas_system/userpage/')
            else:
                message = '密码不正确！'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())
    login_form = forms.UserLoginForm()
    return render(request, 'login.html', locals())


def user_register(request):
    '''
    用户注册
    :param request: 请求
    '''
    if request.session.get('is_login', None):
        return redirect('/qas_system/')

    if request.method == 'POST':
        register_form = forms.UserRegisterForm(request.POST)
        message = ""
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            message = "Good job"

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
    :param request: 请求
    '''
    if not request.session.get('is_login', None):
        # 检查是否处于登陆状态
        return redirect('/qas_system/login/')
    request.session.flush()
    return redirect('/qas_system/login/')


def userpage_collect_question(request):
    '''
    查看收藏的问题
    :param request: 请求
    '''
    try:
        user = User.objects.get(id=request.session['user_id'])
    except KeyError:
        return HttpResponse("请先登录！")
    my_collect = user.collect_question.all()
    return render(request, 'personal_collect_question.html', {'my_collect': my_collect, 'user': user})


def question_fav(request, question_id):
    '''
    收藏问题
    :param request: 请求
    :param question_id: 问题主键值id
    '''
    # 根据 id 获取需要收藏的文章
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'GET':
        # 检查是否处于登陆状态
        if not request.session.get('is_login', None):
            return redirect('/qas_system/login/')

        u = User.objects.get(id=request.session['user_id'])
        cq = u.collect_question.all()
        lis = [i.id for i in cq]

        if question_id in lis:
            #  如果记录已经存在，那么表示用户取消收藏
            q = Question.objects.get(id=question_id)
            u.collect_question.remove(q)
            messages.error(request, '收藏')
        else:
            q = Question.objects.get(id=question_id)
            u.collect_question.add(q)
            messages.error(request, '已收藏')

        return redirect(question)

    else:
        return HttpResponse("收藏仅接受GET请求。")