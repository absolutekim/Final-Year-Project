<template>
  <!-- Destination detail page container -->
  <v-container class="destination-detail-container">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="destination-detail-card" elevation="4">
          <!-- Loading state -->
          <v-card v-if="loading" class="text-center pa-6">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <div class="mt-4">🔄 Loading data...</div>
          </v-card>

          <!-- Error state -->
          <v-alert v-else-if="error" type="error" class="text-center">
            🚨 Error: {{ error }}
          </v-alert>

          <!-- Data display -->
          <template v-else>
            <!-- Header image -->
            <v-img
              v-if="destination.image"
              :src="destination.image"
              height="300"
              cover
              class="destination-detail-image"
            ></v-img>

            <!-- Title section -->
            <v-card-title class="text-h4 font-weight-bold d-flex align-center flex-wrap">
              {{ destination.name }}
              <v-chip
                color="info"
                variant="outlined"
                class="ml-2"
              >
                {{ destination.country }}
              </v-chip>
            </v-card-title>

            <!-- Like button section -->
            <div class="like-button-container px-4">
              <like-button 
                :location-id="Number(destination.id)" 
                :initial-liked="destination.user_has_liked"
                @like-changed="onLikeChanged"
              />
            </div>

            <v-card-text>
              <!-- Basic information -->
              <v-row>
                <v-col cols="12">
                  <h3 class="text-h6 mb-3">Basic Information</h3>
                  <v-chip
                    color="primary"
                    variant="outlined"
                    class="mr-2 mb-2"
                  >
                    {{ destination.type }}
                  </v-chip>
                  
                  <div v-if="destination.subcategories" class="my-2">
                    <v-chip
                      v-for="(subcat, index) in destination.subcategories"
                      :key="index"
                      color="secondary"
                      variant="outlined"
                      class="mr-2 mb-2"
                    >
                      {{ subcat }}
                    </v-chip>
                  </div>

                  <div v-if="destination.subtypes" class="my-2">
                    <v-chip
                      v-for="(subtype, index) in destination.subtypes"
                      :key="index"
                      color="success"
                      variant="outlined"
                      class="mr-2 mb-2"
                    >
                      {{ subtype }}
                    </v-chip>
                  </div>

                  <div v-if="destination.description" class="mt-4 text-body-1">
                    {{ destination.description }}
                  </div>
                </v-col>

                <!-- Address information -->
                <v-col cols="12" md="6">
                  <h3 class="text-h6 mb-3">Address Information</h3>
                  <v-list>
                    <v-list-item v-if="destination.address">
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-map-marker</v-icon>
                      </template>
                      <v-list-item-title>Address</v-list-item-title>
                      <v-list-item-subtitle>{{ destination.address }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item v-if="destination.local_address">
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-map-marker-outline</v-icon>
                      </template>
                      <v-list-item-title>Local Address</v-list-item-title>
                      <v-list-item-subtitle>{{ destination.local_address }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item v-if="destination.city || destination.state">
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-city</v-icon>
                      </template>
                      <v-list-item-title>City/State</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ [destination.city, destination.state].filter(Boolean).join(', ') }}
                      </v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item v-if="destination.postal_code">
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-post</v-icon>
                      </template>
                      <v-list-item-title>Postal Code</v-list-item-title>
                      <v-list-item-subtitle>{{ destination.postal_code }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item v-if="destination.street1 || destination.street2">
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-road-variant</v-icon>
                      </template>
                      <v-list-item-title>Street Address</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ [destination.street1, destination.street2].filter(Boolean).join(' ') }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>

                <!-- Contact and location information -->
                <v-col cols="12" md="6">
                  <h3 class="text-h6 mb-3">Additional Information</h3>
                  <v-list>
                    <v-list-item v-if="destination.website">
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-web</v-icon>
                      </template>
                      <v-list-item-title>Website</v-list-item-title>
                      <v-list-item-subtitle>
                        <a :href="destination.website" target="_blank">{{ destination.website }}</a>
                      </v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item v-if="destination.email">
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-email</v-icon>
                      </template>
                      <v-list-item-title>Email</v-list-item-title>
                      <v-list-item-subtitle>
                        <a :href="`mailto:${destination.email}`">{{ destination.email }}</a>
                      </v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item v-if="destination.latitude && destination.longitude">
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-crosshairs-gps</v-icon>
                      </template>
                      <v-list-item-title>Coordinates</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ destination.latitude }}, {{ destination.longitude }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>
              </v-row>

              <!-- Map Container -->
              <v-row v-if="destination.latitude && destination.longitude" class="mt-4">
                <v-col cols="12">
                  <h3 class="text-h6 mb-3">Location Map</h3>
                  <v-alert v-if="mapError" type="warning" class="mb-3">
                    {{ mapError }}
                  </v-alert>
                  <div
                    id="map"
                    ref="mapContainer"
                    style="width: 100%; height: 400px; border-radius: 8px;"
                  ></div>
                </v-col>
              </v-row>

              <!-- Reviews section -->
              <v-row class="mt-4">
                <v-col cols="12">
                  <h3 class="text-h6 mb-3">Reviews</h3>
                  
                  <!-- Review form for creating new reviews -->
                  <div v-if="isAuthenticated && !isEditingReview">
                    <review-form 
                      :location-id="Number(destination.id)" 
                      @review-submitted="onReviewSubmitted"
                      ref="reviewForm"
                    />
                  </div>
                  
                  <!-- Review form for editing existing reviews -->
                  <div v-if="isEditingReview">
                    <review-form 
                      :location-id="Number(destination.id)" 
                      :existing-review="currentEditingReview"
                      @review-submitted="onReviewUpdated"
                      @cancel="cancelEditReview"
                      ref="editReviewForm"
                    />
                  </div>
                  
                  <!-- Reviews list -->
                  <review-list 
                    :location-id="Number(destination.id)" 
                    @edit-review="startEditReview"
                    ref="reviewList"
                  />
                </v-col>
              </v-row>
            </v-card-text>

            <!-- Back button -->
            <v-card-actions class="pa-4">
              <v-btn
                color="primary"
                variant="outlined"
                block
                @click="$router.push('/destinations')"
              >
                <v-icon left>mdi-arrow-left</v-icon>
                Back to List
              </v-btn>
            </v-card-actions>
          </template>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
/* eslint-disable no-undef */
import axios from 'axios';
import LikeButton from '@/components/LikeButton.vue';
import ReviewForm from '@/components/ReviewForm.vue';
import ReviewList from '@/components/ReviewList.vue';

/**
 * Destination Detail View
 * Displays comprehensive information about a specific travel destination
 * Includes basic info, address details, contact info, and user reviews
 */
export default {
  components: {
    LikeButton,
    ReviewForm,
    ReviewList
  },
  data() {
    return {
      destination: {},
      loading: true,
      error: null,
      isEditingReview: false,
      currentEditingReview: null,
      map: null,
      mapLoaded: false,
      mapError: null,
      mapInitRetries: 0, // 지도 초기화 재시도 횟수
      coordinatesText: '',
      routeCoordinates: [],
      routeMarkers: [],
      routePolyline: null,
      routeInfoWindows: [],
      exampleCoordinates: '71.16983 25.783571 70.97685 25.97946 70.66463 23.680859 69.94744 23.187012 69.93274 23.270948 69.88493 23.25117',
      handleWindowResize: null
    };
  },
  computed: {
    /**
     * Check if user is authenticated
     * @returns {boolean} Authentication status
     */
    isAuthenticated() {
      return !!localStorage.getItem('access_token');
    }
  },
  created() {
    try {
      // Add authentication token to headers if available
      const token = localStorage.getItem('access_token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      // 데이터 로딩 시작
      this.loading = true;
      
      // 비동기로 목적지 데이터 가져오기
      axios.get(`http://localhost:8000/api/destinations/${this.$route.params.id}/`, {
        headers
      }).then(response => {
      this.destination = response.data;
      console.log('Destination details:', this.destination);
      
      // Add to recently viewed destinations
      this.addToRecentlyViewed(this.destination);
      }).catch(err => {
        this.error = err.message;
        console.error("Failed to load data:", err);
      }).finally(() => {
        // 데이터 로딩 완료 플래그 설정
        this.loading = false;
      });
    } catch (err) {
      this.error = err.message;
      console.error("Failed to load data:", err);
      this.loading = false;
    }
  },
  methods: {
    /**
     * Handle like status change event from like button
     * @param {boolean} isLiked - New like status
     */
    onLikeChanged(isLiked) {
      this.destination.user_has_liked = isLiked;
    },
    
    /**
     * Handle new review submission
     * @param {Object} review - New review data
     */
    onReviewSubmitted(review) {
      console.log('Review submitted:', review);
      // Refresh reviews list
      if (this.$refs.reviewList) {
        this.$refs.reviewList.fetchReviews();
      }
    },
    
    /**
     * Start editing an existing review
     * @param {Object} review - Review to edit
     */
    startEditReview(review) {
      console.log('Starting review edit:', review);
      this.isEditingReview = true;
      this.currentEditingReview = review;
    },
    
    /**
     * Cancel review editing mode
     */
    cancelEditReview() {
      console.log('Cancelled review edit');
      this.isEditingReview = false;
      this.currentEditingReview = null;
    },
    
    /**
     * Handle review update completion
     * @param {Object} review - Updated review data
     */
    onReviewUpdated(review) {
      console.log('Review updated:', review);
      // Refresh reviews list
      if (this.$refs.reviewList) {
        this.$refs.reviewList.fetchReviews();
      }
      this.isEditingReview = false;
      this.currentEditingReview = null;
    },
    
    /**
     * Add destination to recently viewed list in localStorage
     * Stores limited information for quick access later
     * @param {Object} destination - Destination to save to recently viewed
     */
    addToRecentlyViewed(destination) {
      if (!destination || !destination.id) return;
      
      try {
        // Get recently viewed destinations from localStorage
        let recentlyViewed = JSON.parse(localStorage.getItem('recentlyViewed') || '[]');
        
        // Remove if already exists (to update with latest info)
        recentlyViewed = recentlyViewed.filter(item => item.id !== destination.id);
        
        // Create viewed info object with essential details
        const viewedInfo = {
          id: destination.id,
          name: destination.name,
          country: destination.country,
          subcategories: destination.subcategories,
          subtypes: destination.subtypes,
          timestamp: new Date().toISOString()
        };
        
        // Add to the beginning of the array
        recentlyViewed.unshift(viewedInfo);
        
        // Keep only the 10 most recent
        if (recentlyViewed.length > 10) {
          recentlyViewed = recentlyViewed.slice(0, 10);
        }
        
        // Save to localStorage
        localStorage.setItem('recentlyViewed', JSON.stringify(recentlyViewed));
        console.log('Added to recently viewed:', destination.name);
      } catch (error) {
        console.error('Error saving to recently viewed:', error);
      }
    },
    
    /**
     * Google Maps API 스크립트를 불러옵니다.
     */
    loadGoogleMapsScript() {
      console.log('Google Maps API 로드 시작');
      
      // 이미 로드되었는지 확인
      if (window.google && window.google.maps) {
        console.log('Google Maps API 이미 로드됨');
        // DOM이 완전히 업데이트된 후에 실행
        this.$nextTick(() => {
          this.initMap();
        });
        return;
      }
      
      const API_KEY = 'AIzaSyAnJWxpGIPrDueHMNX_1xkopRALQXCeZOE';
      
      // 전역 콜백 함수 정의
      window.initGoogleMap = () => {
        console.log('Google Maps API 로드 완료 (콜백)');
        // DOM이 완전히 업데이트된 후에 실행
        this.$nextTick(() => {
          // 충분한 지연시간 후 초기화 (DOM 렌더링 완료 대기)
          setTimeout(() => {
            this.initMap();
          }, 500);
        });
      };
      
      // 스크립트 요소 생성 - 비동기 로드 설정 (Google 권장사항)
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}&callback=initGoogleMap&loading=async`;
      script.async = true;
      script.defer = true;
      
      // 스크립트 로드 오류 처리
      script.onerror = () => {
        console.error('Google Maps API 스크립트 로드 실패');
        this.mapError = "Google Maps API를 불러오는데 실패했습니다.";
        this.mapLoaded = true;
      };
      
      // DOM에 스크립트 추가
      document.head.appendChild(script);
      console.log('Google Maps API 스크립트 태그 추가됨');
    },
    
    /**
     * 요소의 디버그 정보를 확인합니다.
     */
    debugElement(elementId) {
      const element = document.getElementById(elementId);
      if (!element) {
        console.log(`요소 ${elementId}가 존재하지 않음`);
        return;
      }
      
      console.log(`요소 ${elementId} 상태:`, {
        width: element.offsetWidth,
        height: element.offsetHeight,
        display: window.getComputedStyle(element).display,
        visibility: window.getComputedStyle(element).visibility,
        position: window.getComputedStyle(element).position,
        parent: element.parentElement ? element.parentElement.tagName : 'none'
      });
    },
    
    /**
     * 주어진 위치 좌표로 구글 맵을 초기화합니다.
     */
    initMap() {
      console.log('지도 초기화 시작');
      
      if (!this.destination || !this.destination.latitude || !this.destination.longitude) {
        console.log('목적지 좌표 없음');
        this.mapLoaded = true;
        return;
      }
      
      try {
        const lat = parseFloat(this.destination.latitude);
        const lng = parseFloat(this.destination.longitude);
        
        if (isNaN(lat) || isNaN(lng)) {
          console.log('유효하지 않은 좌표:', this.destination.latitude, this.destination.longitude);
          this.mapError = "유효하지 않은 좌표입니다.";
          this.mapLoaded = true;
          return;
        }
        
        // 지도를 표시할 DOM 요소 확인 - ref와 id 둘 다 시도
        const mapElement = this.$refs.mapContainer || document.getElementById('map');
        if (!mapElement) {
          console.log('지도 요소가 아직 준비되지 않았습니다. 잠시 후 다시 시도합니다.');
          
          // 최대 재시도 횟수 체크
          if (this.mapInitRetries >= 5) {
            console.error('지도 초기화 최대 재시도 횟수 초과');
            this.mapError = "지도 요소를 찾을 수 없습니다. 페이지를 새로고침 해보세요.";
            this.mapLoaded = true;
            return;
          }
          
          this.mapInitRetries++;
          // 약간의 지연 후 다시 시도
          setTimeout(() => {
            this.initMap();
          }, 1000); // 지연 시간 증가
          return;
        }
        
        console.log('지도 요소 준비됨, 크기:', mapElement.offsetWidth, 'x', mapElement.offsetHeight);
        
        // 지도 요소가 보이지 않거나 크기가 0인 경우 체크
        if (mapElement.offsetWidth === 0 || mapElement.offsetHeight === 0) {
          console.log('지도 요소의 크기가 0입니다. 잠시 후 다시 시도합니다.');
          
          if (this.mapInitRetries >= 5) {
            console.error('지도 초기화 최대 재시도 횟수 초과');
            this.mapError = "지도 요소의 크기가 0입니다. 페이지를 새로고침 해보세요.";
            this.mapLoaded = true;
            return;
          }
          
          this.mapInitRetries++;
          setTimeout(() => {
            this.initMap();
          }, 1000);
          return;
        }
        
        const position = { lat, lng };
        
        // Google Maps 객체 생성
        try {
          this.map = new google.maps.Map(mapElement, {
            center: position,
            zoom: 14,
            mapTypeControl: true,
            fullscreenControl: true
          });
          
          console.log('지도 객체 생성됨');
        } catch (mapError) {
          console.error('지도 객체 생성 오류:', mapError);
          this.mapError = "지도 객체를 생성하는 데 실패했습니다.";
          this.mapLoaded = true;
          return;
        }
        
        // 위치 마커 추가
        const marker = new google.maps.Marker({
          position: position,
          map: this.map,
          title: this.destination.name,
          animation: google.maps.Animation.DROP
        });
        
        // 정보창 추가
        const infoContent = `
          <div class="info-window">
            <h3>${this.destination.name}</h3>
            ${this.destination.address ? `<p>${this.destination.address}</p>` : ''}
            <p>좌표: ${lat.toFixed(6)}, ${lng.toFixed(6)}</p>
          </div>
        `;
        
        const infoWindow = new google.maps.InfoWindow({
          content: infoContent
        });
        
        // 마커 클릭 시 정보창 표시
        marker.addListener('click', () => {
          infoWindow.open(this.map, marker);
        });
        
        // 지도 초기화 시 정보창 자동 표시
        infoWindow.open(this.map, marker);
        
        console.log('지도 초기화 완료');
        this.mapLoaded = true;
        
        // 지도가 완전히 로드되었을 때 이벤트 리스너 추가
        if (this.map && google.maps.event) {
          google.maps.event.addListenerOnce(this.map, 'idle', () => {
            console.log('지도 렌더링 완료 (idle 이벤트)');
            this.mapLoaded = true;
          });
        }
      } catch (error) {
        console.error('지도 초기화 오류:', error);
        this.mapError = "지도를 불러오는 중 오류가 발생했습니다.";
        this.mapLoaded = true;
      }
    },
    showRouteExample() {
    },
  },
  mounted() {
    console.log('컴포넌트 마운트됨');
    
    // 창 크기 변경 이벤트 핸들러 정의
    this.handleWindowResize = () => {
      if (this.map) {
        google.maps.event.trigger(this.map, 'resize');
        
        // 지도 중심 재설정
        if (this.destination?.latitude && this.destination?.longitude) {
          const lat = parseFloat(this.destination.latitude);
          const lng = parseFloat(this.destination.longitude);
          const center = new google.maps.LatLng(lat, lng);
          this.map.setCenter(center);
        }
      }
    };
    
    // 지도 초기화 함수를 재정의 (v-else에 의한 DOM 요소 변경 문제 해결)
    const ensureMapInitialization = () => {
      console.log('지도 초기화 확인 중');
      
      // DOM이 완전히 렌더링된 후 실행
      this.$nextTick(() => {
        // 로딩이 완료되고 위치 정보가 있는지 확인
        if (!this.loading && this.destination?.latitude && this.destination?.longitude) {
          console.log('조건 충족, 지도 컨테이너 확인 중');
          
          // DOM에서 지도 컨테이너 요소 확인
          const mapEl = this.$refs.mapContainer || document.getElementById('map');
          if (mapEl) {
            console.log('지도 컨테이너 발견, 크기:', mapEl.offsetWidth, 'x', mapEl.offsetHeight);
            this.debugElement('map');
            
            // 충분한 시간을 두고 지도 스크립트 로드
            setTimeout(() => {
              this.loadGoogleMapsScript();
            }, 300);
          } else {
            console.log('지도 컨테이너를 찾을 수 없음, 재시도 예정');
            
            // 재시도 횟수 제한
            if (this.mapInitRetries >= 10) {
              console.error('지도 초기화 최대 재시도 횟수 초과 - 더 이상 시도하지 않음');
              this.mapError = "지도 컨테이너를 찾을 수 없습니다.";
              return;
            }
            
            // 재시도 횟수 증가
            this.mapInitRetries++;
            // 짧은 간격으로 몇 번 더 시도
            setTimeout(ensureMapInitialization, 200);
          }
        }
      });
    };
    
    // 로딩 상태 변화 감시
    this.$watch('loading', (newValue) => {
      if (newValue === false) {
        console.log('데이터 로딩 완료, destination:', this.destination);
        // 지도 초기화 다시 시도
        this.mapInitRetries = 0;
        this.mapError = null;
        ensureMapInitialization();
      }
    });
    
    // 컴포넌트가 마운트된 직후에도 시도 (이미 로딩이 완료된 경우)
    if (!this.loading && this.destination?.latitude && this.destination?.longitude) {
      this.mapInitRetries = 0; 
      ensureMapInitialization();
    }
    
    // 창 크기 변경 이벤트 리스너
    window.addEventListener('resize', this.handleWindowResize);
    
    // 뷰의 조건부 렌더링에 의해 지도 컨테이너가 나중에 나타날 수 있음
    // DOM 변경을 감시하여 지도 컨테이너가 나타나면 초기화
    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
          // 새로 추가된 노드 중 지도 컨테이너 확인
          let mapAdded = false;
          for (const node of mutation.addedNodes) {
            if (node.id === 'map' || 
                (node.nodeType === Node.ELEMENT_NODE && node.querySelector && node.querySelector('#map'))) {
              mapAdded = true;
              break;
            }
          }
          
          if (mapAdded) {
            console.log('지도 컨테이너가 DOM에 추가됨, 다시 초기화 시도');
            this.mapError = null;
            this.mapInitRetries = 0;
            ensureMapInitialization();
            break;
          }
        }
      }
    });
    
    // body를 관찰하여 DOM 변경 감지
    observer.observe(document.body, { childList: true, subtree: true });
    
    // 컴포넌트 해제 시 리소스 정리
    this.$options._beforeDestroy = this.$options._beforeDestroy || [];
    this.$options._beforeDestroy.push(() => {
      observer.disconnect();
      window.removeEventListener('resize', this.handleWindowResize);
    });
  },
  
  beforeUnmount() {
    // 이벤트 리스너 정리
    window.removeEventListener('resize', this.handleWindowResize);
  },
};
</script>

<style scoped>
/* Container styling */
.destination-detail-container {
  padding-top: 2rem;
  padding-bottom: 2rem;
  background-color: #f5f5f5;
  min-height: 100vh;
}

/* Card styling */
.destination-detail-card {
  border-radius: 12px;
  overflow: hidden;
}

/* Header image styling */
.destination-detail-image {
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

/* Card title styling */
.v-card-title {
  padding: 1.5rem;
  background-color: white;
}

/* Card content styling */
.v-card-text {
  padding: 1.5rem;
}

/* Like button container styling */
.like-button-container {
  margin: 0 0 10px 0;
}

/* Link styling */
a {
  color: #1976d2;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .destination-detail-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
  }
}
</style> 