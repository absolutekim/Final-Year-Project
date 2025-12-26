<template>
  <div class="container mx-auto p-4">
    <div class="flex flex-wrap items-center justify-between mb-6">       
      <div class="flex items-center">
        <button @click="goBack" class="back-button mr-4">
          <i class="material-icons mr-1">arrow_back</i>
          Back to Search Results
        </button>
        <h1 class="text-2xl font-semibold page-title">Flight Details</h1>
      </div>
    </div>

    <div v-if="isLoading" class="loading-spinner">
      <i class="material-icons">sync</i>
    </div>

    <div v-else-if="error" class="error-message mb-6">
      <div class="font-medium mb-1">An error occurred</div>
      <div>{{ error }}</div>
    </div>

    <div v-else-if="flightDetails" class="card">
      <!-- Flight Summary Information -->
      <div class="card-header">
        <div class="flex flex-wrap justify-between items-center">
          <div>
            <div class="flight-code">
              {{ getAirportCodes(flightDetails.itinerary.legs[0]) }}
            </div>
            <div class="route-name">
              {{ getOriginToDestination(flightDetails.itinerary.legs[0]) }}
            </div>
          </div>
          <div class="text-right">
            <div class="price-display">
              {{ getPriceInfo(flightDetails.itinerary.pricingOptions) }}
            </div>
            <div>Total Price</div>
          </div>
        </div>
      </div>

      <!-- Destination Images -->
      <div class="destination-images grid grid-cols-3 gap-0.5 mt-0.5">
        <div v-for="(image, index) in destinationImages" :key="index" class="destination-image-container relative">
          <img :src="image.url" :alt="image.alt" class="w-full h-32 object-cover" />
          <div v-if="index === 0" class="absolute bottom-0 left-0 w-full p-2 bg-gradient-to-t from-black/70 to-transparent">
            <div class="text-white text-sm font-medium">{{ getDestinationName() }} Visit</div>
          </div>
        </div>
      </div>

      <!-- Flight Details Information -->
      <div class="p-6">
        <div v-for="(leg, legIndex) in flightDetails.itinerary.legs" :key="leg.id" class="flight-section">
          <div class="section-title">
            <i class="material-icons mr-2">{{ legIndex === 0 ? 'flight_takeoff' : 'flight_land' }}</i>   
            {{ legIndex === 0 ? 'Departure Flight' : 'Return Flight' }}
            <div class="ml-auto text-sm font-normal text-gray-500">
              {{ formatDuration(leg.durationMinutes) }} |
              <span v-if="leg.stopCount === 0" class="text-green-600 font-medium">Direct</span>
              <span v-else class="text-orange-500 font-medium">{{ leg.stopCount }} stops</span>
            </div>
          </div>

          <!-- Segment Information (Each Flight) -->
          <div v-for="(segment, index) in leg.segments" :key="segment.id" class="mb-6">
            <div class="segment-card">
              <div class="flex items-start gap-4 mb-4">
                <div class="flex-none">
                  <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden">
                    <img
                      v-if="segment.marketingCarrier && segment.marketingCarrier.logo"
                      :src="segment.marketingCarrier.logo"
                      :alt="segment.marketingCarrier?.name || 'Airline Information'"
                      class="airline-logo"
                    >
                    <span v-else class="text-3xl text-gray-400">아이콘</span>
                  </div>
                </div>
                <div class="flex-grow">
                  <div class="font-medium text-lg">{{ segment.marketingCarrier?.name || 'Airline information not available' }}</div>
                  <div class="text-sm text-gray-500">
                    Flight Number: {{ segment.marketingCarrier?.displayCode || '?' }}{{ segment.flightNumber || '?' }}
                    <span v-if="segment.marketingCarrier && segment.operatingCarrier && segment.marketingCarrier.id !== segment.operatingCarrier.id">
                      (Operated by: {{ segment.operatingCarrier.name }})
                    </span>
                  </div>
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-10 gap-4 mt-6">
                <!-- Departure Information -->
                <div class="md:col-span-4">
                  <div class="time-display mb-1">{{ formatTime(segment.departure) }}</div>
                  <div class="airport-code">{{ segment.origin?.airport?.displayCode || '?' }}</div>      
                  <div class="airport-name text-sm mb-1">{{ segment.origin?.airport?.name || 'Airport information not available' }}</div>
                  <div class="date-display text-sm">{{ formatDate(segment.departure) }}</div>
                </div>

                <!-- Flight Duration -->
                <div class="md:col-span-2 flex flex-col items-center justify-center">
                  <div class="flight-duration-text mb-2">{{ formatDuration(segment.durationMinutes) }}</div>
                  <div class="w-full relative">
                    <div class="flight-duration-bar w-full"></div>
                    <div class="plane-icon absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                      <i class="material-icons text-blue-600">flight</i>
                    </div>
                  </div>
                  <div class="flight-duration-text mt-2">
                    <span v-if="segment.durationMinutes <= 120" class="text-green-600">Short Distance</span>
                    <span v-else-if="segment.durationMinutes <= 360" class="text-orange-500">Medium Distance</span>
                    <span v-else class="text-red-500">Long Distance</span>
                  </div>
                </div>

                <!-- Arrival Information -->
                <div class="md:col-span-4 text-right">
                  <div class="time-display mb-1">{{ formatTime(segment.arrival) }}</div>
                  <div class="airport-code">{{ segment.destination?.airport?.displayCode || '?' }}</div> 
                  <div class="airport-name text-sm mb-1">{{ segment.destination?.airport?.name || 'Airport information not available' }}</div>
                  <div class="date-display text-sm">
                    {{ formatDate(segment.arrival) }}
                    <span v-if="segment.dayChange" class="day-change ml-1">(+{{ segment.dayChange }} days)</span>
                  </div>
                </div>
              </div>

              <!-- Segment Additional Information -->
              <div v-if="segment.goodToKnowItems && segment.goodToKnowItems.length" class="info-badge mt-4">
                <div v-for="(item, idx) in segment.goodToKnowItems" :key="idx" class="text-sm mb-1 last:mb-0">
                  <span v-if="item.badge && item.badge.value" class="bg-blue-600 text-white px-2 py-0.5 rounded-full text-xs mr-2">
                    {{ item.badge.value }}
                  </span>
                  <span v-if="item.body && item.body.value" v-html="formatGoodToKnowText(item.body.value)"></span>
                </div>
              </div>
            </div>

            <!-- Layover Information -->
            <div v-if="index < leg.segments.length - 1 && leg.layovers && leg.layovers[index]" class="layover-info my-4">
              <div class="flex items-center text-gray-500">
                <i class="material-icons mr-2 text-orange-500">schedule</i>
                {{ formatDuration(leg.layovers[index].duration) }} Layover - {{ leg.layovers[index].origin?.name || 'Airport Information Not Available' }}
              </div>
            </div>
          </div>
        </div>

        <!-- Booking Button -->
        <div v-if="flightDetails.itinerary.pricingOptions && flightDetails.itinerary.pricingOptions.length" class="booking-section">
          <div class="booking-title flex items-center">
            <i class="material-icons mr-2 text-blue-600">shopping_cart</i>
            Booking Options
          </div>

          <div v-for="(option, index) in flightDetails.itinerary.pricingOptions" :key="index" class="booking-option">
            <div class="flex flex-wrap justify-between items-center mb-3">
              <div>
                <div class="font-medium text-lg">
                  {{ option.pricingItems && option.pricingItems[0]?.agent?.name || 'Unknown Provider' }} 
                </div>

                <div v-if="option.pricingItems && option.pricingItems[0]?.agent?.rating" class="flex items-center mt-1">
                  <div class="flex">
                    <i v-for="i in 5" :key="i" class="material-icons text-sm mr-0.5" :class="i <= Math.round(option.pricingItems[0].agent.rating.value) ? 'star-rating' : 'empty-star'">
                      star
                    </i>
                  </div>
                  <span class="text-sm text-gray-500 ml-1">
                    {{ option.pricingItems[0].agent.rating.value.toFixed(1) }} ({{ option.pricingItems[0].agent.rating.count }} reviews)
                  </span>
                </div>
              </div>

              <div class="booking-price">
                {{ formatPriceOption(option) }}
              </div>
            </div>

            <a
              v-if="option.pricingItems && option.pricingItems[0]?.uri"
              :href="option.pricingItems[0].uri"
              target="_blank"
              rel="noopener noreferrer"
              class="booking-button"
            >
              <i class="material-icons mr-1 align-middle text-sm">open_in_new</i>
              Book Now
            </a>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center p-8 text-gray-500 bg-gray-50 rounded-lg">
      <i class="material-icons text-4xl mb-2 text-gray-400">flight_off</i>
      <p class="text-lg">Flight information not found.</p>
    </div>

    <!-- Travel tips section -->
    <div v-if="flightDetails" class="travel-tips bg-white rounded-lg shadow-md p-6 mt-6">
      <h2 class="text-xl font-semibold mb-4 flex items-center">
        <i class="material-icons mr-2 text-blue-600">lightbulb</i>
        Travel Tips
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="tip-card p-4 border border-blue-100 rounded-lg bg-blue-50">
          <div class="flex items-start">
            <i class="material-icons text-blue-600 mr-3">luggage</i>
            <div>
              <h3 class="font-medium mb-1">Baggage Check-In</h3>
              <p class="text-sm text-gray-600">Arrive at the airport 2-3 hours before departure to check in your baggage.</p>
            </div>
          </div>
        </div>

        <div class="tip-card p-4 border border-blue-100 rounded-lg bg-blue-50">
          <div class="flex items-start">
            <i class="material-icons text-blue-600 mr-3">security</i>
            <div>
              <h3 class="font-medium mb-1">Security Check</h3>
              <p class="text-sm text-gray-600">Prepare liquids 100ml or less, and laptops and electronic devices separately.</p>
            </div>
          </div>
        </div>

        <div class="tip-card p-4 border border-blue-100 rounded-lg bg-blue-50">
          <div class="flex items-start">
            <i class="material-icons text-blue-600 mr-3">schedule</i>
            <div>
              <h3 class="font-medium mb-1">Time Zone Adjustment</h3>
              <p class="text-sm text-gray-600">Adjust your sleep schedule to match the destination time zone for faster time zone adaptation.</p>
            </div>
          </div>
        </div>

        <div class="tip-card p-4 border border-blue-100 rounded-lg bg-blue-50">
          <div class="flex items-start">
            <i class="material-icons text-blue-600 mr-3">health_and_safety</i>
            <div>
              <h3 class="font-medium mb-1">In-Flight Health</h3>
              <p class="text-sm text-gray-600">Stretch regularly and drink enough water during long flights.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Debug Section (Only used during development) -->
    <div v-if="flightDetails" class="debug-section">
      <details>
        <summary class="debug-title">Debug Information (Development Only)</summary>
        <div class="debug-content">
          <h3 class="text-white font-semibold mb-2">Token: {{ token }}</h3>
          <h3 class="text-white font-semibold mb-2">Itinerary ID: {{ itineraryId }}</h3>
          <pre class="debug-pre">{{ JSON.stringify(flightDetails, null, 2) }}</pre>
        </div>
      </details>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { getFlightDetails } from '@/api/flight';

