from django.shortcuts import render
from django.views.generic.base import View
from .forms import InputBrokerFormSet

from .models import Broker, UpdateReport

# Create your views here.
class MainView(View):
    template_name = 'broker/main.html'

    def get(self, request, *args, **kwargs):
        bukken_id = request.GET.get('bukken')  
        print("bukken_id data:", bukken_id)
        formset = InputBrokerFormSet(queryset=Broker.objects.all())

        return render(request, self.template_name, {
            'formset': formset, 
            })

    def post(self, request, *args, **kwargs):
        print("REQUEST POST", request.POST)
        formset = InputBrokerFormSet(request.POST, queryset=Broker.objects.all())
        formset.save()
        formset = InputBrokerFormSet(queryset=Broker.objects.all())
        # print("formset passing here", formset)
        if formset.is_valid():
            formset.save()
        else:
            print("Formset is not valid", formset.errors)
        return render(request, self.template_name, {
            'formset': formset, 
        })
