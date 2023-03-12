import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .logic import common
from witchquiz.models import RoundScore, RoundStageTickTime, Question, UserToken
from witchquiz import settings
from django import utils
from django.contrib.auth.models import User
from django.db import transaction
import logging
import json
import subprocess

logger = logging.getLogger(__name__)

def periodic_execution():
    currentTime = utils.timezone.now()
    for rstt in RoundStageTickTime.objects.filter(checked=False, time__lt=currentTime):
        logger.info(f"aggregate score {rstt.stage} {rstt.round} tick: 1~{rstt.tick} [{currentTime}]")

        ranking = {}
        for r in common.getRanking(rstt.stage,rstt.tick):
            ranking[r['userid']] = r
        
        allUser = User.objects.all()
        if len(allUser) != len(RoundScore.objects.filter(round=rstt.round)):
            with transaction.atomic():
                for user in allUser:
                    rs = RoundScore.objects.filter(user=user, round=rstt.round)
                    logger.info(f"ranking: round={rstt.round}, user={user}, questionid={rstt.stage},score={ranking[user.pk]['stageScore']},tick={rstt.tick},rank={ranking[user.pk]['rank']}")
                    if len(rs) == 0:
                        data = RoundScore(round=rstt.round, user=user, questionid=rstt.stage,score=ranking[user.pk]['stageScore'],tick=rstt.tick,rank=ranking[user.pk]['rank'])
                        data.save()
                    
        scores = []
        roundscore = RoundScore.objects.filter(round=rstt.round)
        if len(User.objects.all()) == len(roundscore):
            for rs in roundscore:
                usertoken = UserToken.objects.filter(user=rs.user)
                if len(usertoken) != 1:
                    logger.error(f"error: {user} not found")
                token = usertoken[0].token

                scores.append({
                    "team_token": token,
                    "point": rs.score
                    })

            logger.info(f"ranking: round={rstt.round} completed")

            file_name = settings.BASE_DIR / f"round{rstt.round}_score.json"
            try:
                with open(file_name, "w") as f:
                    f.write(json.dumps( { "category_name": "WitchQuiz", "round": rstt.round, "scores": scores, "override": True }))
            except Exception as e:
                logger.error(f"file open error: {e}")
                continue

            try:
                r = subprocess.run([settings.BASE_DIR / "kothcli-client", file_name], capture_output=True, timeout=5)
                logger.error(f"kothcli-client return code: {r.returncode}")
                logger.error(f"kothcli-client stdout: {r.stdout}")
                logger.error(f"kothcli-client stderr: {r.stderr}")
                if r.returncode != 0:
                    logger.error(f"kothcli-client error: {r.returncode}")
                    continue
            except Exception as e:
                logger.error(f"kothcli-client exception: {e}")
                continue

            with transaction.atomic():
                rstt.checked = True
                rstt.save()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_execution, 'interval', seconds=10)
    scheduler.start()
