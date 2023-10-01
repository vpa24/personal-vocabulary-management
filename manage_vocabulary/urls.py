from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('authentication/', include('authentication.urls')),
    path("add-vocabulary", views.add_vocabulary, name="add_vocabulary"),
    path("dictionary/<str:word_name>", views.vocabulary_detail, name="vocabulary_detail"),
    path("dictionary/<slug:title>-<int:vid>/edit",
         views.edit_vocabulary, name="edit_vocabulary"),
    path("search", views.search, name="search"),
    path("history", views.vocab_by_dates, name="vocab_by_dates"),
]
