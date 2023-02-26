from django.urls import path

from apps.notifications import views
urlpatterns = [
    path('<int:pk>/', view=views.mark_as_read, name='as_read')
]