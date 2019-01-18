from django.contrib import admin
from bills.models import Client, ClientPayment, Bill, BillItem, Product, InventoryItem, Inventory
from rangefilter.filter import DateRangeFilter


class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 1


class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "number", "debit", "type", "previous_credit", "paid_last_seven_days")
    search_fields = ("name", "number", "address")
    list_filter = ("type",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "name", "price_per_kg", "weight", "price", "price_per_kg_sale", "brand")
    list_filter = ("type", "brand")
    search_fields = ("name", "brand")


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    inlines = (BillItemInline,)
    list_display = ("id", "client", "date", "total_bill", "total_weight", "pdf_link")
    search_fields = ("client__name",)
    list_filter = ("client__name", ('date', DateRangeFilter))


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    inlines = (InventoryItemInline,)
    list_display = ("id", "name", "pdf_link")


@admin.register(ClientPayment)
class ClientPaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "date", "payment")
    list_filter = ("client__name", ('date', DateRangeFilter))
    search_fields = ("client__name",)
