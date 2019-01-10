from django.contrib import admin
from bills.models import Client, ClientPayment, Bill, BillItem, Product
from rangefilter.filter import DateRangeFilter


class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "number", "debit")
    search_fields = ("name", "number", "address")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "name", "price_per_kg", "weight", "price")
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    inlines = (BillItemInline,)
    list_display = ("id", "client", "date", "total_bill", "total_weight")
    search_fields = ("client__name",)
    list_filter = ("client__name", ('date', DateRangeFilter))


@admin.register(ClientPayment)
class ClientPaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "date", "payment")
    list_filter = ("client__name", ('date', DateRangeFilter))
    search_fields = ("client__name",)
