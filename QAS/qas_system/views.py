from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import QuestionPostForm
from . import models
from .models import Question, Subject
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
    question = models.Question.objects.get(id=id)
    context = {'question': question}
    return render(request, 'test_ly2.html', context)


def question_delete(request, id):
    '''
    删除问题后端
    author:liyang
    '''
    # 根据 id 获取需要删除的文章
    question = models.Question.objects.get(id=id)
    # 调用.delete()方法删除文章
    question.delete()
    return redirect("/qas_system/")


def create_question(request):
    '''
    创建问题网页后端
    author：liyang
    '''
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
            new_q.questioner = models.User.objects.get(user_name='anonymity')  # 暂时认定只有一个匿名用户
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
