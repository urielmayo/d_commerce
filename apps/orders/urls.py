from django.urls import path

from apps.orders import views
from apps.products.views import ProductReviewCreateView
urlpatterns = [
    path('', view=views.OrderListView.as_view(), name='list'),
    path('create/', view=views.OrderCreateView.as_view(), name='create'),

    path('sales/', view=views.OrderLinesListView.as_view(), name='sales-list'),
    path('sales/<int:pk>/ship/', view=views.ship_product, name='ship-product'),
    path('sales/<int:pk>/deliver/', view=views.deliver_product, name='deliver-product'),

    path('order_lines/<int:pk>/add-review/', view=ProductReviewCreateView.as_view(), name='add-review')

]