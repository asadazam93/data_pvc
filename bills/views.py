from django.shortcuts import render
from django.views.generic import View, DetailView

from bills.models import Client, Bill, Inventory


class HomeView(View):
    template = "home_view.html"

    def get(self, request, *args, **kwargs):
        context = dict()
        clients = Client.objects.filter(type='Client')
        amount = sum([client.debit for client in clients])
        context["amount"] = amount
        buyers = Client.objects.filter(type='Supplier')
        debit = sum([buyer.debit for buyer in buyers])
        context["debit"] = debit
        return render(request, template_name=self.template, context=context)


class BillView(DetailView):
    model = Bill


class InventoryView(DetailView):
    model = Inventory
