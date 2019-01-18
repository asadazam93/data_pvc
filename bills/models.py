from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.utils.html import mark_safe


class Client(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, choices=(('Client', 'Client'), ('Supplier', 'Supplier')))
    address = models.CharField(max_length=512, blank=True, null=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    debit = models.IntegerField(default=0, verbose_name="Debit/Credit")
    previous_credit = models.IntegerField(default=0)

    def save(self, *args, **kwargs):

        client_payments = self.client_payments.all()
        paid = sum([client_payment.payment for client_payment in client_payments])
        client_bills = self.bills.all()
        bills = sum([bill.total_bill for bill in client_bills])
        self.debit = self.previous_credit + bills - paid
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def paid_last_seven_days(self):
        current_date = timezone.now()
        date_seven_days_back = current_date - timedelta(days=7)
        if ClientPayment.objects.filter(date__range=[date_seven_days_back, current_date], client=self):
            return "Yes"
        return "Not Paid"


class Product(models.Model):
    type = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    price_per_kg = models.IntegerField()
    price_per_kg_sale = models.IntegerField()
    weight = models.FloatField()

    @property
    def price(self):
        return int(self.price_per_kg * self.weight)

    @property
    def sale_price(self):
        return int(self.price_per_kg_sale * self.weight)

    def __str__(self):
        return self.name + ": " + self.type


class Bill(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="bills"
    )
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        choices=(('Sale', 'Sale'), ('Purchase', 'Purchase')),
        max_length=20,
        default='Sale'
    )

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
        self.date = timezone.now()
        super(Bill, self).save(*args, **kwargs)

    def pdf_link(self):
        return mark_safe(
            '<a class="grp-button" href="%s" target="blank">view bill</a>' % reverse('bill_view', args=[self.id]))

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
        if self.bill.type == 'Sale':
            return self.product.sale_price * self.quantity


    @property
    def total_weight(self):
        return self.product.weight * self.quantity

    @property
    def profit(self):
        if self.bill.type == 'Sale':
            return self.product.sale_price * self.quantity - self.product.price * self.quantity

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
        self.date = timezone.now()
        super(ClientPayment, self).save(*args, **kwargs)


class Inventory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def pdf_link(self):
        return mark_safe(
            '<a class="grp-button" href="%s" target="blank">view inventory</a>' % reverse('inventory_view', args=[self.id]))

    pdf_link.short_description = 'PDF'


class InventoryItem(models.Model):
    product = models.OneToOneField(
        Product,
        related_name="inventory_item",
        on_delete=models.CASCADE
    )
    inventory = models.ForeignKey(
        Inventory,
        related_name="inventoryitems",
        on_delete=models.CASCADE
    )
    stock = models.IntegerField(default=0)
    initial_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name + ': ' + str(self.stock)
