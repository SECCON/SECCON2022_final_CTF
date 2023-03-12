import mimetypes
import shutil
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from ..logic import common
from django.utils import timezone
from witchquiz.models import Question
from witchquiz.settings import PROBLEM_PATH
from wsgiref.util import FileWrapper
import datetime

def download(request, stage):
    currentTime = timezone.now()
    questions = Question.objects.filter(pk=stage) # ToDo Add Problem
    if len(questions) != 1:
        return HttpResponse("stage not found")
    question = questions[0]
    if common.getQuestionStatus(question, currentTime) == common.QuestionStatus.YET:
        return HttpResponse("this problem is not active yet")

    filename = question.content + ".py"
    with open((PROBLEM_PATH / filename), 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=' + "problem_" + str(stage) + ".py"
    return response