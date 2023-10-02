from django.contrib import admin
from .models import League, Match, Prediction

# Register the League model
admin.site.register(League)

# Register the Match model
admin.site.register(Match)

# Register the Prediction model
admin.site.register(Prediction)

