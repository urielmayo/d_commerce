from django.urls import path, include

from apps.users import views

cart_urls = [
    path('', views.ShoppingCartView.as_view(), name='cart'),
    path('<int:pk>/change_qty', views.change_product_qty, name='change-qty'),
    path('<int:pk>/remove', views.remove_item, name='remove_item'),
]

urlpatterns = [
    #users
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(),name='signup'),

    path('my-profile/', views.ProfileDetailView.as_view(), name='my-profile'),

    path('my-profile/addresses/', views.ProfileAddressListView.as_view(), name='address-list'),
    path('my-profile/addresses/create/', views.ProfileAddressCreateView.as_view(), name='create-address'),
    path('my-profile/addresses/<int:pk>/', views.ProfileAddressUpdateView.as_view(), name='edit-address'),
    path('my-profile/addresses/<int:pk>/delete', views.delete_profile_address, name='delete-address'),

    path('my-profile/payment-cards/', views.ProfilePaymentListView.as_view(), name='paymentcard-list'),
    path('my-profile/payment-cards/create/', views.ProfilePaymentCreateView.as_view(), name='create-paymentcard'),
    path('my-profile/payment-cards/<int:pk>/', views.ProfilePaymentUpdateView.as_view(), name='edit-paymentcard'),
    path('my-profile/payment-cards/<int:pk>/delete', views.delete_profile_payment, name='delete-paymentcard'),

    path('my-profile/published-products/', views.PublishedProductsListView.as_view(), name='published-products'),

    path('my-profile/cart/',include((cart_urls, 'cart')))
]