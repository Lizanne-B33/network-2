
from django.urls import path
import network.views as views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name="add_post"),

    # API Routes
    path("api/feed", views.feed, name="api_feed"),
    path("api/single_profile/<id>", views.single_profile, name="single_profile"),
    path("api/single_feed/<str:created_by>",
         views.single_feed, name="api_single_feed"),
    path("api/single_post/<id>", views.single_post, name="api_single_post"),

]
