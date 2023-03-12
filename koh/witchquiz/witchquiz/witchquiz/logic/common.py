from witchquiz.models import Submission
from django.db import models
from django.contrib.auth.models import User
from witchquiz.models import Submission, Question
import datetime
from enum import Enum
from django.utils import timezone
from typing import Optional

class QuestionStatus(Enum):
    YET = 1
    ACTIVE = 2
    OVER = 3

    def __str__(self):
        if self.value == 2:
            return "running"
        elif self.value == 1:
            return "yet"
        else:
            return "over"

def getRanking(stage: int, tick: Optional[int] = None) -> list[dict]:
    # highest values
    # ToDo: I want to write a better query :(
    allUsers = User.objects.all().values('pk', 'username')
    memoUsers = {}
    for u in allUsers:
        memoUsers[u['pk']] = u['username']

    if tick is None:
        userScores = Submission.objects.filter(stage=stage).select_related('user').values('user', 'score').annotate(tick=models.Min('tick'))
    else:
        userScores = Submission.objects.filter(stage=stage, submitTick__lte=tick).select_related('user').values('user', 'score').annotate(tick=models.Min('tick'))
    if len(userScores) != 0:
        # get max_scores
        max_scores = userScores.values('user', 'user__username').annotate(score=models.Max('score'))
        condition = None
        for max_score in max_scores:
            m = models.Q(score=max_score['score']) & models.Q(user__pk=max_score['user'])
            if condition is None:
                condition = m
            else:
                condition |= m
        userScores = userScores.filter(condition).order_by('-score', 'tick').values('score', 'tick', username=models.F('user__username'), userid=models.F('user__pk'))

    submissionsUserCount = len(userScores)
    ranking = list(userScores)
    rank = 0
    tmp = 1
    for i in range(len(ranking)):
        if i-1 >= 0 and ranking[i-1]['score'] == userScores[i]['score']:
            tmp += 1
        else:
            rank += tmp
            tmp = 1

        ranking[i]['rank'] = rank
        ranking[i]['stageScore'] = getstageScore(rank)
        memoUsers.pop(ranking[i]['userid'])

    for u, v in memoUsers.items():
        rank = submissionsUserCount+1
        ranking.append({'score': 0, 'tick': 99999999, 'username': v, 'userid': u, 'rank': rank, 'stageScore': getstageScore(rank)})
    
    return ranking


def getActiveQuestions(currentTime) -> list[Question]:
    questions = Question.objects.all()
    if len(questions) == 0:
        return []

    activeQuestions = []
    for question in questions:
        if getQuestionStatus(question, currentTime) == QuestionStatus.ACTIVE:
            activeQuestions.append(question)

    return activeQuestions

def getCurrentTick(question: Question, currentTime: datetime):
    tick = ((currentTime - question.starttime) // question.tickinterval) + 1
    return min(max(tick, -1), question.tickcount+1)

def getQuestionStatus(question: Question, currentTime: datetime) -> QuestionStatus:
    tick = getCurrentTick(question, currentTime)
    if question.starttime <= currentTime and tick <= question.tickcount:
        return QuestionStatus.ACTIVE
    elif question.starttime <= currentTime:
        return QuestionStatus.OVER
    else:
        return QuestionStatus.YET

def getstageScore(rank) -> int:
    points = [20,17,14,12,10,8,6,5,4,3,2,1]
    return points[rank-1]

def getAllScoreTiming(startTime: datetime) -> int:
    time = startTime
    res = []
    for round in range(84):
        last_time = time + timezone.timedelta(minutes=4, seconds=59.9)
        questions = getActiveQuestions(last_time)
        if len(questions) >= 1:
            question = questions[-1]
            tick = getCurrentTick(question, last_time)
            res.append({
                'round': round+1,
                'time': time,
                'quesiton': question.pk,
                'lasttick': tick
            })
        time += timezone.timedelta(minutes=5)
    return res

def getCurrentRound(startTime: datetime, currentTime: datetime) -> int:
    return ((currentTime - startTime) // timezone.timedelta(minutes=5)) + 1

def getRoundQuestionTick(round: int, startTime: datetime) -> Optional[tuple[Question, int]]:
    last_time = startTime + timezone.timedelta(minutes=5)*(round-1) + timezone.timedelta(minutes=4, seconds=59.9)
    questions = getActiveQuestions(last_time)
    if len(questions) >= 1:
        question = questions[-1]
        tick = getCurrentTick(question, last_time)
        return question, tick
    return None

def getRoundTime(round: int, startTime: datetime) -> tuple[datetime.datetime, datetime.datetime]:
    return startTime + timezone.timedelta(minutes=5)*(round-1), startTime + timezone.timedelta(minutes=5)*(round-1) + timezone.timedelta(minutes=4, seconds=59.9)