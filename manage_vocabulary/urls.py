from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add-vocabulary", views.add_vocabulary, name="add_vocabulary"),
    path("dictionary/<int:vid>", views.vocabulary_detail, name="vocabulary_detail"),
    path("dictionary/<slug:title>-<int:vid>/edit",
         views.edit_vocabulary, name="edit_vocabulary"),
    path("search", views.search, name="search"),
    path("history", views.vocab_by_dates, name="vocab_by_dates"),
]
