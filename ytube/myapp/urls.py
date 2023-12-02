from django.contrib import admin
from django.urls import path , include
from myapp import views

from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.signuplogin, name="signuplogin"),
    path('logout/',views.logout,name='logout'),
    path('home/',views.home, name="home"),
    path('channel/',views.channel, name="channel"),
    path('userprofile/',views.userprofile, name="userprofile"),
    path('usercommunity/',views.usercommunity, name="usercommunity"),
    path('userupload/',views.userupload, name="userupload"),

    path('videopage/<slug:post_slug>',views.videopage, name="videopage"),

    # Building nav options button 
    path('subscribing/',views.subscribing, name="subscribing"),
    path('mylist/',views.mylist, name="mylist"),
    path('addtomylist/',views.addtomylist, name="addtomylist"),
    path('remove_mylist/',views.remove_mylist,name='remove_mylist'),
    path('most_likedvideos',views.most_likedvideos,name='most_likedvideos'),
    path('most_watched',views.most_watched,name='most_watched'),
    #path('like_video/<int:video_id>/', like_video, name='like_video'),

    path('settings/',views.settings,name='settings'),
    # writing the urls for filters 
    path('action_videos/',views.action_videos,name='action_videos'),
    path('anime_videos/',views.anime_videos,name='anime_videos'),
    path('film_videos/',views.film_videos,name='film_videos'),
    path('gaming_videos/',views.gaming_videos,name='gaming_videos'),
    path('learning_videos/',views.learning_videos,name='learning_videos'),
    path('fashion_videos/',views.fashion_videos,name='fashion_videos'),
    path('sports_videos/',views.sports_videos,name='sports_videos'),

    path('shorts/',views.shorts,name='shorts'),
    path('uploadshorts/',views.uploadshorts,name='uploadshorts'),

    path('searchpage/',views.searchpage,name='searchpage'),
    path('communitypost/',views.communitypost,name='communitypost'),

]
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
