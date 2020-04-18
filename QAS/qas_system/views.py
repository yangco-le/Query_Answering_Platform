from django.shortcuts import render, redirect
from . import models
from django.utils import timezone
# Create your views here.


def test_ly(request):
    return render(request, 'test_ly.html')


def create_question(request):
    '''
    创建问题网页后端
    author：郦洋
    '''
    if request.method == "POST":
        title = request.POST.get('title')
        text = request.POST.get('text')
        subject = request.POST.get('subject')
        if title.strip() and text.strip() and subject.strip():  # 确保都不为空
            # 确保科目在数据库中
            try:
                original_subject = models.Subject.objects.get(name=subject)
            except:
                message = '科目不存在！请填写正确科目名!'
                return render(request, 'create_question.html', {'message': message})
            new_q = models.Question()
            new_q.question_title = title
            new_q.question_text = text
            new_q.question_subject = original_subject
            new_q.questioner = models.User.objects.get(user_name='anonymity')  # 暂时认定只有一个匿名用户
            new_q.pub_date = timezone.now()
            new_q.save()
            # print(new_q.question_text)
            return redirect('/qas_system/')

    return render(request, 'create_question.html')
