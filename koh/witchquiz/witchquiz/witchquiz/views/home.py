from django.http import HttpResponse
from django.views.generic import View
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authtoken.models import Token
import logging
from witchquiz.models import Question, Submission, RoundScore
from django.utils import timezone
from ..logic import common
from collections import ChainMap
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import logging
from datetime import datetime
from django.utils.timezone import make_aware

class View(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = ''
    def get(self, request):

        template = loader.get_template('witchquiz/home.html')
        user = self.request.user
        token = Token.objects.get(user=user)
        questions = Question.objects.all()

        questionView = []
        currentTime = timezone.now()
        rankings = []
        scoreSum = {}

        for i, question in enumerate(questions):
            stage = i+1
            status = common.getQuestionStatus(question, currentTime)
            questionView.append({"stage": stage, "status":str(status), "starttime":question.starttime, "endtime":question.starttime + question.tickcount * question.tickinterval})
        
            ranking = common.getRanking(stage)
            for score in ranking:
                id = score['userid']
                if id not in scoreSum:
                    scoreSum[id] = {'username': score['username'], 'value': 0}
                scoreSum[id]['value'] += score['stageScore']
            rankings.append({'stage': stage, 'ranking': ranking})
        
        scoreSumView = list(sorted(map(lambda x: x[1], scoreSum.items()), key= lambda x:x['value'], reverse=True))
        for i in range(len(scoreSumView)):
            scoreSumView[i]['rank'] = i+1

        rss = RoundScore.objects.all().select_related().order_by('-score')
        roundScoreView = {}

        for rs in rss:
            if rs.round not in roundScoreView:
                roundScoreView[rs.round] = {'stage': rs.questionid, 'tick': rs.tick ,'content':[]}

            roundScoreView[rs.round]['content'].append({
                "round": rs.round,
                "rank": rs.rank,
                "username": rs.user.username,
                "score": rs.score,
            })
        
        return HttpResponse(template.render({'username': user.username, 'token': token.key, 'questions': questionView, 'rankings': rankings, 'scoreSum': scoreSumView, 'roundScore': list(reversed(roundScoreView.items()))}, request))