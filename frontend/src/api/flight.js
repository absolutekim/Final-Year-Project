import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/flights/";

// Flight search function
export async function searchFlights(params) {
  try {
    // Backend API call
    const response = await axios.get(`${API_BASE_URL}search/`, {
      params: params
    });
    
    console.log('Original SkyScanner API response:', response.data);
    
    // Process normal response
    if (response.data && response.data.status === true) {
      const flightData = response.data.data;
      
      // Check response structure
      if (flightData && flightData.itineraries && Array.isArray(flightData.itineraries)) {
        // Extract session ID from SkyScanner response
        const sessionId = extractSessionId(flightData);
        console.log('Extracted session ID from SkyScanner response:', sessionId);
        
        // itineraries format response (one-way or round-trip search)
        return {
          data: {
            responseType: "itineraries",
            itineraries: flightData.itineraries,
            // Include all possible session ID fields
            token: sessionId || flightData.token || flightData.flightsSessionId || "",
            // Also include the raw data for debugging
            rawData: flightData
          }
        };
      } 
      // countryDestination format response (destination search results - everywhere search)
      else if (flightData && flightData.countryDestination) {
        // Return countryDestination data as is (no conversion)
        return {
          data: {
            responseType: "countryDestination",
            countryDestination: flightData.countryDestination,
            token: flightData.countryDestination.context?.sessionId || "",
            // Include raw data for debugging
            rawData: flightData
          }
        };
      } else {
        return { 
          data: {
            responseType: "unknown",
            rawData: flightData
          }
        };
      }
    } else {
      return { 
        data: { 
          responseType: "error",
          error: response.data.message || "Flight search failed" 
        } 
      };
    }
  } catch (error) {
    return { 
      data: { 
        responseType: "error",
        error: error.response?.data?.message || error.message || "Flight search error occurred" 
      } 
    };
  }
}

// Helper function to extract session ID from SkyScanner response
function extractSessionId(data) {
  // Try all possible locations for session ID
  return data.context?.sessionId || 
         data.sessionId || 
         data.session?.token || 
         data.flightsSessionId || 
         // Look for sessionId in itineraries if available
         (data.itineraries && data.itineraries[0]?.context?.sessionId) ||
         "";
}

// Airport autocomplete search function
export async function searchAirports(query) {
  try {
    if (!query || query.trim() === '') {
      return [];
    }
    
    const response = await axios.get(`${API_BASE_URL}get-airports/`, {
      params: { query }
    });

    // Return response data as is
    return response.data || []; 
  } catch (error) {
    return [];
  }
}

// Flight details function
export async function getFlightDetails(token, itineraryId, options = {}) {
  try {
    // Check required parameters
    if (!token || !itineraryId) {
      return {
        status: false,
        message: "Required parameters are missing.",
        data: null
      };
    }
    
    // API call parameters
    const params = {
      token: token,
      itineraryId: itineraryId,
      // Optional parameters
      market: options.market || 'US',
      locale: options.locale || 'en-US',
      currency: options.currency || 'USD',
      // cookie parameter (captcha error prevention, only if provided)
      ...(options.cookie ? { cookie: options.cookie } : {})
    };
    
    // API call
    const response = await axios.get(`${API_BASE_URL}get-flight-details/`, { params });
    
    // Check response data
    if (response.data && response.data.status === true && response.data.data) {
      // Return response as is (original structure)
      return response.data;
    } else {
      return {
        status: false,
        message: response.data.message || "Failed to load flight details",
        data: null
      };
    }
  } catch (error) {
    // Generate detailed error message
    let errorMessage = "Failed to load flight details";
    if (error.response) {
      errorMessage = error.response.data?.message || 
                     `Server error (${error.response.status}): ${error.response.statusText}`;
    } else if (error.request) {
      errorMessage = "Failed to connect to server. Please check your network connection.";
    } else {
      errorMessage = error.message || errorMessage;
    }
    
    return {
      status: false,
      message: errorMessage,
      data: null
    };
  }
}

