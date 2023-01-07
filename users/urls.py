from django.urls import path

from users import views

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
    path('my-profile/payment-cards/<int:pk>/delete', views.delete_profile_payment, name='delete-paymentcard')
]