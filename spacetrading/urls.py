from django.urls import path
from spacetrading import views


urlpatterns = [
    path('', views.rules, name='rules'),
    path('rules', views.rules, name='rules'),
    path('games/create/', views.create_game, name='create_game'),
    path('games/active/', views.ActiveGameListView.as_view(), name='active_games'),
    path('games/open/', views.OpenGameListView.as_view(), name='open_games'),
    path('games/<int:pk>', views.GameDetailView.as_view(), name='game_detail'),
]