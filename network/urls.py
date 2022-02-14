
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allPosts",views.allPosts,name="allPosts"),
    path("profilePage\<str:userid>",views.profilePage,name="profilePage"),
    path("follow\<str:userid>",views.follow,name="follow"),
    path("unfollow\<str:userid>",views.unfollow,name="unfollow"),
    path("following",views.following,name="following"),

    # API Routes
    path("posts/<int:number>",views.savePost,name="savePost"),
    path("like",views.like,name="like")
]
