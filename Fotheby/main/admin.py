from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html

from main.forms import AuctionItemForm
from .models import Bid, Category, Item, Auction, AuctionItem

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'user', 'image', 'view_bids_link', 'commission')

    def view_bids_link(self, obj):
        bids_count = obj.bid_set.count()
        url = reverse("admin:main_bid_changelist") + f"?item_id__id__exact={obj.id}"
        return format_html('<a href="{}">{} Bids</a>', url, bids_count)

    view_bids_link.short_description = "Bids"

    exclude = ('commission',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].widget = forms.HiddenInput()
        if obj is None:  # Only set the default value for a new object
            form.base_fields['user'].initial = request.user.id
        return form

class AuctionItemAdmin(admin.ModelAdmin):
    list_display = ('auction','item_id','lot_number')


class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_id', 'bid_amount', 'status')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].widget = forms.HiddenInput()

        if obj is None:  # Only set the default value for a new object
            form.base_fields['user'].initial = request.user.id

        return form

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'start_date', 'end_date', 'status')

admin.site.register(Bid, BidAdmin)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(AuctionItem, AuctionItemAdmin)
