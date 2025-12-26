from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SearchHistory, Airport
import json
import os
from dotenv import load_dotenv

# API 키를 환경 변수에서 로드
load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '0e8e728d6dmsh90bb05c3c37e094p17e44fjsn4f55039ba30b')  # 실제 프로덕션에서는 이 키를 환경 변수로 설정
RAPIDAPI_HOST = "sky-scanner3.p.rapidapi.com"

# 하드코딩된 키가 있는지 확인 (디버깅용)
print(f"\n==== API KEY CHECK ====")
print(f"Using API Key: {RAPIDAPI_KEY[:5]}...{RAPIDAPI_KEY[-5:]}")  # 보안을 위해 키의 일부만 출력
print(f"Using API Host: {RAPIDAPI_HOST}")

# API 엔드포인트 URL
AUTO_COMPLETE_URL = "https://sky-scanner3.p.rapidapi.com/flights/auto-complete"
SEARCH_ROUNDTRIP_URL = "https://sky-scanner3.p.rapidapi.com/flights/search-roundtrip"
SEARCH_ONEWAY_URL = "https://sky-scanner3.p.rapidapi.com/flights/search-one-way"
FLIGHT_DETAIL_URL = "https://sky-scanner3.p.rapidapi.com/flights/detail"

# 기본 헤더
DEFAULT_HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

@api_view(['GET'])
def get_airports(request):
    """공항 자동완성 API"""
    query = request.GET.get('query', '')
    
    if not query:
        return Response({"error": "Query parameter is required"}, status=400)
    
    querystring = {"query": query}
    
    try:
        response = requests.get(AUTO_COMPLETE_URL, headers=DEFAULT_HEADERS, params=querystring)
        response.raise_for_status()  # 에러 발생시 예외 발생
        
        # 공항 자동완성 검색은 기록하지 않음 (너무 많은 데이터 생성 방지)
        
        return Response(response.json())
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def search_flights(request):
    """항공편 검색 API (왕복/편도)"""
    trip_type = request.GET.get('trip_type', 'round')  # 'round' 또는 'one-way'
    from_entity_id = request.GET.get('fromEntityId', '')
    to_entity_id = request.GET.get('toEntityId', '')
    depart_date = request.GET.get('departDate', '')
    return_date = request.GET.get('returnDate', '')
    cabin_class = request.GET.get('cabinClass', 'economy')
    adults = request.GET.get('adults', '1')
    children = request.GET.get('children', '0')
    infants = request.GET.get('infants', '0')
    
    # 디버깅을 위한 요청 정보 출력
    print("\n==== FLIGHT SEARCH REQUEST ====")
    print(f"Trip Type: {trip_type}")
    print(f"From: {from_entity_id}")
    print(f"To: {to_entity_id}")
    print(f"Depart Date: {depart_date}")
    print(f"Return Date: {return_date}")
    print(f"Cabin Class: {cabin_class}")
    print(f"Adults: {adults}, Children: {children}, Infants: {infants}")
    
    if not from_entity_id:
        return Response({"error": "From location is required"}, status=400)
    
    # 기본 쿼리 파라미터
    querystring = {
        "fromEntityId": from_entity_id,
        "toEntityId": to_entity_id,
        "cabinClass": cabin_class,
        "adults": adults,
        "children": children,
        "infants": infants
    }
    
    # 출발 날짜가 있으면 추가
    if depart_date:
        querystring["departDate"] = depart_date
    
    # 왕복인 경우 돌아오는 날짜도 추가
    if trip_type == 'round' and return_date:
        querystring["returnDate"] = return_date
        url = SEARCH_ROUNDTRIP_URL
    else:
        url = SEARCH_ONEWAY_URL
    
    print(f"\nAPI URL: {url}")
    print(f"Query Params: {querystring}")
    print(f"API Headers: {DEFAULT_HEADERS}")
    
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, params=querystring)
        print(f"\nAPI Response Status: {response.status_code}")
        
        # 응답 시작 부분만 출력 (너무 길어질 수 있음)
        response_preview = str(response.text)[:500] + "..." if len(response.text) > 500 else response.text
        print(f"API Response Preview: {response_preview}")
        
        response.raise_for_status()
        
        # 검색 기록 저장
        if depart_date and to_entity_id:
            try:
                # 로그인한 사용자이면 사용자 정보 포함하여 저장
                user = request.user if request.user.is_authenticated else None
                
                # DB 테이블이 없는 경우에 대비한 예외 처리 추가
                SearchHistory.objects.create(
                    user=user,  # 사용자 정보 추가
                    origin=from_entity_id,
                    destination=to_entity_id,
                    departure_date=depart_date,
                    return_date=return_date if trip_type == 'round' and return_date else None
                )
            except Exception as e:
                print(f"Error saving search history: {e}")
                # 오류가 발생해도 계속 진행
        
        response_data = response.json()
        
        # 응답 데이터 구조 검사
        print(f"\nResponse Data Keys: {response_data.keys() if isinstance(response_data, dict) else 'Not a dict'}")
        if isinstance(response_data, dict) and 'data' in response_data:
            data_preview = str(response_data['data'])[:500] + "..." if len(str(response_data['data'])) > 500 else str(response_data['data'])
            print(f"Data Preview: {data_preview}")
        
        return Response(response_data)
    except requests.exceptions.RequestException as e:
        print(f"\nAPI Error: {e}")
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_flight_details(request):
    """항공편 상세 정보 API"""
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

@api_view(['GET'])
def get_search_history(request):
    """사용자의 최근 검색 기록을 반환"""
    try:
        # 인증된 사용자인지 확인
        if not request.user.is_authenticated:
            return Response({"error": "로그인이 필요합니다."}, status=401)
            
        # 현재 로그인한 사용자의 최신 검색 기록 10개 가져오기
        try:
            history = SearchHistory.objects.filter(user=request.user).order_by('-search_date')[:10]
            data = [
                {
                    "id": item.id,
                    "origin": item.origin,
                    "destination": item.destination,
                    "departure_date": item.departure_date,
                    "return_date": item.return_date,
                    "search_date": item.search_date
                }
                for item in history
            ]
            return Response({"results": data})
        except Exception as e:
            # 테이블이 없는 경우 등의 오류 처리
            print(f"Error retrieving search history: {e}")
            return Response({"results": []})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
