import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/flights/";

// 항공편 검색 함수
export async function searchFlights(params) {
  try {
    console.log("==== 항공편 검색 요청 ====");
    console.log("검색 파라미터:", params);
    console.log("API URL:", `${API_BASE_URL}search/`);
    
    // 백엔드 API 호출 - 백엔드가 sky-scanner3.p.rapidapi.com을 호출합니다
    const response = await axios.get(`${API_BASE_URL}search/`, {
      params: params
    });

    console.log("==== 항공편 검색 응답 ====");
    console.log("응답 상태:", response.status);
    console.log("응답 헤더:", response.headers);
    console.log("API 응답 데이터:", response.data);
    
    // 응답 구조 분석
    if (response.data) {
      console.log("응답 데이터 타입:", typeof response.data);
      console.log("응답 데이터에 data 키 포함:", 'data' in response.data);
      
      if ('data' in response.data && response.data.data) {
        console.log("data 객체 내 itineraries 포함:", 'itineraries' in response.data.data);
        if ('itineraries' in response.data.data) {
          console.log("itineraries 배열 길이:", response.data.data.itineraries.length);
        }
      }
      
      return response.data;
    } else {
      console.warn("항공편 API 응답에 항공편 정보가 없습니다.");
      return { flights: [] };
    }
  } catch (error) {
    console.error("항공 Django API 요청 실패:", error);
    if (error.response) {
      console.error("에러 응답:", error.response.data);
      console.error("에러 상태:", error.response.status);
    }
    return { flights: [] };
  }
}

// 공항 자동완성 검색 함수
export async function searchAirports(query) {
  try {
    // views.py의 get_airports 함수에 맞게 URL 수정
    const response = await axios.get(`${API_BASE_URL}get-airports/`, {
      params: { query }
    });

    console.log("공항 검색 응답:", response.data);
    // API 응답 구조에 맞게 처리
    return response.data || []; 
  } catch (error) {
    console.error("공항 검색 실패:", error);
    return [];
  }
}

// 항공편 세부 정보 함수
export async function getFlightDetails(token, itineraryId) {
  try {
    // views.py의 get_flight_details 함수에 맞게 URL 수정
    const response = await axios.get(`${API_BASE_URL}get-flight-details/`, {
      params: { token, itineraryId }
    });

    console.log("Flight Details API 응답:", response.data);
    return response.data;
  } catch (error) {
    console.error("항공 getFlightDetails API 오류:", error);
    return {};
  }
}

// 사용자 검색 기록 조회 함수
export async function getSearchHistory() {
  try {
    const token = localStorage.getItem('access_token');
    
    // views.py의 get_search_history 함수에 맞게 URL 수정
    const response = await axios.get(`${API_BASE_URL}get-search-history/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    return response.data;
  } catch (error) {
    console.error("검색 기록 조회 실패:", error);
    if (error.response && error.response.status === 401) {
      // 인증 오류 처리
      return { error: "로그인이 필요합니다." };
    }
    return { results: [] };
  }
}
