from django.urls import path
from spacetrading import views


urlpatterns = [
    path('', views.index, name='index'),
    path('games/create/', views.create_game, name='create_game'),
    path('games/', views.GameListView.as_view(), name='games'),
]