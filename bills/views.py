from django.shortcuts import render
from django.views.generic import View

from bills.models import Client


class HomeView(View):
    template = "home_view.html"

    def get(self, request, *args, **kwargs):
        context = dict()
        clients = Client.objects.all()
        amount = sum([client.debit for client in clients])
        context["amount"] = amount
        return render(request, template_name=self.template, context=context)
