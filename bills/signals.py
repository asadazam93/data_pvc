from django.db.models.signals import post_save

from bills.models import BillItem, ClientPayment, InventoryItem


def save_billitem(sender, instance, **kwargs):
    print("called")
    bill = instance.bill
    client = bill.client
    client_payments = client.client_payments.all()
    paid = sum([client_payment.payment for client_payment in client_payments])
    client_bills = client.bills.all()
    bills = sum([bill.total_bill for bill in client_bills])
    client.debit = client.previous_credit + bills - paid
    client.save()
    product = instance.product
    try:
        inventory_item = product.inventory_item
        bill_items = product.bill_items.filter(bill__client__type="Client")
        quantity_sold = sum([bill_item.quantity for bill_item in bill_items])
        bill_items_purchase = product.bill_items.filter(bill__client__type="Supplier")
        quantity_purchased = sum([bill_item.quantity for bill_item in bill_items_purchase])
        inventory_item.stock += quantity_purchased - quantity_sold
        inventory_item.save()
    except InventoryItem.DoesNotExist:
        pass


def save_clientpayment(sender, instance, **kwargs):
    client = instance.client
    client_payments = client.client_payments.all()
    paid = sum([client_payment.payment for client_payment in client_payments])
    client_bills = client.bills.all()
    bills = sum([bill.total_bill for bill in client_bills])
    client.debit = client.previous_credit + bills - paid
    client.save()

post_save.connect(save_billitem, sender=BillItem)
post_save.connect(save_clientpayment, sender=ClientPayment)