export default {
  name: 'FlightDetailView',
  props: {
    token: {
      type: String,
      required: true
    },
    itineraryId: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const router = useRouter();

    const flightDetails = ref(null);
    const isLoading = ref(true);
    const error = ref(null);

    // Destination Images (Static)
    const destinationImages = computed(() => {
      // In reality, the images should be dynamically selected based on the destination information from the API response
      return [
        {
          url: 'https://images.unsplash.com/photo-1520986606214-8b456906c813?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
          alt: 'Travel destination image'
        },
        {
          url: 'https://images.unsplash.com/photo-1543336472-fj17ac5ae834?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
          alt: 'Travel destination image'
        },
        {
          url: 'https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
          alt: 'Travel destination image'
        }
      ];
    });

    // Get Destination Name
    const getDestinationName = () => {
      if (!flightDetails.value || !flightDetails.value.itinerary || !flightDetails.value.itinerary.legs || flightDetails.value.itinerary.legs.length === 0) {
        return 'Destination';
      }

      const leg = flightDetails.value.itinerary.legs[0];
      return leg.destination && leg.destination.city
        ? leg.destination.city.name
        : (leg.destination && leg.destination.airport ? leg.destination.airport.name : '목적지');      
    };

    // Get Flight Details
    const fetchFlightDetails = async () => {
      isLoading.value = true;
      error.value = null;

      try {
        const response = await getFlightDetails(props.token, props.itineraryId);
        if (response && response.data) {
          console.log('Flight Details API Response:', response.data);  // Debugging Log

          // Verify Data Structure and Process
          if (response.data.itinerary) {
            // Check if required properties exist
            if (!response.data.itinerary.legs || response.data.itinerary.legs.length === 0) {
              console.warn('No legs data found in the API response');
            }

            // Check Date Format and Convert (if needed)
            if (response.data.itinerary.legs && response.data.itinerary.legs.length > 0) {
              response.data.itinerary.legs.forEach(leg => {
                console.log('Leg data:', leg);
                if (leg.segments && leg.segments.length > 0) {
                  leg.segments.forEach(segment => {
                    console.log('Segment departure:', segment.departure);
                    console.log('Segment arrival:', segment.arrival);
                    // Add processing logic for unusual date formats if needed
                  });
                }
              });
            }
          } else {
            console.warn('No itinerary data found in the API response');
          }

          flightDetails.value = response.data;
        } else {
          error.value = 'Failed to fetch flight information.';
        }
      } catch (err) {
        console.error('Flight Details Error:', err);
        error.value = 'Failed to fetch flight information.';
      } finally {
        isLoading.value = false;
      }
    };

    // Go Back
    const goBack = () => {
      router.back();
    };

    // Formatting Functions
    const formatDate = (dateObj) => {
      if (!dateObj) return 'No date information';

      try {
        // If the API provides a {year, month, day, hour, minute} object
        if (typeof dateObj === 'object' && dateObj.year && dateObj.month && dateObj.day) {
          const date = new Date(dateObj.year, dateObj.month - 1, dateObj.day);
          const options = { year: 'numeric', month: 'short', day: 'numeric', weekday: 'short' };
          return date.toLocaleDateString('ko-KR', options);
        }

        // If it's a string, keep the existing processing method
        const date = new Date(dateObj);
        if (isNaN(date.getTime())) {
          return 'Date information error';
        }

        const options = { year: 'numeric', month: 'short', day: 'numeric', weekday: 'short' };
        return date.toLocaleDateString('ko-KR', options);
      } catch (e) {
        console.error('Date formatting error:', e, dateObj);
        return 'Date information error';
      }
    };

    const formatTime = (dateObj) => {
      if (!dateObj) return 'No time information';

      try {
        // If the API provides a {year, month, day, hour, minute} object
        if (typeof dateObj === 'object' && dateObj.hour !== undefined && dateObj.minute !== undefined) { 
          // Format time and minutes as two-digit numbers
          const hours = dateObj.hour.toString().padStart(2, '0');
          const minutes = dateObj.minute.toString().padStart(2, '0');
          return `${hours}:${minutes}`;
        }

        // If it's a string, keep the existing processing method
        const date = new Date(dateObj);
        if (isNaN(date.getTime())) {
          return 'Time information error';
        }

        return date.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', hour12: true });   
      } catch (e) {
        console.error('Time formatting error:', e, dateObj);
        return 'Time information error';
      }
    };

    const formatDuration = (minutes) => {
      if (!minutes && minutes !== 0) return '';

      const hours = Math.floor(minutes / 60);
      const mins = minutes % 60;
      return `${hours}hours ${mins > 0 ? mins + 'minutes' : ''}`;
    };

    const formatGoodToKnowText = (text) => {
      if (!text) return '';

      // Convert <style0> tags to highlighted text
      return text.replace(/<style0>(.*?)<\/style0>/g, '<span class="font-medium">$1</span>');
    };

    const getAirportCodes = (leg) => {
      if (!leg) return 'No information';

      const originCode = leg.origin && leg.origin.airport ? leg.origin.airport.displayCode : 'No information';
      const destCode = leg.destination && leg.destination.airport ? leg.destination.airport.displayCode : 'No information';

      return `${originCode} - ${destCode}`;
    };

    const getOriginToDestination = (leg) => {
      if (!leg) return 'No information';

      const originName = leg.origin && leg.origin.city ? leg.origin.city.name : (leg.origin && leg.origin.airport ? leg.origin.airport.name : 'No information');
      const destName = leg.destination && leg.destination.city ? leg.destination.city.name : (leg.destination && leg.destination.airport ? leg.destination.airport.name : 'No information');

      return `${originName} - ${destName}`;
    };

    // Extract and format price information
    const getPriceInfo = (pricingOptions) => {
      if (!pricingOptions || pricingOptions.length === 0) {
        return 'No price information';
      }

      try {
        // Use the first price option
        const option = pricingOptions[0];
        if (option.price && option.price.amount && option.price.currencyCode) {
          // Convert price stored in cents to dollars (100 cents = 1 dollar)
          const amount = parseInt(option.price.amount) / 100;
          return `${option.price.currencyCode} ${amount.toFixed(2)}`;
        }

        return 'No price information';
      } catch (e) {
        console.error('Price processing error:', e);
        return 'No price information';
      }
    };

    // Format individual price options
    const formatPriceOption = (option) => {
      if (!option || !option.price) {
        return 'No price information';
      }

      try {
        if (option.price.amount && option.price.currencyCode) {
          // Convert price stored in cents to dollars (100 cents = 1 dollar)
          const amount = parseInt(option.price.amount) / 100;
          return `${option.price.currencyCode} ${amount.toFixed(2)}`;
        }

        return 'No price information';
      } catch (e) {
        console.error('Price processing error:', e);
        return 'No price information';
      }
    };

    onMounted(() => {
      fetchFlightDetails();
    });

    return {
      flightDetails,
      isLoading,
      error,
      destinationImages,
      goBack,
      formatDate,
      formatTime,
      formatDuration,
      formatGoodToKnowText,
      getAirportCodes,
      getOriginToDestination,
      getPriceInfo,
      formatPriceOption,
      getDestinationName
    };
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}

.page-title {
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.back-button {
  display: flex;
  align-items: center;
  color: #3b82f6;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.75rem;
  transition: all 0.2s ease;
  background-color: rgba(59, 130, 246, 0.1);
}

.back-button:hover {
  background-color: rgba(59, 130, 246, 0.2);
  transform: translateX(-5px);
}

.card {
  background-color: white;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
  overflow: hidden;
  border: 1px solid #f0f0f0;
}

.card-header {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  padding: 1.5rem;
}

.flight-code {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.route-name {
  font-weight: 500;
  opacity: 0.9;
}

.price-display {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.flight-section {
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem;
}

.flight-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #1f2937;
}

.segment-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.25rem;
  margin-bottom: 1rem;
  transition: all 0.2s ease;
}

.segment-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.airline-logo {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background-color: #f9fafb;
  padding: 0.25rem;
  border: 1px solid #e5e7eb;
  object-fit: contain;
}

.time-display {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.airport-code {
  font-weight: 700;
  font-size: 1.25rem;
  color: #1f2937;
}

.airport-name {
  color: #4b5563;
}

.date-display {
  color: #6b7280;
}

.flight-duration-bar {
  height: 2px;
  background-color: #e5e7eb;
  position: relative;
}

.flight-duration-bar::before {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #3b82f6;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
}

.flight-duration-bar::after {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #3b82f6;
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

.flight-duration-text {
  font-weight: 500;
  color: #6b7280;
  font-size: 0.9rem;
  text-align: center;
  margin-top: 0.5rem;
}

.info-badge {
  background-color: #eff6ff;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
}

.layover-info {
  border-left: 2px dashed #d1d5db;
  margin-left: 1.5rem;
  padding-left: 1.5rem;
  color: #6b7280;
}

.booking-section {
  border-top: 1px solid #f0f0f0;
  padding-top: 1.5rem;
  margin-top: 1.5rem;
}

.booking-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #1f2937;
}

.booking-option {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1rem;
  margin-bottom: 1rem;
  transition: all 0.2s ease;
}

.booking-option:hover {
  border-color: #bfdbfe;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.booking-price {
  font-size: 1.25rem;
  font-weight: 700;
  color: #3b82f6;
}

.booking-button {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  font-weight: 600;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  transition: all 0.2s ease;
  text-align: center;
  display: block;
  width: 100%;
}

.booking-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.star-rating {
  color: #facc15;
}

.empty-star {
  color: #e5e7eb;
}

.error-message {
  background-color: #fee2e2;
  border-radius: 0.75rem;
  color: #b91c1c;
  padding: 1rem;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.loading-spinner .material-icons {
  animation: spin 1.5s linear infinite;
  font-size: 3rem;
  color: #3b82f6;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.debug-section {
  background-color: #f3f4f6;
  border-radius: 0.75rem;
  margin-top: 2rem;
}

.debug-title {
  cursor: pointer;
  font-weight: 600;
  color: #3b82f6;
  padding: 0.75rem 1rem;
}

.debug-content {
  padding: 1rem;
  max-height: 400px;
  overflow: auto;
  background-color: #1f2937;
  border-radius: 0 0 0.75rem 0.75rem;
}

.debug-pre {
  font-size: 0.75rem;
  color: #f9fafb;
  white-space: pre-wrap;
}

.day-change {
  color: #ef4444;
  font-weight: 500;
}

.destination-images {
  overflow: hidden;
}

.destination-image-container {
  overflow: hidden;
}

.destination-image-container img {
  transition: all 0.5s ease;
}

.destination-image-container:hover img {
  transform: scale(1.1);
}

.plane-icon {
  animation: fly 1.5s infinite ease-in-out;
}

@keyframes fly {
  0%, 100% { transform: translate(-50%, -50%) rotate(0deg); }
  50% { transform: translate(-50%, -50%) rotate(10deg) translateY(-3px); }
}

.tip-card {
  transition: all 0.3s ease;
}

.tip-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(59, 130, 246, 0.15);
}

.travel-tips {
  background-color: white;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
}
</style>