from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.auction, name='auction'),
    
    path('item_view/<int:myid>/', views.item_view, name='item_view'),
    path('item_view/<int:myid>/bid/', views.bid_view, name='place_bid'),
    path('item_edit/<int:myid>/', views.item_edit, name='item_edit'),
    path('item_add/', views.item_add, name='item_add'),
    path('item/', views.item, name='item'),
    # path('item/<int:myid>/', views.item_view, name='item_view'),
    path('item_delete/<int:myid>/', views.item_delete, name='item_delete'),

    path('auction/', views.auction, name='auction'),
    path('auction_add/', views.auction_add, name='auction_add'),
    path('auction_delete/<int:pk>/', views.auction_delete, name='auction_delete'),
    path('auction_edit/<int:pk>/', views.auction_edit, name='auction_edit'),
    path('auc_item/<int:auction_id>/', views.auc_item, name='auc_item'),

    
    path('bid_view/<int:myid>/', views.bid_view, name='bid_view'),
    path('bid_add/<int:myid>/', views.bid_add, name='bid_add'),

   
    path('auc_itemadd/', views.auc_itemadd, name='auc_itemadd'),
    path('auc_itemdelete/<int:item_id>/', views.auc_itemdelete, name='auc_itemdelete'),
    path('auc_itemedit/<int:item_id>/', views.auc_itemedit, name='auc_itemedit'),

    path('search/', views.search, name='search'),
    path('search/<int:auction_id>/', views.auc_item, name='search_with_auction'),

      
    path('register/', views.to_register, name='to_register'),
    path('login/', views.to_login, name='to_login'),
    path('logout', views.to_logout, name='to_logout'),
    
  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
