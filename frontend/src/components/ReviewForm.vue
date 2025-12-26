<template>
  <!-- Review form component for creating and editing reviews -->
  <div class="review-form-container">
    <h3 class="form-title">{{ existingReview ? 'Edit Review' : 'Write a Review' }}</h3>
    
    <!-- Rating selection section -->
    <div class="rating-section">
      <div class="rating-label">Select Rating:</div>
      
      <!-- Star rating radio buttons -->
      <div class="rating-options">
        <div 
          v-for="rating in 5" 
          :key="rating" 
          class="rating-option"
          @click="setRating(rating)"
        >
          <input 
            type="radio" 
            :id="`rating-${rating}`" 
            name="rating" 
            :value="rating" 
            :checked="review.rating === rating"
          />
          <label :for="`rating-${rating}`" class="rating-label-option">
            {{ rating }} points
            <span class="star-icon" :class="{ 'active': rating <= review.rating }">
              <i class="fas fa-star"></i>
            </span>
          </label>
        </div>
      </div>
      
      <!-- Selected rating display -->
      <div class="selected-rating" v-if="review.rating > 0">
        Selected rating: <strong>{{ review.rating }} points</strong>
      </div>
      
      <!-- Rating selection reminder -->
      <div v-else class="rating-hint">
        ⚠️ Please select a rating (1-5)
      </div>
    </div>
    
    <!-- Review content textarea section -->
    <div class="content-container">
      <label for="review-content" class="content-label">Review Content:</label>
      <textarea 
        id="review-content"
        v-model="review.content" 
        placeholder="Share your experience about this destination..." 
        rows="4"
        :disabled="isLoading"
      ></textarea>
    </div>
    
    <!-- Form action buttons -->
    <div class="form-actions">
      <button 
        @click="submitReview" 
        class="submit-button"
        :disabled="isLoading || !isValid"
      >
        {{ isLoading ? 'Processing...' : (existingReview ? 'Update' : 'Submit') }}
      </button>
      
      <button 
        v-if="existingReview" 
        @click="$emit('cancel')" 
        class="cancel-button"
        :disabled="isLoading"
      >
        Cancel
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

/**
 * Review form component for submitting and editing destination reviews
 * Allows users to rate destinations and share their experiences
 */
