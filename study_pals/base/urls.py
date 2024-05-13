
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home ,name='home_route'),
    path('login/', views.login_page ,name='login_route'),
    path('register/', views.registration_page ,name='register_route'),
    path('logout/', views.logout_user ,name='logout_route'),

    path('room/<int:pk>/', views.room ,name='room_route'),
    path('room/delete-message/<int:pk>/', views.delete_message ,name='delete_message_route'),
    # path('room/edit-message/<int:pk>/', views.delete_message ,name='delete_message_route'),
    
    path('create-room/', views.create_room ,name='create_room_route'),
    path('edit-room/<int:pk>/', views.edit_room ,name='edit_room_route'),
    path('delete-room/<int:pk>/', views.delete_room ,name='delete_room_route'),


    path('user/profile/<int:pk>', views.user_profile ,name='user_profile_route'),
    path('user/edit-profile', views.edit_user ,name='edit_user_profile_route'),

    path('user/browse-topics', views.browse_topics ,name='browse_topics_route'),
    path('user/recent-activities', views.recent_activities ,name='recent_activities_route'),


    
]

