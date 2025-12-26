from django.urls import path
from .views import get_airports, search_flights, get_flight_details, get_search_history

urlpatterns = [
    path("search/", search_flights, name="search-flights"),
    path("get-airports/", get_airports, name="get-airports"),  # Airport autocomplete
    path('get-flight-details/', get_flight_details, name='get-flight-details'),
    path('get-search-history/', get_search_history, name='get-search-history'),
] 