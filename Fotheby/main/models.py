from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group



class CustomGroup(Group):
    pass

class Auction(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateField(max_length=255)
    end_date = models.DateField(max_length=255)
    STATUS_CHOICES = [
            ('active', 'Active'),
            ('pending', 'Pending'),
            ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f'{self.name} -- {self.start_date} {"TO"} {self.end_date} {"Status is -"}{self.status}'
    

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='item_images/')
    price = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    commission = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    drawing_medium = models.CharField(max_length=255, null=True, blank=True)
    dimensions = models.CharField(max_length=255, null=True, blank=True)
    material_used = models.CharField(max_length=255, null=True, blank=True)
    weight = models.CharField(max_length=255, null=True, blank=True)
    framed = models.CharField(max_length=255, null=True, blank=True)
    image_type = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate commission as 10% of the price with two decimal places
        self.commission = round(float(self.price) * 0.1, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('sold', 'Sold'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')  

    def __str__(self):
        return f'{self.user} -- {self.item_id} -- {self.bid_amount} -- {self.status}' 

class AuctionItem(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    lot_number = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.auction} -- {self.item_id} -- {self.lot_number}'
