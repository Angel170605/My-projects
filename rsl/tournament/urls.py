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
    path('<team_id>/edit/', views.edit_team, name='edit-team'),
    path('<team_id>/delete/', views.delete_team, name='delete-team'),
    path('<team_id>/<user_id>/sign/', views.sign_player, name='sign-player'),
    path('matches/add/', views.add_match, name='add-match'),
    path('matches/<match_id>/', views.match_info, name='match-info'),
    path('matches/<match_id>/add_event/', views.add_event, name='add-event')
]
