from django.shortcuts import get_object_or_404, render , redirect
from .forms import AuctionForm, AuctionItemForm, BidForm, CustomUserCreationForm, ItemForm
from .models import Auction, AuctionItem, Bid, Item
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal



# Create your views here.
def index(request):
    return render(request,'auction.html')

def item(request):
    items = Item.objects.all()  # Adjust this query based on your needs
    return render(request, 'item.html', {'items': items})
    
def item_view(request, myid):
    item = get_object_or_404(Item, id=myid)
    bids = Bid.objects.filter(item_id=item).order_by('-bid_amount')

    context = {'item': item, 'bids': bids}
    return render(request, 'item_view.html', context)

@login_required
def item_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            # Automatically set the user to the currently logged-in user
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Item added successfully!')
            return redirect('item')  
    else:
        form = ItemForm()
    return render(request, 'item_add.html', {'form': form})

@login_required
def item_edit(request, myid):
    item = get_object_or_404(Item, id=myid)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            # Redirect to item.html or any other desired page
            return redirect('item')  # Replace 'item_list' with the appropriate URL name
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'item_edit.html', {'item': item, 'form': form})

@login_required
def item_delete(request, myid):
    item = get_object_or_404(Item, id=myid)
    item.delete()
    return redirect('item')  # Redirect to the item list page after deletion


def auction(request):
    auctions = Auction.objects.filter(status='active')
    return render(request, 'auction.html', {'auctions': auctions})

@login_required
def auction_add(request):
    if request.method == 'POST':
            form = AuctionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('auction')
    else:
            form = AuctionForm()
    return render(request, 'auction_add.html', {'form': form})

@login_required
def auction_edit(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    if request.method == 'POST':
            form = AuctionForm(request.POST, instance=auction)
            if form.is_valid():
                form.save()
                return redirect('auction')
    else:
            form = AuctionForm(instance=auction)
    return render(request, 'auction_edit.html', {'form': form, 'auction': auction})

@login_required
def auction_delete(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    auction.delete()
    return redirect('auction')


def auc_item(request, auction_id=None):
    if auction_id is not None:
        auction = get_object_or_404(Auction, id=auction_id)
        auctionitems = AuctionItem.objects.filter(auction=auction)
        items_related_to_auction = auctionitems.values_list('item_id', flat=True)
        items = Item.objects.filter(id__in=items_related_to_auction)
    else:
        items = Item.objects.none()

    return render(request, 'search.html', {'items': items})

@login_required
def auc_itemadd(request):
    if request.method == 'POST':
        form = AuctionItemForm(request.POST)
        if form.is_valid():
            new_auction_item = form.save()
            auction_id = new_auction_item.auction.id
            return redirect('auc_item', auction_id=auction_id)
    else:
        form = AuctionItemForm()

    return render(request, 'auc_itemadd.html', {'form': form})

@login_required
def auc_itemedit(request, item_id):
    auctionitem = get_object_or_404(AuctionItem, id=item_id)
    
    if request.method == 'POST':
        form = AuctionItemForm(request.POST, instance=auctionitem)
        if form.is_valid():
            form.save()
            return redirect('auc_item')  # Redirect to the auction item list page
    else:
        form = AuctionItemForm(instance=auctionitem)

    return render(request, 'auc_itemedit.html', {'form': form, 'auctionitem': auctionitem})

@login_required
def auc_itemdelete(request, item_id):
    auctionitem = get_object_or_404(AuctionItem, id=item_id)
    auctionitem.delete()
    return redirect('auc_item')  # Redirect to the auction item list page

def bid(request):
    return render(request,'item.html')

@login_required
def bid_view(request, myid):
    item = get_object_or_404(Item, id=myid)

    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')

        # Create a new bid
        bid = Bid.objects.create(user=request.user, item_id=item, bid_amount=bid_amount, status='pending')

        return redirect('item_view', myid=myid)
    
    return redirect('item_view', myid=myid)

@login_required
def bid_add(request, myid):
    item = get_object_or_404(Item, id=myid)

    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')

        if not bid_amount:
            messages.error(request, 'Bid amount is required.')
        
        else:
            bid_amount = int(bid_amount)  # Convert bid amount to integer
            item_price = int(item.price)  # Convert item price to integer
            # Get the current highest bid for the item
            highest_bid = Bid.objects.filter(item_id=item).order_by('-bid_amount').first()
            if bid_amount <= item_price:
                messages.success(request, 'Bid amount must be greater than the item price.')
            elif highest_bid and bid_amount <= highest_bid.bid_amount:
                messages.success(request, 'Bid amount must be greater than the current highest bid.')
            else:
                # Create a new bid
                bid = Bid.objects.create(user=request.user, item_id=item, bid_amount=bid_amount, status='pending')
                messages.success(request, 'Bid placed successfully!')

    return redirect('item_view', myid=myid)



def search(request, auction_id=None):
    query = request.GET.get('q')

    if query:
        items = Item.objects.filter(
            Q(name__icontains=query) |
            Q(artist__icontains=query) |
            Q(price__icontains=query)
        ).distinct()

        return render(request, 'search.html', {'items': items, 'query': query})
    else:
        return render(request, 'search.html')
    

def auc_search(request, auction_id=None):
    query = request.GET.get('q')

    if query:
        items = Item.objects.filter(
            Q(name__icontains=query) |
            Q(artist__icontains=query) |
            Q(price__icontains=query)
        ).distinct()

        return render(request, 'search.html', {'items': items, 'query': query})
    else:
        return render(request, 'search.html')



def to_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()

            # Assign the user to the selected group
            group = form.cleaned_data['group']
            group.user_set.add(user)

            # Set the user as staff
            user.is_staff = True
            user.save()

            # Log the user in
            login(request, user)

            return redirect('auction')  # Redirect to your desired page after registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def to_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Authenticate the user
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('auction')  # Redirect to your desired page after login
            else:
                # Authentication failed, show an error
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def to_logout(request):
    logout(request)
    return redirect('auction')

    return render(request,'logout.html')


    

 