export default {
  name: 'ReviewForm',
  props: {
    locationId: {
      type: Number,
      required: true
    },
    existingReview: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      review: {
        rating: this.existingReview ? this.existingReview.rating : 0,
        content: this.existingReview ? this.existingReview.content : ''
      },
      isLoading: false
    };
  },
  mounted() {
    console.log('ReviewForm mounted - locationId:', this.locationId);
    console.log('ReviewForm mounted - existingReview:', this.existingReview);
    console.log('ReviewForm mounted - initial rating:', this.review.rating);
    console.log('ReviewForm mounted - initial content:', this.review.content);
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  computed: {
    /**
     * Check if the review is valid for submission
     * Requires both rating and content to be provided
     */
    isValid() {
      const valid = this.review.rating > 0 && this.review.content.trim().length > 0;
      console.log('Rating:', this.review.rating, 'Content length:', this.review.content.trim().length, 'isValid:', valid);
      return valid;
    }
  },
  methods: {
    /**
     * Set the review rating
     * @param {number} rating - Selected rating value (1-5)
     */
    setRating(rating) {
      console.log('Setting rating to:', rating);
      if (!this.isLoading) {
        this.review.rating = rating;
        console.log('Rating after setting:', this.review.rating);
      }
    },
    
    /**
     * Submit the review to the server
     * Creates a new review or updates an existing one
     */
    async submitReview() {
      console.log('submitReview called');
      console.log('Current review state:', this.review);
      
      if (!localStorage.getItem('access_token')) {
        this.toast.warning('Login is required for this feature.');
        this.$router.push('/login');
        return;
      }
      
      if (!this.isValid) {
        console.log('Validation failed');
        console.log('Rating:', this.review.rating, 'Content length:', this.review.content.trim().length);
        this.toast.warning('Please provide both rating and review content.');
        return;
      }
      
      this.isLoading = true;
      console.log('Sending review data');
      
      try {
        const reviewData = {
          location_id: this.locationId,
          rating: this.review.rating,
          content: this.review.content
        };
        
        console.log('Review data to send:', reviewData);
        
        let response;
        const token = localStorage.getItem('access_token');
        
        if (this.existingReview) {
          // Update existing review
          console.log('Updating existing review...');
          response = await axios.put(
            `http://localhost:8000/api/destinations/reviews/${this.existingReview.id}/`,
            reviewData,
            {
              headers: {
                Authorization: `Bearer ${token}`
              }
            }
          );
          this.toast.success('Review updated successfully.');
        } else {
          // Create new review
          console.log('Creating new review...');
          response = await axios.post(
            'http://localhost:8000/api/destinations/reviews/',
            reviewData,
            {
              headers: {
                Authorization: `Bearer ${token}`
              }
            }
          );
          console.log('Review submission response:', response.data);
          this.toast.success('Review submitted successfully.');
        }
        
        // Notify parent component
        this.$emit('review-submitted', response.data);
        
        // Reset form for new review creation
        if (!this.existingReview) {
          this.review.rating = 0;
          this.review.content = '';
        }
      } catch (error) {
        console.error('Error submitting review:', error);
        if (error.response) {
          console.error('Error response:', error.response.data);
        }
        this.toast.error('An error occurred while submitting your review.');
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Form container styling */
.review-form-container {
  background-color: #f8fafc;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Form title styling */
.form-title {
  font-size: 18px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 15px;
}

/* Rating section container */
.rating-section {
  margin-bottom: 20px;
}

/* Rating label styling */
.rating-label {
  font-size: 14px;
  font-weight: 500;
  color: #4a5568;
  margin-bottom: 10px;
}

/* Rating options layout */
.rating-options {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

/* Single rating option styling */
.rating-option {
  display: flex;
  align-items: center;
}

/* Radio button styling */
.rating-option input[type="radio"] {
  margin-right: 5px;
}

/* Rating option label styling */
.rating-label-option {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 14px;
  color: #4a5568;
}

/* Star icon styling */
.star-icon {
  margin-left: 5px;
  color: #cbd5e0;
  transition: color 0.2s;
}

/* Active star styling */
.star-icon.active {
  color: #f6ad55;
}

/* Selected rating display */
.selected-rating {
  margin-top: 10px;
  font-size: 14px;
  color: #4a5568;
}

/* Rating validation hint */
.rating-hint {
  font-size: 13px;
  color: #e53e3e;
  margin-top: 5px;
}

/* Content section container */
.content-container {
  margin-bottom: 15px;
}

/* Content label styling */
.content-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #4a5568;
  margin-bottom: 5px;
}

/* Textarea styling */
textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  resize: vertical;
  transition: border-color 0.2s;
}

/* Textarea focus state */
textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

/* Textarea disabled state */
textarea:disabled {
  background-color: #f7fafc;
  cursor: not-allowed;
}

/* Action buttons container */
.form-actions {
  display: flex;
  gap: 10px;
}

/* Button base styling */
.submit-button,
.cancel-button {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

/* Submit button styling */
.submit-button {
  background-color: #4299e1;
  color: white;
  border: none;
}

/* Submit button hover state */
.submit-button:hover:not(:disabled) {
  background-color: #3182ce;
}

/* Submit button disabled state */
.submit-button:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

/* Cancel button styling */
.cancel-button {
  background-color: white;
  color: #4a5568;
  border: 1px solid #e2e8f0;
}

/* Cancel button hover state */
.cancel-button:hover:not(:disabled) {
  background-color: #f7fafc;
  border-color: #cbd5e0;
}

/* Cancel button disabled state */
.cancel-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style> 