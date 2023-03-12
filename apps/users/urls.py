from django.urls import path, include

from apps.users import views

cart_urls = [
    path('', views.ShoppingCartView.as_view(), name='cart'),
    path('<int:pk>/change_qty', views.change_product_qty, name='change-qty'),
    path('<int:pk>/remove', views.remove_item, name='remove_item'),
]

adressess_urls = [
    path('', views.ProfileAddressListView.as_view(), name='list'),
    path('create/', views.ProfileAddressCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProfileAddressUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete', views.delete_profile_address, name='delete'),
]

paymentcards_urls = [
    path('', views.ProfilePaymentListView.as_view(), name='list'),
    path('create/', views.ProfilePaymentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProfilePaymentUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete', views.delete_profile_payment, name='delete'),
]

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(),name='signup'),

    path('my-profile/', views.ProfileDetailView.as_view(), name='my-profile'),
    path('my-profile/change_password', views.ProfileChangePasswordView.as_view(), name='change-password'),
    path('my-profile/questions/', views.ProductQuestionListView.as_view(), name='questions'),
    path('my-profile/published-products/', views.PublishedProductsListView.as_view(), name='published-products'),
    path('my_profile/published-products/<int:pk>/update_qty/', views.update_stock_qty, name='update_qty'),

    path('my-profile/cart/',include((cart_urls, 'cart'))),
    path('my-profile/addresses/',include((adressess_urls, 'address'))),
    path('my-profile/payment-cards/',include((paymentcards_urls, 'paymentcard'))),
]