from django.urls import path

from . import views

app_name = 'tournament'

urlpatterns = [
    path('', views.main, name='main'),
    path('info/', views.info, name='info'),
    path('teams/', views.teams, name='teams'),
    path('add/ ', views.add_team, name='add-team'),
    path('<team_id>/', views.team_info, name='team-info'),
    path('<team_id>/edit/', views.edit_team, name='edit-team'),
    path('<team_id>/delete/', views.delete_team, name='delete-team'),
]
