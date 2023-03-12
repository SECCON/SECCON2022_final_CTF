from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.template import loader
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token

class LoginView(View):
    def get(self, request):
        template = loader.get_template('witchquiz/login.html')
        return HttpResponse(template.render({}, request))
    
    def post(self, request):
        token = request.POST["token"]
        user = authenticate(username=None, password=token)

        if user is not None:
            token, _ = Token.objects.update_or_create(user=user, key=token)
            login(request, user)
            return redirect('/')
        else:
            template = loader.get_template('witchquiz/login.html')
            context = {'error': 'invalid token'}
            return HttpResponse(template.render(context, request))

