from django.http import HttpResponse
from django.views.generic import View
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authtoken.models import Token
from witchquiz.models import Submission, Question, RoundStageTickTime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from ..logic import common
import datetime
import logging
from django.db.models import Max
from witchquiz.settings import ROUND_DELTA

logger = logging.getLogger(__name__)

class View(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = ''

    def get(self, request, stage=-1):
        template = loader.get_template('witchquiz/stage.html')
        user = self.request.user
        token = Token.objects.get(user=user)
        currentTime = timezone.now()
        questions = Question.objects.filter(pk=stage) # ToDo Add Problem
        if len(questions) != 1:
            return HttpResponse("stage not found")
        question = questions[0]

        tick = common.getCurrentTick(question, currentTime)
        status = common.getQuestionStatus(question, currentTime)
        if status == common.QuestionStatus.YET:
            return HttpResponse("stage is not started yet!!!")

        roundcand = RoundStageTickTime.objects.filter(stage=stage, time__lt=(currentTime + ROUND_DELTA)).order_by('-time')
        if len(roundcand) < 1:
            round = -1
            roundTickStart = 1
            roundTickEnd = 1
        else:
            round = roundcand[0].round
            roundTickStart = roundcand[0].tick - (ROUND_DELTA // question.tickinterval) + 1
            roundTickEnd = roundcand[0].tick 

        questionMetadata = {
            "currentRound": round,
            "roundTickStart": roundTickStart,
            "roundTickEnd": roundTickEnd,
            "currentTime": currentTime,
            "tickInterval": question.tickinterval,
            "currentTick": tick,
            "nextTickTime": (tick) * question.tickinterval + question.starttime,
            "startTime": question.starttime,
            "endTime": question.starttime + question.tickinterval * (question.tickcount+1),
            "tickCount": question.tickcount,
            "staticFileName": "download/" + str(stage),
            "status": str(status),
        }

        submissions = Submission.objects.filter(user=user, stage=stage).order_by('-submitTick')

        submissionScores = {}

        for submission in submissions:
            tick = submission.tick
            data = {
                "tick": tick,
                "score": submission.score,
            }
            submissionScores[tick] = data
        
        rankingData = common.getRanking(stage)
        
        return HttpResponse(template.render({'stage': stage, 'username': user.username, 'token': token.key, 'metadata': questionMetadata, 'submissions': submissionScores, 'rankingData': rankingData}, request))