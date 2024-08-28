from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Item, Auction, AuctionItem, Bid
from .forms import CustomUserCreationForm, ItemForm, AuctionForm, AuctionItemForm, BidForm

class FormTestCase(TestCase):
    def test_custom_user_creation_form(self):
        # Create a test group
        group = Group.objects.create(name='Test Group')

        # Create a test form
        form_data = {'username': 'testuser', 'password1': 'testpassword', 'password2': 'testpassword', 'group': group.id}
        form = CustomUserCreationForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())
        

    # Add more test cases for other forms

