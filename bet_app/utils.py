# This is the utils.py file of your app
# It imports the requests and sklearn libraries
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# Create a function to get the matches for a given league from an external API
def get_matches(league):
  # Define the API endpoint and the parameters
  api_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
  print(response.json())
  api_headers = {
    "x-rapidapi-key": "0d927587e8mshf9668aafd1b2f49p1fd558jsnf44ed8412864",
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
  }
  api_params = {
    "league": "39",
    "season": "2023",
    "next": "10"
  }
  # Make a GET request to the API and get the response
  response = requests.get(api_url, headers=api_headers, params=api_params)
  # Check if the response is successful
  if response.status_code == 200:
    # Parse the response as JSON and get the data
    data = response.json()
    # Get the list of fixtures from the data
    fixtures = data["response"]
    # Create an empty list to store the matches
    matches = []
    # Loop through the fixtures and extract the relevant information
    for fixture in fixtures:
      # Get the match id, date, time, and teams from the fixture
      match_id = fixture["fixture"]["id"]
      date = fixture["fixture"]["date"][:10]
      time = fixture["fixture"]["date"][11:16]
      home_team = fixture["teams"]["home"]["name"]
      away_team = fixture["teams"]["away"]["name"]
      # Create a dictionary to store the match details
      match = {
        "id": match_id,
        "date": date,
        "time": time,
        "home_team": home_team,
        "away_team": away_team
      }
      # Append the match to the matches list
      matches.append(match)
    # Return the matches list
    return matches
  else:
    # Return an empty list if the response is not successful
    return []

# Create a function to get the predictions for a given match from a machine learning model
def get_predictions(match):
  # Define the features and labels for the model
  features = ["home_goals", "away_goals", "home_corners", "away_corners", "home_shots", "away_shots", "home_possession", "away_possession"]
  labels = ["over_under_goals", "more_corners"]
  # Load the training data from a CSV file
  data = pd.read_csv("bet_app/data.csv")
  # Split the data into X and y
  X = data[features]
  y = data[labels]
  # Create two models for each label: logistic regression and decision tree
  lr_model_ou = LogisticRegression()
  lr_model_mc = LogisticRegression()
  dt_model_ou = DecisionTreeClassifier()
  dt_model_mc = DecisionTreeClassifier()
  # Fit the models on the training data
  lr_model_ou.fit(X, y["over_under_goals"])
  lr_model_mc.fit(X, y["more_corners"])
  dt_model_ou.fit(X, y["over_under_goals"])
  dt_model_mc.fit(X, y["more_corners"])
  # Get the match statistics from an external API using the match id
  api_url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics?fixture={match.id}"
  api_headers = {
    "x-rapidapi-key": "0d927587e8mshf9668aafd1b2f49p1fd558jsnf44ed8412864",
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
  }
  # Make a GET request to the API and get the response
  response = requests.get(api_url, headers=api_headers)
  # Check if the response is successful
  if response.status_code == 200:
    # Parse the response as JSON and get the data
    data = response.json()
    # Get the list of statistics from the data
    statistics = data["response"]
    # Create an empty dictionary to store the match features
    match_features = {}
    # Loop through the statistics and extract the relevant information
    for statistic in statistics:
      # Get the type and value of the statistic for each team
      type = statistic["type"]
      home_value = statistic["statistics"][0]["value"]
      away_value = statistic["statistics"][1]["value"]
      # Check if the type is one of the features
      if type in features:
        # Store the home and away values in the match features dictionary
        match_features[f"home_{type}"] = home_value
        match_features[f"away_{type}"] = away_value
    # Convert the match features dictionary into a pandas series
    match_features = pd.Series(match_features)
    # Predict the labels for the match using the models
    lr_pred_ou = lr_model_ou.predict([match_features])[0]
    lr_pred_mc = lr_model_mc.predict([match_features])[0]
    dt_pred_ou = dt_model_ou.predict([match_features])[0]
    dt_pred_mc = dt_model_mc.predict([match_features])[0]
    # Get the probabilities for the predictions using the models
    lr_prob_ou = lr_model_ou.predict_proba([match_features])[0][lr_pred_ou]
    lr_prob_mc = lr_model_mc.predict_proba([match_features])[0][lr_pred_mc]
    dt_prob_ou = dt_model_ou.predict_proba([match_features])[0][dt_pred_ou]
    dt_prob_mc = dt_model_mc.predict_proba([match_features])[0][dt_pred_mc]
    # Create an empty dictionary to store the predictions
    predictions = {}
    # Store the predictions and probabilities for over/under goals
    predictions["over_under_goals"] = {
      "lr": {
        "prediction": lr_pred_ou,
        "probability": lr_prob_ou
      },
      "dt": {
        "prediction": dt_pred_ou,
        "probability": dt_prob_ou
      }
    }
    # Store the predictions and probabilities for more corners
    predictions["more_corners"] = {
      "lr": {
        "prediction": lr_pred_mc,
        "probability": lr_prob_mc
      },
      "dt": {
        "prediction": dt_pred_mc,
        "probability": dt_prob_mc
      }
    }
    # Return the predictions dictionary
    return predictions
  else:
    # Return an empty dictionary if the response is not successful
    return {}
