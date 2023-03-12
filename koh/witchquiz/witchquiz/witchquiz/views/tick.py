from django.http import JsonResponse
from django.views.generic import View
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authtoken.models import Token
import logging
from witchquiz.models import Submission, Question
from django.utils import timezone
from rest_framework import status

class View(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = ''

    def get(self, request, stage=-1, tick=-1):
        user = self.request.user
        submissions = Submission.objects.filter(user=user,stage=stage,tick=tick)
        if len(submissions) == 0:
            return JsonResponse("not found",status=status.HTTP_404_NOT_FOUND)
        submission = submissions[0]
        
        resp = {}
        resp['tick'] = submission.tick
        resp['stage'] = submission.stage
        resp['score'] = submission.score

        return JsonResponse(resp)