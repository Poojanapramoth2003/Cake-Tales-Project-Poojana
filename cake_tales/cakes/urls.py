from django.urls import path

from . import views

urlpatterns=[

    path('',views.HomeView.as_view(),name='home'),

    path('add-a-cake/',views.AddCakeView.as_view(),name='add-a-cake'),
    
    path('cake-details/<str:uuid>/',views.CakeDetailsView.as_view(),name='cake-details'),

    path('cake-edit/<str:uuid>/',views.CakeEditView.as_view(),name='cake-edit'),\
    
    path('cake-delete/<str:uuid>/',views.CakeDeleteView.as_view(),name='cake-delete'),

    path('add-to-wishlist/<str:uuid>/',views.AddtoWishlist.as_view(),name='add-to-wishlist'),

    path('remove-from-wishlist/<str:uuid>/',views.RemovefromWishlist.as_view(),name='remove-from-wishlist'),
]