from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import os
from dotenv import load_dotenv
import base64

# Load API key from environment variables
load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '4a95574f32msh3ecc8c16cd287a5p127f43jsn2d2530d45138')  # In production, this key should be set as an environment variable
RAPIDAPI_HOST = "sky-scanner3.p.rapidapi.com"

# API endpoints
AUTO_COMPLETE_URL = "https://sky-scanner3.p.rapidapi.com/flights/auto-complete"
SEARCH_ROUNDTRIP_URL = "https://sky-scanner3.p.rapidapi.com/flights/search-roundtrip"
SEARCH_ONEWAY_URL = "https://sky-scanner3.p.rapidapi.com/flights/search-one-way"
FLIGHT_DETAIL_URL = "https://sky-scanner3.p.rapidapi.com/flights/detail"

# default headers
DEFAULT_HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

@api_view(['GET'])
def get_airports(request):
    """Airport autocomplete API"""
    query = request.GET.get('query', '')
    
    if not query:
        return Response({"error": "Query parameter is required"}, status=400)
    
    querystring = {"query": query}
    
    try:
        response = requests.get(AUTO_COMPLETE_URL, headers=DEFAULT_HEADERS, params=querystring)
        response.raise_for_status()  # raise an exception if an error occurs
        
        # airport autocomplete search is not logged (to avoid creating too much data)
        
        return Response(response.json())
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def search_flights(request):
    """Flight search API (round/one-way)"""
    print("="*40)
    print("[DEBUG] search_flights endpoint was called")
    print("[DEBUG] Request method:", request.method)
    print("[DEBUG] Request GET params:", dict(request.GET))
    print("="*40)
    
    trip_type = request.GET.get('trip_type', 'round')  # 'round' or 'one-way'
    from_entity_id = request.GET.get('fromEntityId', '')
    to_entity_id = request.GET.get('toEntityId', '')
    depart_date = request.GET.get('departDate', '')
    return_date = request.GET.get('returnDate', '')
    cabin_class = request.GET.get('cabinClass', 'economy')
    adults = request.GET.get('adults', '1')
    children = request.GET.get('children', '0')
    infants = request.GET.get('infants', '0')
    
    if not from_entity_id:
        return Response({"error": "From location is required"}, status=400)
    
    # default query parameters
    querystring = {
        "fromEntityId": from_entity_id,
        "toEntityId": to_entity_id,
        "cabinClass": cabin_class,
        "adults": adults,
        "children": children,
        "infants": infants
    }
    
    # if the departure date is provided, add it to the query parameters
    if depart_date:
        querystring["departDate"] = depart_date
    
    # if the round trip is selected and the return date is provided, add it to the query parameters
    if trip_type == 'round' and return_date:
        querystring["returnDate"] = return_date
        url = SEARCH_ROUNDTRIP_URL
    else:
        url = SEARCH_ONEWAY_URL
    
    print(f"[DEBUG] Calling SkyScanner API URL: {url}")
    print(f"[DEBUG] With parameters: {querystring}")
    
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, params=querystring)
        print(f"[DEBUG] SkyScanner API response status code: {response.status_code}")
        
        response.raise_for_status()
        
        response_data = response.json()
        
        # Log session ID information
        if 'sessionId' in response_data:
            print(f"[DEBUG] Found sessionId at root level: {response_data['sessionId']}")
        elif 'session' in response_data and 'token' in response_data['session']:
            print(f"[DEBUG] Found session token: {response_data['session']['token']}")
        elif 'context' in response_data and 'sessionId' in response_data['context']:
            print(f"[DEBUG] Found sessionId in context: {response_data['context']['sessionId']}")
        elif 'flightsSessionId' in response_data:
            print(f"[DEBUG] Found flightsSessionId: {response_data['flightsSessionId']}")
        else:
            # Look deeper for session IDs
            print("[DEBUG] Session ID not found in common locations, searching deeper...")
            try:
                response_str = json.dumps(response_data)
                if 'sessionId' in response_str:
                    print("[DEBUG] A sessionId exists somewhere in the response")
                if 'token' in response_str:
                    print("[DEBUG] A token exists somewhere in the response")
            except:
                print("[DEBUG] Could not search deeper for session IDs")
        
        print("[DEBUG] Returning original SkyScanner API response structure")
        return Response(response_data)
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        print(f"[ERROR] SkyScanner API request failed: {error_msg}")
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def search_flights_complete(request):
    """Process subsequent requests for incomplete flight search results"""
    print("="*40)
    print("[DEBUG] search_flights_complete endpoint was called")
    print("[DEBUG] Request method:", request.method)
    print("[DEBUG] Request GET params:", dict(request.GET))
    print("="*40)
    
    session_id = request.GET.get('sessionId', '')
    
    if not session_id:
        print("[ERROR] No sessionId provided in request")
        return Response({"error": "session ID is required"}, status=400)
    
    print(f"[DEBUG] search_flights_complete called with session_id: {session_id}")
    
    # Check if sessionId looks like base64
    try:
        # Try to decode to check if it's base64
        decoded = base64.b64decode(session_id)
        print(f"[DEBUG] sessionId appears to be base64 encoded. Decoded: {decoded[:30]}...")
        
        # Try to parse as JSON if it looks like JSON
        if decoded.startswith(b'{') and decoded.endswith(b'}'):
            try:
                decoded_json = json.loads(decoded)
                print(f"[DEBUG] sessionId decoded to JSON: {decoded_json}")
                print("[WARNING] This looks like a client-generated sessionId, not from SkyScanner API")
            except:
                print("[DEBUG] Base64 decoded value is not valid JSON")
    except:
        print("[DEBUG] sessionId is not base64 encoded, likely a genuine SkyScanner token")
    
    # API endpoint
    api_url = "https://sky-scanner3.p.rapidapi.com/flights/search-incomplete"
    print(f"[DEBUG] Using API URL: {api_url}")
    
    # set API call parameters - SkyScanner expects sessionId
    querystring = {
        "sessionId": session_id
    }
    
    # optional filter parameters
    stops = request.GET.get('stops', '')
    sort = request.GET.get('sort', '')
    airlines = request.GET.get('airlines', '')
    
    # add optional parameters only if they are provided
    if stops:
        querystring["stops"] = stops
    if sort:
        querystring["sort"] = sort
    if airlines:
        querystring["airlines"] = airlines
        
    # other optional parameters
    market = request.GET.get('market', '')
    locale = request.GET.get('locale', '')
    currency = request.GET.get('currency', '')
    cookie = request.GET.get('cookie', '')
    
    if market:
        querystring["market"] = market
    if locale:
        querystring["locale"] = locale
    if currency:
        querystring["currency"] = currency
    if cookie:
        querystring["cookie"] = cookie
    
    print(f"[DEBUG] API call parameters: {querystring}")
    
    try:
        print(f"[DEBUG] Making request to SkyScanner API with sessionId parameter...")
        
        # Make the API call
        response = requests.get(
            api_url, 
            headers=DEFAULT_HEADERS, 
            params=querystring
        )
        
        print(f"[DEBUG] API response received with status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"[DEBUG] Response content: {response.text}")
            
            # If the sessionId format is wrong, try with token parameter instead
            if response.status_code == 400 and "Invalid format" in response.text:
                print("[DEBUG] Trying again with 'token' parameter instead of 'sessionId'")
                
                # Use token parameter instead of sessionId
                token_querystring = querystring.copy()
                token_querystring.pop('sessionId', None)
                token_querystring['token'] = session_id
                
                print(f"[DEBUG] New API call parameters: {token_querystring}")
                
                response = requests.get(
                    api_url, 
                    headers=DEFAULT_HEADERS, 
                    params=token_querystring
                )
                
                print(f"[DEBUG] Second attempt API response status code: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"[DEBUG] Second attempt response content: {response.text}")
        
        # Raise exception for bad responses
        response.raise_for_status()
        
        # Parse JSON response
        response_data = response.json()
        print(f"[DEBUG] API response successfully parsed to JSON")
        
        # Format the response to be consistent with search_flights
        formatted_response = {
            "status": True,
            "message": "Flight search completed successfully",
            "data": response_data
        }
        
        print("[DEBUG] Returning formatted response to client")
        return Response(formatted_response)
        
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        print(f"[ERROR] API request failed: {error_msg}")
        
        # Return a special error code so the frontend knows to use the initial search results
        return Response({
            "status": False,
            "message": f"SkyScanner API 호출 오류: {error_msg}",
            "data": None,
            "errorCode": "API_UNAVAILABLE"
        }, status=500)

@api_view(['GET'])
def get_flight_details(request):
    """Flight details API"""
    token = request.GET.get('token', '')
    itinerary_id = request.GET.get('itineraryId', '')
    
    if not token or not itinerary_id:
        return Response({"error": "Token and itineraryId are required"}, status=400)
    
    querystring = {
        "token": token,
        "itineraryId": itinerary_id
    }
    
    try:
        response = requests.get(FLIGHT_DETAIL_URL, headers=DEFAULT_HEADERS, params=querystring)
        response.raise_for_status()
        return Response(response.json())
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)

