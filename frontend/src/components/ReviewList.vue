<template>
  <!-- Review list component to display reviews for a location -->
  <div class="review-list-container">
    <h3 class="section-title">Reviews ({{ reviews.length }})</h3>
    
    <!-- Loading state -->
    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading reviews...</p>
    </div>
    
    <!-- Empty state when no reviews exist -->
    <div v-else-if="reviews.length === 0" class="empty-state">
      <p>No reviews yet. Be the first to write a review!</p>
    </div>
    
    <!-- Reviews list -->
    <div v-else class="reviews">
      <div v-for="review in reviews" :key="review.id" class="review-card">
        <!-- Review header with user info and actions -->
        <div class="review-header">
          <div class="user-info">
            <span class="username">{{ review.user.username }}</span>
            <div class="rating">
              <span v-for="star in 5" :key="star" class="star" :class="{ 'filled': star <= review.rating }">
                <i class="fas fa-star"></i>
              </span>
            </div>
          </div>
          <div class="review-meta">
            <span class="date">{{ formatDate(review.created_at) }}</span>
            <div v-if="isCurrentUserReview(review)" class="review-actions">
              <button @click="editReview(review)" class="action-button edit">
                <i class="fas fa-edit"></i>
              </button>
              <button @click="deleteReview(review)" class="action-button delete">
                <i class="fas fa-trash"></i>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Review content -->
        <div class="review-content">
          <p>{{ review.content }}</p>
        </div>
        
        <!-- Sentiment analysis results -->
        <div v-if="review.sentiment" class="review-sentiment" :class="getSentimentClass(review.sentiment)">
          <span class="sentiment-label">Sentiment:</span>
          <span class="sentiment-value">{{ getSentimentText(review.sentiment) }}</span>
        </div>
        
        <!-- Keywords extracted from review -->
        <div v-if="review.keywords && review.keywords.length > 0" class="review-keywords">
          <span v-for="(keyword, index) in review.keywords" :key="index" class="keyword-tag">
            {{ keyword }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- Load more button -->
    <div v-if="hasMoreReviews" class="load-more">
      <button @click="loadMoreReviews" :disabled="isLoadingMore" class="load-more-button">
        {{ isLoadingMore ? 'Loading...' : 'Load More' }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

/**
 * Component for displaying a list of reviews for a location
 * Includes pagination and review management actions
 */
export default {
  name: 'ReviewList',
  props: {
    locationId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      reviews: [],
      isLoading: true,
      isLoadingMore: false,
      page: 1,
      hasMoreReviews: false
    };
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  computed: {
    currentUserId() {
      // Get user ID from local storage - this is a simplified implementation
      // In a real app, would retrieve user information from authentication state
      return null;
    }
  },
  mounted() {
    this.fetchReviews();
  },
  methods: {
    /**
     * Fetch reviews for the specified location
     * Retrieves the initial batch of reviews from the API
     */
    async fetchReviews() {
      this.isLoading = true;
      
      try {
        const response = await axios.get(`http://localhost:8000/api/destinations/${this.locationId}/reviews/`);
        this.reviews = response.data.results;
        this.hasMoreReviews = this.reviews.length < response.data.count;
      } catch (error) {
        console.error('Error loading review list:', error);
        this.toast.error('An error occurred while loading reviews.');
      } finally {
        this.isLoading = false;
      }
    },
    
    /**
     * Load more reviews when paginating
     * Fetches the next page of reviews and appends them to the list
     */
    async loadMoreReviews() {
      if (this.isLoadingMore) return;
      
      this.isLoadingMore = true;
      this.page += 1;
      
      try {
        const response = await axios.get(`http://localhost:8000/api/destinations/${this.locationId}/reviews/`, {
          params: { page: this.page }
        });
        
        this.reviews = [...this.reviews, ...response.data.results];
        this.hasMoreReviews = this.reviews.length < response.data.count;
      } catch (error) {
        console.error('Error loading additional reviews:', error);
        this.toast.error('An error occurred while loading more reviews.');
      } finally {
        this.isLoadingMore = false;
      }
    },
    
    /**
     * Format date in local format
     * @param {string} dateString - ISO date string from API
     * @returns {string} Formatted date string
     */
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    
    /**
     * Check if the review belongs to the current user
     * @param {Object} review - Review object
     * @returns {boolean} True if the review belongs to the current user
     */
    isCurrentUserReview(review) {
      return this.currentUserId && review.user.id === this.currentUserId;
    },
    
    /**
     * Trigger edit mode for a review
     * Emits an event to parent component to handle editing
     * @param {Object} review - Review object to edit
     */
    editReview(review) {
      this.$emit('edit-review', review);
    },
    
    /**
     * Delete a review
     * Removes a review after confirmation
     * @param {Object} review - Review object to delete
     */
    async deleteReview(review) {
      if (!confirm('Are you sure you want to delete this review?')) {
        return;
      }
      
      try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`http://localhost:8000/api/destinations/reviews/${review.id}/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        
        // Remove deleted review from the list
        this.reviews = this.reviews.filter(r => r.id !== review.id);
        this.toast.success('Review deleted successfully.');
      } catch (error) {
        console.error('Error deleting review:', error);
        this.toast.error('An error occurred while deleting the review.');
      }
    },
    
    /**
     * Get CSS class for sentiment display
     * @param {string} sentiment - Sentiment value (POSITIVE, NEGATIVE, NEUTRAL)
     * @returns {string} CSS class name
     */
    getSentimentClass(sentiment) {
      switch (sentiment) {
        case 'POSITIVE':
          return 'positive';
        case 'NEGATIVE':
          return 'negative';
        default:
          return 'neutral';
      }
    },
    
    /**
     * Get display text for sentiment value
     * @param {string} sentiment - Sentiment value (POSITIVE, NEGATIVE, NEUTRAL)
     * @returns {string} Display text
     */
    getSentimentText(sentiment) {
      switch (sentiment) {
        case 'POSITIVE':
          return 'Positive';
        case 'NEGATIVE':
          return 'Negative';
        default:
          return 'Neutral';
      }
    }
  }
};
</script>

<style scoped>
/* Container for the review list */
.review-list-container {
  margin-top: 30px;
}

/* Section title styling */
.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 20px;
}

/* Loading spinner container */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 0;
}

/* Spinner animation */
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #4299e1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Empty state when no reviews exist */
.empty-state {
  text-align: center;
  padding: 30px;
  background-color: #f8fafc;
  border-radius: 8px;
  color: #718096;
}

/* Reviews list container */
.reviews {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Individual review card */
.review-card {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Review header with user info and actions */
.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

/* User information section */
.user-info {
  display: flex;
  flex-direction: column;
}

/* Username display */
.username {
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 5px;
}

/* Star rating display */
.rating {
  display: flex;
}

.star {
  color: #cbd5e0;
  margin-right: 2px;
}

.star.filled {
  color: #f6ad55;
}

/* Review metadata section */
.review-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

/* Date display */
.date {
  font-size: 12px;
  color: #718096;
  margin-bottom: 5px;
}

/* Review actions container */
.review-actions {
  display: flex;
  gap: 5px;
}

/* Action button base styling */
.action-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  padding: 2px 5px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

/* Edit button styling */
.action-button.edit {
  color: #4299e1;
}

.action-button.edit:hover {
  background-color: #ebf8ff;
}

/* Delete button styling */
.action-button.delete {
  color: #e53e3e;
}

.action-button.delete:hover {
  background-color: #fff5f5;
}

/* Review content styling */
.review-content {
  font-size: 14px;
  line-height: 1.6;
  color: #4a5568;
  margin-bottom: 15px;
}

/* Sentiment analysis badge */
.review-sentiment {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 10px;
}

/* Sentiment types */
.review-sentiment.positive {
  background-color: #c6f6d5;
  color: #2f855a;
}

.review-sentiment.negative {
  background-color: #fed7d7;
  color: #c53030;
}

.review-sentiment.neutral {
  background-color: #e2e8f0;
  color: #4a5568;
}

/* Sentiment label styling */
.sentiment-label {
  font-weight: 500;
  margin-right: 5px;
}

/* Keywords tags container */
.review-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 10px;
}

/* Individual keyword tag */
.keyword-tag {
  background-color: #e2e8f0;
  color: #4a5568;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

/* Load more container */
.load-more {
  text-align: center;
  margin-top: 20px;
}

/* Load more button */
.load-more-button {
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 8px 16px;
  font-size: 14px;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.2s;
}

/* Load more button hover state */
.load-more-button:hover:not(:disabled) {
  background-color: #f7fafc;
  border-color: #cbd5e0;
}

/* Load more button disabled state */
.load-more-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style> 