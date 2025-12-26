<template>
  <div class="container mx-auto p-4">
    <!-- Top banner image -->
    <div class="banner-container mb-8 rounded-xl overflow-hidden relative">
      <img src="https://images.unsplash.com/photo-1503220317375-aaad61436b1b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80" 
        alt="banner image" 
        class="w-full h-64 object-cover"
      />
      <div class="absolute inset-0 bg-gradient-to-r from-blue-900/70 to-indigo-900/40 flex flex-col justify-center px-8 md:px-12">
        <h1 class="text-4xl md:text-5xl font-bold mb-2 text-white">Flight Search</h1>
        <p class="text-white/90 text-lg md:text-xl max-w-xl">Find the best flight to your destination</p>
      </div>
    </div>
    
    <!-- Search form -->
    <div class="search-form p-6 mb-8">
      <div class="flex gap-6 mb-5">
        <div class="flex gap-2 items-center">
          <input type="radio" id="round-trip" v-model="tripType" value="round" class="w-5 h-5 accent-blue-600">
          <label for="round-trip" class="text-lg font-medium">Round Trip</label>
        </div>
        <div class="flex gap-2 items-center">
          <input type="radio" id="one-way" v-model="tripType" value="one-way" class="w-5 h-5 accent-blue-600">
          <label for="one-way" class="text-lg font-medium">One Way</label>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
        <!-- Departure -->
        <div class="relative">
          <label class="block mb-2 font-medium text-gray-700">Departure</label>
          <div class="relative">
            <i class="material-icons absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">flight_takeoff</i>
            <input 
              type="text" 
              v-model="originQuery" 
              @input="searchOriginAirports" 
              placeholder="City or Airport" 
              class="w-full pl-10 pr-3 py-3 border rounded-lg"
            >
          </div>
          <div v-if="showOriginDropdown && originAirports.length" class="dropdown-menu absolute z-10 bg-white w-full mt-1 max-h-64 overflow-y-auto">
            <div 
              v-for="airport in originAirports" 
              :key="airport.presentation.id" 
              @click="selectOrigin(airport)"
              class="dropdown-item p-3 cursor-pointer"
            >
              <div class="font-medium">{{ airport.presentation.title }}</div>
              <div class="text-sm text-gray-500">{{ airport.presentation.subtitle }}</div>
            </div>
          </div>
        </div>
        
        <!-- Destination -->
        <div class="relative">
          <label class="block mb-2 font-medium text-gray-700">Destination</label>
          <div class="relative">
            <i class="material-icons absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">flight_land</i>
            <input 
              type="text" 
              v-model="destinationQuery" 
              @input="searchDestinationAirports" 
              placeholder="City or Airport" 
              class="w-full pl-10 pr-3 py-3 border rounded-lg"
            >
          </div>
          <div v-if="showDestinationDropdown && destinationAirports.length" class="dropdown-menu absolute z-10 bg-white w-full mt-1 max-h-64 overflow-y-auto">
            <div 
              v-for="airport in destinationAirports" 
              :key="airport.presentation.id" 
              @click="selectDestination(airport)"
              class="dropdown-item p-3 cursor-pointer"
            >
              <div class="font-medium">{{ airport.presentation.title }}</div>
              <div class="text-sm text-gray-500">{{ airport.presentation.subtitle }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
        <!-- Departure date -->
        <div>
          <label class="block mb-2 font-medium text-gray-700">Departure Date</label>
          <div class="relative">
            <i class="material-icons absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">event</i>
            <input 
              type="date" 
              v-model="departDate" 
              class="w-full pl-10 pr-3 py-3 border rounded-lg"
              :min="today"
            >
          </div>
        </div>
        
        <!-- Return date (only for round trips) -->
        <div v-if="tripType === 'round'">
          <label class="block mb-2 font-medium text-gray-700">Return Date</label>
          <div class="relative">
            <i class="material-icons absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">event</i>
            <input 
              type="date" 
              v-model="returnDate" 
              class="w-full pl-10 pr-3 py-3 border rounded-lg"
              :min="departDate || today"
            >
          </div>
        </div>
        
        <!-- Cabin class -->
        <div>
          <label class="block mb-2 font-medium text-gray-700">Cabin Class</label>
          <div class="relative">
            <i class="material-icons absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">airline_seat_recline_normal</i>
            <select v-model="cabinClass" class="w-full pl-10 pr-3 py-3 border rounded-lg appearance-none">
              <option value="economy">Economy</option>
              <option value="premium_economy">Premium Economy</option>
              <option value="business">Business</option>
              <option value="first">First</option>
            </select>
            <i class="material-icons absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400">arrow_drop_down</i>
          </div>
        </div>
        
        <!-- Number of passengers -->
        <div>
          <label class="block mb-2 font-medium text-gray-700">Passengers</label>
          <div class="grid grid-cols-3 gap-3">
            <div>
              <label class="text-sm text-gray-600 mb-1 block">Adult</label>
              <div class="relative">
                <i class="material-icons absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">person</i>
                <input type="number" v-model="adults" min="1" max="9" class="w-full pl-10 pr-3 py-3 border rounded-lg">
              </div>
            </div>
            <div>
              <label class="text-sm text-gray-600 mb-1 block">Child</label>
              <div class="relative">
                <i class="material-icons absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">child_care</i>
                <input type="number" v-model="children" min="0" max="9" class="w-full pl-10 pr-3 py-3 border rounded-lg">
              </div>
            </div>
            <div>
              <label class="text-sm text-gray-600 mb-1 block">Infant</label>
              <div class="relative">
                <i class="material-icons absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">baby_changing_station</i>
                <input type="number" v-model="infants" min="0" max="9" class="w-full pl-10 pr-3 py-3 border rounded-lg">
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <button 
        @click="searchFlights" 
        class="search-button w-full text-white py-4 px-6 rounded-lg font-medium text-lg flex items-center justify-center"
        :disabled="isLoading"
      >
        <i class="material-icons mr-2" v-if="!isLoading">search</i>
        <i class="material-icons animate-spin mr-2" v-if="isLoading">sync</i>
        {{ isLoading ? 'Searching...' : 'Search Flights' }}
      </button>
    </div>
    
    <!-- Search results -->
    <div v-if="flightResults && flightResults.data" class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-semibold mb-6 flex items-center">
        <i class="material-icons mr-2 text-blue-600">flight</i>
        Search Results
      </h2>
      
      <div v-if="flightResults.data.itineraries && flightResults.data.itineraries.length">
        <div v-for="flight in flightResults.data.itineraries" :key="flight.id" class="flight-card mb-5">
          <div class="bg-blue-50 p-4">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center">
              <div class="flex flex-col">
                <div class="text-xl font-semibold">
                  {{ getOriginDestinationText(flight) }}
                </div>
                <div class="text-sm text-gray-600 mt-1">
                  {{ getFlightDateInfo(flight) }}
                </div>
              </div>
              <div class="mt-3 md:mt-0">
                <div class="price-tag text-2xl">{{ flight.price.formatted }}</div>
                <div class="text-sm text-gray-500 text-right">Total Price</div>
              </div>
            </div>
          </div>
          
          <div class="p-4">
            <div v-for="leg in flight.legs" :key="leg.id" class="flight-leg first:border-t-0 first:pt-0 mt-3">
              <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-3">
                <div>
                  <div class="text-lg font-semibold">
                    {{ leg.origin.displayCode }} ??{{ leg.destination.displayCode }}
                  </div>
                  <div class="text-sm text-gray-600">
                    {{ formatDate(leg.departure) }} - {{ formatDate(leg.arrival) }}
                    <span v-if="leg.timeDeltaInDays > 0" class="text-orange-500 font-medium ml-1">
                      (+{{ leg.timeDeltaInDays }} days)
                    </span>
                  </div>
                </div>
                <div class="flex flex-col items-end mt-2 md:mt-0">
                  <div class="flight-duration">{{ formatDuration(leg.durationInMinutes) }}</div>
                  <div class="text-sm mt-1">
                    <span v-if="leg.stopCount === 0" class="text-green-600 font-medium">Direct</span>
                    <span v-else class="text-orange-500 font-medium">{{ leg.stopCount }} stop</span>
                  </div>
                </div>
              </div>
              
              <div class="flex flex-wrap gap-3 mt-3">
                <div v-for="carrier in leg.carriers.marketing" :key="carrier.id" class="flex items-center bg-gray-50 px-3 py-2 rounded-full">
                  <img :src="carrier.logoUrl" alt="airline logo" class="airline-logo mr-2">
                  <span class="text-sm font-medium">{{ carrier.name }}</span>
                </div>
              </div>
            </div>
            
            <div class="mt-4 text-right">
              <button 
                @click="viewFlightDetails(flight)" 
                class="details-button bg-blue-600 text-white py-2.5 px-5 rounded-lg hover:bg-blue-700 transition flex items-center ml-auto"
              >
                <span class="mr-1">Details</span>
                <i class="material-icons text-sm">arrow_forward</i>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center p-8 text-gray-500 bg-gray-50 rounded-lg">
        <i class="material-icons text-4xl mb-2 text-gray-400">search_off</i>
        <p class="text-lg">No search results. Try different search conditions.</p>
      </div>
    </div>
    
    <!-- Recent search history -->
    <div v-if="isAuthenticated && searchHistory && searchHistory.length > 0" class="mt-8 mb-8">
      <div class="flex items-center mb-4">
        <h2 class="text-xl font-semibold">
          <i class="material-icons mr-2 text-blue-600">history</i>
          Recent Search History
        </h2>
        <div class="ml-2 text-sm text-gray-500">
          (Only personal search history is displayed)
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div 
          v-for="(history, index) in searchHistory" 
          :key="index" 
          class="history-card p-4 cursor-pointer"
          @click="loadSearchHistory(history)"
        >
          <div class="flex flex-col">
            <div class="font-semibold text-blue-700">
              {{ history.origin }} ??{{ history.destination }}
            </div>
            <div class="text-sm text-gray-600 mt-1">
              Departure: {{ formatDate(history.departure_date) }}
            </div>
            <div v-if="history.return_date" class="text-sm text-gray-600">
              Return: {{ formatDate(history.return_date) }}
            </div>
            <div class="text-xs text-gray-500 mt-2">
              Search date: {{ formatDate(history.search_date) }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Login required message -->
    <div v-if="!isAuthenticated" class="mt-8 mb-8 bg-blue-50 p-4 rounded-lg border border-blue-200">
      <div class="flex items-center">
        <i class="material-icons mr-2 text-blue-600">info</i>
        <h3 class="text-lg font-medium text-blue-700">Want to save your search history?</h3>
      </div>
      <p class="mt-2 text-blue-600">
        Log in to save your personal search history and use it conveniently.
      </p>
      <div class="mt-3">
        <router-link to="/login" class="inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-200">
          Log in
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { searchAirports, searchFlights as apiSearchFlights, getSearchHistory } from '@/api/flight';

export default {
  name: 'FlightView',
  setup() {
    const router = useRouter();
    
    // Search Form State
    const tripType = ref('round');
    const originQuery = ref('');
    const destinationQuery = ref('');
    const departDate = ref('');
    const returnDate = ref('');
    const cabinClass = ref('economy');
    const adults = ref(1);
    const children = ref(0);
    const infants = ref(0);
    
    // Airport Autocomplete Related State
    const originAirports = ref([]);
    const destinationAirports = ref([]);
    const showOriginDropdown = ref(false);
    const showDestinationDropdown = ref(false);
    const selectedOrigin = ref(null);
    const selectedDestination = ref(null);
    
    // Search Results and Loading State
    const flightResults = ref(null);
    const isLoading = ref(false);
    const searchHistory = ref([]);
    
    // Login State
    const isAuthenticated = computed(() => {
      return !!localStorage.getItem('access_token');
    });
    
    // Calculate Today's Date
    const today = computed(() => {
      const date = new Date();
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    });
    
    // Airport Search Function
    const searchOriginAirports = async () => {
      if (originQuery.value.length < 2) {
        originAirports.value = [];
        showOriginDropdown.value = false;
        return;
      }
      
      try {
        const response = await searchAirports(originQuery.value);
        if (response && response.data && response.data.length) {
          originAirports.value = response.data;
          showOriginDropdown.value = true;
        }
      } catch (error) {
        console.error('Airport Search Error:', error);
      }
    };
    
    const searchDestinationAirports = async () => {
      if (destinationQuery.value.length < 2) {
        destinationAirports.value = [];
        showDestinationDropdown.value = false;
        return;
      }
      
      try {
        const response = await searchAirports(destinationQuery.value);
        if (response && response.data && response.data.length) {
          destinationAirports.value = response.data;
          showDestinationDropdown.value = true;
        }
      } catch (error) {
        console.error('Airport Search Error:', error);
      }
    };
    
    // Airport Selection Function
    const selectOrigin = (airport) => {
      originQuery.value = airport.presentation.suggestionTitle;
      selectedOrigin.value = airport;
      showOriginDropdown.value = false;
    };
    
    const selectDestination = (airport) => {
      destinationQuery.value = airport.presentation.suggestionTitle;
      selectedDestination.value = airport;
      showDestinationDropdown.value = false;
    };
    
    // Flight Search Function
    const searchFlights = async () => {
      if (!selectedOrigin.value || !selectedDestination.value || !departDate.value) {
        alert('Please enter departure, destination, and departure date.');
        return;
      }
      
      if (tripType.value === 'round' && !returnDate.value) {
        alert('Please enter return date.');
        return;
      }
      
      isLoading.value = true;
      
      try {
        const params = {
          trip_type: tripType.value,
          fromEntityId: selectedOrigin.value.navigation.relevantFlightParams.skyId,
          toEntityId: selectedDestination.value.navigation.relevantFlightParams.skyId,
          departDate: departDate.value,
          cabinClass: cabinClass.value,
          adults: adults.value,
          children: children.value,
          infants: infants.value
        };
        
        if (tripType.value === 'round') {
          params.returnDate = returnDate.value;
        }
        
        const response = await apiSearchFlights(params);
        flightResults.value = response;
      } catch (error) {
        console.error('Flight Search Error:', error);
        alert('Flight search error occurred. Please try again.');
      } finally {
        isLoading.value = false;
      }
    };
    
    // Flight Details Page Navigation
    const viewFlightDetails = (flight) => {
      router.push({
        name: 'FlightDetails',
        query: {
          token: flightResults.value.data.token,
          itineraryId: flight.id
        }
      });
    };
    
    // Search History Loading
    const fetchSearchHistory = async () => {
      if (!isAuthenticated.value) {
        searchHistory.value = [];
        return;
      }
      
      try {
        console.log('?뵇 Login status check:', isAuthenticated.value);
        console.log('?뵎 Token:', localStorage.getItem('access_token'));
        
        const response = await getSearchHistory();
        console.log('?뱥 Search history response:', response);
        
        if (response && response.results) {
          searchHistory.value = response.results;
        } else {
          // No results case - initialize empty array
          searchHistory.value = [];
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          console.log('?좑툘 Login required');
          searchHistory.value = [];
        } else {
          console.error('??Error loading search history:', error);
          searchHistory.value = [];
        }
      }
    };
    
    // Search History Item Selection
    const loadSearchHistory = async (history) => {
      console.log('Search History Loading Started:', history);
      
      // Set basic information
      tripType.value = history.return_date ? 'round' : 'one-way';
      departDate.value = history.departure_date;
      returnDate.value = history.return_date;
      
      // Search in progress state
      isLoading.value = true;
      
      try {
        // Extract location name for accurate airport search
        const extractLocationName = (fullName) => {
          // "Seoul (all airports) - Korea" -> "Seoul"
          // "Incheon International Airport - Korea" -> "Incheon International Airport"
          const match = fullName.match(/^([^(]+?)(?:\s*\(.*\))?\s*-/);
          return match ? match[1].trim() : fullName;
        };
        
        // Check if it's an airport code (typically 3-4 uppercase letters)
        const isAirportCode = (code) => {
          return /^[A-Z]{3,4}$/.test(code);
        };
        
        // Create temporary object for direct airport code input
        const createAirportObjectFromCode = (code, name) => {
          return {
            presentation: {
              id: code,
              title: name || code,
              subtitle: 'Directly entered airport code',
              suggestionTitle: name || code
            },
            navigation: {
              relevantFlightParams: {
                skyId: code
              }
            }
          };
        };
        
        // Origin airport search and setup
        const originIsCode = isAirportCode(history.origin);
        
        if (originIsCode) {
          console.log('Departure is an airport code:', history.origin);
          // Direct airport code input case - create temporary object
          originQuery.value = history.origin;
          selectedOrigin.value = createAirportObjectFromCode(history.origin, history.origin_name || history.origin);
          console.log('Departure airport object created:', selectedOrigin.value);
        } else {
          // Perform general search
          const originName = extractLocationName(history.origin);
          originQuery.value = originName;
          console.log('Origin airport search started:', originName);
          
          // Add small delay to ensure input is ready for search
          await new Promise(resolve => setTimeout(resolve, 300));
          
          const originResponse = await searchAirports(originName);
          console.log('Origin airport search results:', originResponse);
          
          if (originResponse && originResponse.data && originResponse.data.length > 0) {
            console.log('Origin airport selected:', originResponse.data[0]);
            
            // Execute internal logic instead of calling the selection function directly
            const originAirport = originResponse.data[0];
            originQuery.value = originAirport.presentation.suggestionTitle || history.origin;
            selectedOrigin.value = originAirport;
            showOriginDropdown.value = false;
          } else {
            console.error('No origin airport search results');
            originQuery.value = history.origin; // Restore original value
            // Create temporary object even when no search results
            selectedOrigin.value = createAirportObjectFromCode(history.origin, history.origin);
          }
        }
        
        // Add delay between searches
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Destination airport search and setup
        const destIsCode = isAirportCode(history.destination);
        
        if (destIsCode) {
          console.log('Destination is an airport code:', history.destination);
          // Direct airport code input case - create temporary object
          destinationQuery.value = history.destination;
          selectedDestination.value = createAirportObjectFromCode(history.destination, history.destination_name || history.destination);
          console.log('Destination airport object directly created:', selectedDestination.value);
        } else {
          // Perform general search
          const destName = extractLocationName(history.destination);
          destinationQuery.value = destName;
          console.log('Destination airport search started:', destName);
          
          // Add small delay to ensure input is ready for search
          await new Promise(resolve => setTimeout(resolve, 300));
          
          const destResponse = await searchAirports(destName);
          console.log('Destination airport search results:', destResponse);
          
          if (destResponse && destResponse.data && destResponse.data.length > 0) {
            console.log('Destination airport selected:', destResponse.data[0]);
            
            // Execute internal logic instead of calling the selection function directly
            const destAirport = destResponse.data[0];
            destinationQuery.value = destAirport.presentation.suggestionTitle || history.destination;
            selectedDestination.value = destAirport;
            showDestinationDropdown.value = false;
          } else {
            console.error('No destination airport search results');
            destinationQuery.value = history.destination; // Restore original value
            // Create temporary object even when no search results
            selectedDestination.value = createAirportObjectFromCode(history.destination, history.destination);
          }
        }
        
        console.log('Search settings complete', {
          departure: selectedOrigin.value,
          destination: selectedDestination.value,
          departureDate: departDate.value,
          returnDate: returnDate.value
        });
        
        // When the search settings are complete, automatically run the search
        // Only run if both airports are selected
        if (selectedOrigin.value && selectedDestination.value) {
          await new Promise(resolve => setTimeout(resolve, 500)); // Wait briefly and then run the search
          searchFlights();
        }
      } catch (error) {
        console.error('Error occurred while loading search history:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    // Formatting functions
    const formatDate = (dateStr) => {
      if (!dateStr) return '';
      
      const date = new Date(dateStr);
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return date.toLocaleDateString('en-US', options);
    };
    
    const formatDuration = (minutes) => {
      const hours = Math.floor(minutes / 60);
      const mins = minutes % 60;
      return `${hours}hours ${mins}minutes`;
    };
    
    const getOriginDestinationText = (flight) => {
      const leg = flight.legs[0];
      return `${leg.origin.city || leg.origin.displayCode} ??${leg.destination.city || leg.destination.displayCode}`;
    };
    
    const getFlightDateInfo = (flight) => {
      const departLeg = flight.legs[0];
      
      if (flight.legs.length > 1) {
        const returnLeg = flight.legs[1];
        return `${formatDate(departLeg.departure)} - ${formatDate(returnLeg.arrival)}`;
      }
      
      return `${formatDate(departLeg.departure)}`;
    };
    
    // When the page loads, load the search history
    onMounted(() => {
      fetchSearchHistory();
    });
    
    return {
      tripType,
      originQuery,
      destinationQuery,
      departDate,
      returnDate,
      cabinClass,
      adults,
      children,
      infants,
      originAirports,
      destinationAirports,
      showOriginDropdown,
      showDestinationDropdown,
      flightResults,
      isLoading,
      searchHistory,
      today,
      isAuthenticated,
      searchOriginAirports,
      searchDestinationAirports,
      selectOrigin,
      selectDestination,
      searchFlights,
      viewFlightDetails,
      loadSearchHistory,
      formatDate,
      formatDuration,
      getOriginDestinationText,
      getFlightDateInfo
    };
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}

h1 {
  background: linear-gradient(45deg, #3b82f6, #2563eb);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-top: 1rem;
}

.search-form {
  background-color: white;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
}

.search-form:hover {
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.15);
}

input[type="text"], input[type="date"], input[type="number"], select {
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  padding: 0.75rem 1rem;
  transition: all 0.2s ease;
  font-size: 1rem;
}

input[type="text"]:focus, input[type="date"]:focus, input[type="number"]:focus, select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
  outline: none;
}

.search-button {
  background: linear-gradient(45deg, #3b82f6, #2563eb);
  border-radius: 0.75rem;
  padding: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.search-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(59, 130, 246, 0.3);
}

.search-button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.flight-card {
  border-radius: 1rem;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
  overflow: hidden;
}

.flight-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: #bfdbfe;
}

.flight-leg {
  border-top: 1px solid #f3f4f6;
  padding-top: 1rem;
}

.details-button {
  background: linear-gradient(45deg, #3b82f6, #2563eb);
  border-radius: 0.75rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.details-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.dropdown-menu {
  border-radius: 0.75rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.dropdown-item {
  transition: all 0.2s ease;
  border-bottom: 1px solid #f3f4f6;
}

.dropdown-item:hover {
  background-color: #f9fafb;
}

.history-card {
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.history-card:hover {
  background-color: #f0f7ff;
  border-color: #bfdbfe;
  transform: translateY(-2px);
}

.price-tag {
  color: #2563eb;
  font-weight: 700;
}

.airline-logo {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  object-fit: contain;
  background-color: #f9fafb;
  padding: 0.25rem;
  border: 1px solid #e5e7eb;
}

.flight-duration {
  font-weight: 600;
  color: #4b5563;
}

.banner-container {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

/* Material Icons animation */
.animate-spin {
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 
