from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('profile_list/',profile_list,name='profile_list'),
    path('profile/<int:id>',profile,name='profile'),
    path('profile/followers/<int:id>',followers,name='followers'),
    path('profile/following/<int:id>',following,name='following'),
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('register/',register_user,name='register'),
    path('update_user/',update_user,name='update_user'),
    path('tweet_like/<int:id>',tweet_likes,name='tweet_likes'),
    path('tweet_share/<int:id>',tweet_share,name='tweet_share'),
    path('unfollow/<int:id>',unfollow,name='unfollow'),
    path('follow/<int:id>',follow,name='follow'),
    path('delete_tweet/<int:id>',delete_tweet,name='delete_tweet'),
    path('edit_tweet/<int:id>',edit_tweet,name='edit_tweet'),
    path('search/',search,name='search'),
    path('search_user/',search_user,name='search_user'),
]