from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.html import mark_safe


class Client(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512, blank=True, null=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    debit = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Product(models.Model):
    type = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    price_per_kg = models.IntegerField()
    weight = models.FloatField()

    @property
    def price(self):
        return int(self.price_per_kg*self.weight)

    def __str__(self):
        return self.name + ": " + self.type


class Bill(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="bills"
    )
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total_bill(self):
        bill = 0
        bill_items = self.billitems.all()
        if bill_items:
            bill += sum([bill_item.total_price for bill_item in bill_items])
        return bill

    @property
    def total_weight(self):
        weight = 0
        bill_items = self.billitems.all()
        if bill_items:
            weight += sum([bill_item.total_weight for bill_item in bill_items])
        return weight

    def __str__(self):
        return self.client.name + " bill: " + str(self.total_bill)

    def save(self, *args, **kwargs):
        client = self.client
        client_payments = client.client_payments.all()
        paid = sum([client_payment.payment for client_payment in client_payments])
        client_bills = client.bills.all()
        bills = sum([bill.total_bill for bill in client_bills])
        client.debit = bills - paid
        client.save()
        self.date = timezone.now()
        super(Bill, self).save(*args, **kwargs)

    def pdf_link(self):
        return mark_safe('<a class="grp-button" href="%s" target="blank">view bill</a>' % reverse('bill_view', args=[self.id]))
    pdf_link.short_description = 'PDF'


class BillItem(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="bill_items",
        on_delete=models.CASCADE
    )
    bill = models.ForeignKey(
        Bill,
        related_name="billitems",
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField()

    @property
    def total_price(self):
        return self.product.price * self.quantity

    @property
    def total_weight(self):
        return self.product.weight * self.quantity

    def __str__(self):
        return self.product.__str__() + " Q: " + str(self.quantity)


class ClientPayment(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="client_payments"
    )
    date = models.DateTimeField(auto_now_add=True)
    payment = models.IntegerField()

    def __str__(self):
        return self.client.name + " Paid: " + str(self.payment)

    def save(self, *args, **kwargs):
        client = self.client
        client_payments = client.client_payments.all()
        paid = sum([client_payment.payment for client_payment in client_payments])
        client_bills = client.bills.all()
        bills = sum([bill.total_bill for bill in client_bills])
        client.debit = bills - paid
        client.save()
        self.date = timezone.now()
        super(ClientPayment, self).save(*args, **kwargs)
