from django.http import HttpResponse
from django.views.generic import View
from django.template import loader

class HowToView(View):
    def get(self, request):
        template = loader.get_template('witchquiz/howto.html')
        return HttpResponse(template.render({}, request))