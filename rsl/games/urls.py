from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('', views.games, name='games'),
    path('add/', views.add_game, name='add-game'),
    path('<game_id>/', views.game_info, name='game-info'),
    path('<game_id>/add_event/', views.add_event, name='add-event'),
    path('<game_id>/edit/', views.edit_game, name='edit-game'),
    path('<game_id>/delete/', views.delete_game, name='delete-game'),
    path('<game_id>/<event_id>/delete/', views.delete_event, name='delete-event'),
    path('<game_id>/point_game/', views.point_game, name='point-game'),
]
