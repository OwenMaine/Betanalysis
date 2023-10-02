from django.db import models


# Create a model for the leagues
class League(models.Model):
  # A league has a name and an image
  name = models.CharField(max_length=100)
  image = models.ImageField(upload_to='leagues/')

  # A string representation of a league
  def __str__(self):
    return self.name

# Create a model for the matches
class Match(models.Model):
  # A match belongs to a league and has two teams, a date, and a time
  league = models.ForeignKey(League, on_delete=models.CASCADE)
  home_team = models.CharField(max_length=100)
  away_team = models.CharField(max_length=100)
  date = models.DateField()
  time = models.TimeField()

  # A string representation of a match
  def __str__(self):
    return f"{self.home_team} vs {self.away_team} on {self.date} at {self.time}"

# Create a model for the predictions
class Prediction(models.Model):
  # A prediction belongs to a match and has two types, values, and confidences
  match = models.ForeignKey(Match, on_delete=models.CASCADE)
  over_under_goals_type = models.CharField(max_length=10)
  over_under_goals_value = models.DecimalField(max_digits=3, decimal_places=1)
  over_under_goals_confidence = models.IntegerField()
  more_corners_type = models.CharField(max_length=10)
  more_corners_value = models.CharField(max_length=100)
  more_corners_confidence = models.IntegerField()

  # A string representation of a prediction
  def __str__(self):
    return f"Predictions for {self.match}"
