from . import views
from django.urls import path

urlpatterns = [
    path('', views.connection_check),
    path('checkClubName', views.check_club_name),
    path('createClub', views.create_club),
    path('getUserData', views.get_user_data),
    path('editUserData', views.edit_user_data),
    path('getClubs', views.get_clubs),
    path('getClubsNumber', views.get_clubs_number),
    path('getClubData', views.get_club_data),
    path('getClubPosts', views.get_club_posts),
    path('createPost', views.create_post),
    path('getMyPosts', views.get_my_posts),
    path('getMyClubs', views.get_my_clubs),
]
