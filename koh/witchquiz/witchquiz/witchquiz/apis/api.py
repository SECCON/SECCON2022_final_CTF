from typing import Optional

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import datetime
from django.utils import timezone
from django.db import DatabaseError, transaction
from witchquiz.models import Question, Submission
from rest_framework import status
from ..logic import common

from ..quiz.iproblem import IProblem
from ..quiz.problemlist import problemClasses
import logging
import time

logger = logging.getLogger(__name__)

class QuizData:
    def __init__(self,pk:int, starttime: datetime, tickcount: datetime, tickinterval: int, content: IProblem):
        self.pk = pk
        self.starttime = starttime
        self.tickcount = tickcount
        self.tickinterval = tickinterval
        self.content = content

# ViewSets define the view behavior.
# sample: curl 'http://127.0.0.1:8000/api/quiz/' -H 'Authorization: Token 6fd9df8a54c6a21e5162e71b7b2253412b588a66'
class QuizViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user

        datas = json.loads(request.body)
        if 'stage' not in datas:
            return Response({"error": "stage field is required"}, status.HTTP_400_BAD_REQUEST)
        if 'tick' not in datas:
            return Response({"error": "tick field is required"}, status.HTTP_400_BAD_REQUEST)

        stage = self.__to_int(datas['stage'])
        tick = self.__to_int(datas['tick'])

        submissions = Submission.objects.filter(user=user,stage=stage,tick=tick)
        if len(submissions) == 0:
            return Response({"error": "not found"},status=status.HTTP_404_NOT_FOUND)
        submission = submissions[0]
        
        resp = {}
        resp['tick'] = submission.tick
        resp['stage'] = submission.stage
        resp['score'] = submission.score

        return Response(resp)
    
    def post(self, request, format=None):
        currentTime = timezone.now()
        logger.info(f"{request.user}: {request.body}")

        try:
            datas = json.loads(request.body)
        except:
            return Response({"error": "json parse error"}, status.HTTP_400_BAD_REQUEST)

        if 'answer' not in datas:
            return Response({"error": "answer field is required"}, status.HTTP_400_BAD_REQUEST)
        if 'stage' not in datas:
            return Response({"error": "stage field is required"}, status.HTTP_400_BAD_REQUEST)

        answer = self.__answer_to_int(datas['answer'])
        stage = self.__to_int(datas['stage'])

        question, reason = self.__get_active_question(stage, currentTime)
        if question is None:
            return Response({"error":reason}, status.HTTP_503_SERVICE_UNAVAILABLE)

        currentTick = common.getCurrentTick(question, currentTime)

        givenTick = -1
        if 'tick' not in datas:
            givenTick = currentTick
        else:
            givenTick = self.__to_int(datas['tick'])

        if 1 > givenTick or givenTick > currentTick:
            return Response({"error": f"tick must be 1 <= tick < {currentTick}(current tick), given: {givenTick}"}, status=status.HTTP_400_BAD_REQUEST)

        sub = Submission.objects.filter(user=request.user, tick=givenTick, stage=stage)
        if sub.count() > 0:
            return Response({"error": f"tick {givenTick} has beed submitted."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        sub = Submission.objects.filter(user=request.user, submitTick=currentTick, stage=stage)
        if sub.count() > 0:
            return Response({"error": "You can only submit once every 5 seconds(1tick)"}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        score = question.content.score(givenTick, answer)

        f = False
        for i in range(5):
            try:
                with transaction.atomic():
                    logger.info(f"{request.user}'s score: tick={givenTick} stage={stage} user={request.user} score={score} submitTick={currentTick}")
                    sub = Submission.objects.filter(user=request.user, submitTick=currentTick, stage=stage)
                    if sub.count() > 0:
                        return Response({"error": "You can only submit once every 5 seconds(1tick)"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
                    sub = Submission(tick=givenTick, stage=stage, user=request.user, content="", score=score, submitTick=currentTick)
                    sub.save()
                    f = True
                    break
            except DatabaseError as e:
                    logger.error(e)
            time.sleep(0.5)
        if not f:
            return Response({"error: server error please retry. sorry"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        resp = {}
        resp['recieved_time'] = timezone.make_naive(currentTime)
        resp['score'] = score
        resp['tick'] = givenTick
        resp['current_server_tick'] = currentTick
        resp['stage'] = stage
        return Response(resp)
    
    def __get_active_question(self, stage, currentTime) -> tuple[Optional[QuizData], str]:
        cand = Question.objects.filter(pk=stage)
        if len(cand) != 1:
            return None, "stage not found"
        data: Question = cand[0]
        if common.getQuestionStatus(data, currentTime) != common.QuestionStatus.ACTIVE:
            return None, "stage is not running"

        problem = problemClasses[data.content]
        quiz = QuizData(pk=data.pk, starttime=data.starttime, tickcount=data.tickcount, tickinterval=data.tickinterval, content=problem) # ToDo: serialize
        return quiz, ""

    def __answer_to_int(self, answer) -> Optional[list[int]]:
        try:
            return list(map(lambda x: int(x), answer))
        except:
            return None

    def __to_int(self, value) -> Optional[int]:
        try:
            return int(value)
        except:
            return None