// Search history retrieval function (requires login)
export async function getSearchHistory() {
  try {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
      return { error: "Login required" };
    }
    
    const response = await axios.get(`${API_BASE_URL}get-search-history/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    return response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      return { error: "Login required" };
    }
    return { results: [] };
  }
}

// Get complete search results function
export async function getCompleteResults(sessionId, options = {}) {
  try {
    if (!sessionId || sessionId.trim() === '') {
      console.error('getCompleteResults called with empty sessionId');
      return { 
        data: { 
          responseType: "error",
          error: "Session ID is empty or invalid" 
        } 
      };
    }
    
    console.log(`Calling API with Sky-Scanner session ID: "${sessionId}"`);
    
    // Request parameter configuration
    const params = {
      sessionId: sessionId,
      ...options
    };
    
    const apiUrl = `${API_BASE_URL}get-complete-results/`;
    console.log(`Making API call to: ${apiUrl} with params:`, params);
    
    // Backend API call
    const response = await axios.get(apiUrl, {
      params: params
    });
    
    console.log('Backend raw response status:', response.status);
    console.log('Backend response data:', response.data);
    
    // Process normal response
    if (response.data && response.data.status === true) {
      const responseData = response.data.data;
      console.log('Data extracted from response:', responseData);
      
      // Check response structure
      if (responseData && responseData.data && responseData.data.itineraries && Array.isArray(responseData.data.itineraries)) {
        // Handle nested data structure (due to backend changes)
        console.log(`Found ${responseData.data.itineraries.length} itineraries in nested data structure`);
        return {
          data: {
            responseType: "itineraries",
            itineraries: responseData.data.itineraries,
            token: sessionId
          }
        };
      } 
      // Common itineraries array structure
      else if (responseData && responseData.itineraries && Array.isArray(responseData.itineraries)) {
        console.log(`Found ${responseData.itineraries.length} itineraries in response`);
        return {
          data: {
            responseType: "itineraries",
            itineraries: responseData.itineraries,
            token: responseData.context?.sessionId || responseData.flightsSessionId || sessionId
          }
        };
      } 
      // content.results structure
      else if (responseData && responseData.content && responseData.content.results) {
        // Handle alternative response format
        console.log(`Found alternative format with ${responseData.content.results.length} results`);
        return {
          data: {
            responseType: "itineraries",
            itineraries: responseData.content.results,
            token: responseData.content.context?.sessionId || sessionId
          }
        };
      } 
      // rawData structure
      else if (responseData && responseData.rawData && responseData.rawData.itineraries && Array.isArray(responseData.rawData.itineraries)) {
        console.log(`Found ${responseData.rawData.itineraries.length} itineraries in rawData property`);
        return {
          data: {
            responseType: "itineraries",
            itineraries: responseData.rawData.itineraries,
            token: sessionId
          }
        };
      }
      else {
        console.warn('Unknown response data structure, trying to extract itineraries', responseData);
        // Find itineraries in the response
        let extractedItineraries = [];
        
        if (responseData && typeof responseData === 'object') {
          // Check all properties of the object for itineraries array
          for (const key in responseData) {
            if (key === 'itineraries' && Array.isArray(responseData[key])) {
              extractedItineraries = responseData[key];
              console.log(`Found itineraries array in root level with ${extractedItineraries.length} items`);
              break;
            } else if (responseData[key] && typeof responseData[key] === 'object') {
              if (responseData[key].itineraries && Array.isArray(responseData[key].itineraries)) {
                extractedItineraries = responseData[key].itineraries;
                console.log(`Found itineraries array in ${key} property with ${extractedItineraries.length} items`);
                break;
              }
            }
          }
        }
        
        if (extractedItineraries.length > 0) {
          return {
            data: {
              responseType: "itineraries",
              itineraries: extractedItineraries,
              token: sessionId
            }
          };
        }
        
        return { 
          data: {
            responseType: "unknown",
            rawData: responseData,
            message: "Could not extract itineraries from response"
          }
        };
      }
    } else {
      return { 
        data: { 
          responseType: "error",
          error: response.data.message || "Failed to get complete results" 
        } 
      };
    }
  } catch (error) {
    console.error("Error in getCompleteResults:", error);
    return { 
      data: { 
        responseType: "error",
        error: error.response?.data?.message || error.message || "Error while getting complete search results" 
      } 
    };
  }
}

