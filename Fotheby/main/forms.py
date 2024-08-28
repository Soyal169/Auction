from django import forms
from .models import Item, Auction, AuctionItem,Bid
from django.contrib.auth.forms import UserCreationForm
from .models import CustomGroup
from django.contrib.auth.models import User,Group


class CustomUserCreationForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None)
    email = forms.EmailField(required=False)


    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('group','email')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['user']

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = '__all__'

class AuctionItemForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = '__all__'

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'