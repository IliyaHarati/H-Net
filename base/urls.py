from django.urls import path
from .views import *
urlpatterns=[
    path("",home,name="home"),
    path("room/<str:pk>/",room,name="room"),
    path("update-room/<str:pk>/",updateRoom,name="update-room"),
    path("delete-room/<str:pk>/",deleteRoom,name="delete-room"),
    path("delete-message/<str:pk>/",deleteMessage,name="delete-message"),
    path("create-room/",createRoom,name="create-room"),
    path("user-profile/<str:pk>/",profilePage,name="user-profile"),
    path("register/",registerPage,name="register"),
    path("login/",loginPage,name="login"),
    path("logout/",logoutView,name="logout"),
    path("update-user/",updateUser,name="update-user"),
    path("topics/",topicsPage,name="topics"),
    path("activities/",activitiesPage,name="activities"),
]