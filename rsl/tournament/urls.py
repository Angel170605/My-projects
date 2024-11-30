from django.urls import path

from . import views

app_name = 'tournament'

urlpatterns = [
    path('', views.main, name='main'),
    path('info/', views.info, name='info'),
    path('teams/', views.teams, name='teams'),
    path('matches/', views.matches, name='matches'),
    path('add/ ', views.add_team, name='add-team'),
    path('<team_id>/', views.team_info, name='team-info'),
    path('<name>/edit/', views.edit_team, name='edit-team'),
    path('<team_id>/<user_id>/sign/', views.sign_player, name='sign-player'),
    path('match/<match_id>/', views.match_info, name='match-info'),
]
