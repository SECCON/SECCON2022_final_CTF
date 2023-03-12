from witchquiz.models import RoundStageTickTime, Question
from witchquiz import settings

import datetime

RoundStageTickTime.objects.all().delete()
START_TIME = datetime.datetime(9999, 2, 10, 1, 30, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
for q in Question.objects.all():
    START_TIME = min(START_TIME, q.starttime)

for q in Question.objects.all():
    print(q.starttime)

    round_tick = {}
    for tick in range(1, q.tickcount+1):
        t = q.starttime + q.tickinterval*(tick-1)
        round = (t - START_TIME)//settings.ROUND_DELTA + 1
        round_tick[round] = max(round_tick.get(round,0), tick)

    for round, tick in round_tick.items():
        r = RoundStageTickTime(round=round, stage=q.pk, tick=tick, time=START_TIME + round*settings.ROUND_DELTA, checked=False)
        r.save()

for rstt in RoundStageTickTime.objects.all():
    print(rstt.stage, rstt.round, rstt.tick, rstt.time, rstt.checked)