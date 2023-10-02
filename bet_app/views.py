from django.shortcuts import render, get_object_or_404
from .models import League, Match, Prediction
from .utils import get_matches, get_predictions

# Create a view for the home page
def home(request):
  # Get all the leagues from the database
  leagues = League.objects.all()
  # Render the home template with the leagues as context
  return render(request, 'bet_app/home.html', {'leagues': leagues})

# Create a view for the league page
def league(request, league_id):
  # Get the league with the given id from the database
  league = get_object_or_404(League, pk=league_id)
  # Get the matches for the league from an external API
  matches = get_matches(league.name)
  # Render the league template with the league and matches as context
  return render(request, 'bet_app/league.html', {'league': league, 'matches': matches})

# Create a view for the match page
def match(request, match_id):
  # Get the match with the given id from the database
  match = get_object_or_404(Match, pk=match_id)
  # Render the match template with the match as context
  return render(request, 'bet_app/match.html', {'match': match})

# Create a view for the prediction page
def prediction(request, prediction_id):
  # Get the prediction with the given id from the database
  prediction = get_object_or_404(Prediction, pk=prediction_id)
  # Get the predictions for the match from a machine learning model
  predictions = get_predictions(prediction.match)
  # Render the prediction template with the prediction and predictions as context
  return render(request, 'bet_app/prediction.html', {'prediction': prediction, 'predictions': predictions})

