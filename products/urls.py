from django.urls import path

from products import views
urlpatterns = [
    path(
        route='create/',
        view=views.ProductCreateView.as_view(),
        name='create'
    ),
    path(
        route='',
        view=views.ProductListView.as_view(),
        name='list'
    ),
    path(
        route='<slug:slug>/',
        view=views.ProductDetailView.as_view(),
        name='detail'
    ),
    path(
        route='<slug:slug>/ask-question/',
        view=views.ask_question,
        name='ask-question'
    ),
    path(
        route='<slug:slug>/<int:question_id>/answer/',
        view=views.answer_question,
        name='answer-question'
    ),
]