
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("new", views.newpost_view, name="newpost"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("follow/<str:username>", views.follow_profile, name="follow"),
    path("unfollow/<str:username>", views.unfollow_profile, name="unfollow"),
    path("following", views.following_view, name="following"),

    # API routes
    path("update/<int:post_id>", views.update_view, name="update"),
    path("like/<int:post_id>", views.like_view, name="like"),
    path("unlike/<int:post_id>", views.unlike_view, name="unlike")

]
