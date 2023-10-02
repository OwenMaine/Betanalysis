# This is the urls.py file of your app
# It imports the path function and the views of your app
from django.urls import path
from . import views

urlpatterns = [
  # Create a URL for the home page with an empty pattern and a name 'home'
  path('', views.home, name='home'),
  # Create a URL for the league page with a pattern that captures the league id and a name 'league'
  path('league/<int:league_id>/', views.league, name='league'),
  # Create a URL for the match page with a pattern that captures the match id and a name 'match'
  path('match/<int:match_id>/', views.match, name='match'),
  # Create a URL for the prediction page with a pattern that captures the prediction id and a name 'prediction'
  path('prediction/<int:prediction_id>/', views.prediction, name='prediction'),
]

