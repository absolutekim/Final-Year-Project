<template>
  <!-- User profile page container -->
  <v-container class="mypage">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <!-- Profile information card -->
        <v-card class="mx-auto" elevation="3">
          <v-card-title class="text-h4 font-weight-bold text-center py-6 primary white--text">
            My Page
          </v-card-title>

          <v-card-text v-if="profile" class="pa-6">
            <v-row>
              <!-- Profile image section -->
              <v-col cols="12" sm="4" class="text-center">
                <v-avatar size="200" class="profile-avatar">
                  <v-img
                    :src="getProfileImageUrl(profile.profile_image)"
                    alt="Profile Image"
                    @error="handleImageError"
                  >
                    <template v-slot:placeholder>
                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <v-progress-circular indeterminate color="primary"></v-progress-circular>
                      </v-row>
                    </template>
                  </v-img>
                </v-avatar>
              </v-col>

              <!-- Profile information section -->
              <v-col cols="12" sm="8">
                <div v-if="!isEditing">
                  <h2 class="text-h5 font-weight-bold mb-4">
                    {{ profile.nickname || profile.user.username }}
                  </h2>
                  <v-card outlined class="pa-4 mb-4 bio-card">
                    <p class="text-body-1">{{ profile.bio || 'No introduction available.' }}</p>
                  </v-card>
                  
                  <!-- User Info Cards -->
                  <v-row class="mb-4">
                    <!-- Age Group Card -->
                    <v-col cols="12" sm="6">
                      <v-card outlined class="info-card" :class="{'info-card-empty': !profile.user.age_group}">
                        <div class="d-flex align-center">
                          <v-avatar color="primary" size="36" class="mr-3">
                            <v-icon color="white">mdi-calendar-account</v-icon>
                          </v-avatar>
                          <div>
                            <div class="caption grey--text text--darken-1">Age Group</div>
                            <div class="subtitle-1 font-weight-medium">
                              {{ getAgeGroupText(profile.user.age_group) || 'Not specified' }}
                            </div>
                          </div>
                        </div>
                      </v-card>
                    </v-col>
                    
                    <!-- Gender Card -->
                    <v-col cols="12" sm="6">
                      <v-card outlined class="info-card" :class="{'info-card-empty': !profile.user.gender}">
                        <div class="d-flex align-center">
                          <v-avatar :color="profile.user.gender === 'M' ? 'blue' : profile.user.gender === 'F' ? 'pink' : 'grey'" size="36" class="mr-3">
                            <v-icon color="white">{{ profile.user.gender === 'M' ? 'mdi-gender-male' : profile.user.gender === 'F' ? 'mdi-gender-female' : 'mdi-gender-non-binary' }}</v-icon>
                          </v-avatar>
                          <div>
                            <div class="caption grey--text text--darken-1">Gender</div>
                            <div class="subtitle-1 font-weight-medium">
                              {{ getGenderText(profile.user.gender) || 'Not specified' }}
                            </div>
                          </div>
                        </div>
                      </v-card>
                    </v-col>
                  </v-row>
                  
                  <v-btn
                    color="primary"
                    @click="startEditing"
                    prepend-icon="mdi-account-edit"
                    class="mr-2"
                  >
                    Modify Profile
                  </v-btn>
                  <v-btn
                    color="error"
                    @click="showDeleteAccountDialog"
                    prepend-icon="mdi-account-remove"
                  >
                    Delete Account
                  </v-btn>
                </div>

                <!-- Profile edit form -->
                <v-form v-else @submit.prevent="updateProfile">
                  <v-text-field
                    v-model="editForm.nickname"
                    label="Nickname"
                    outlined
                    dense
                    class="mb-4"
                  />
                  
                  <v-textarea
                    v-model="editForm.bio"
                    label="Introduction"
                    outlined
                    auto-grow
                    rows="4"
                    class="mb-4"
                  />

                  <!-- User Info Edit Section -->
                  <v-card outlined class="mb-4 pa-4">
                    <v-card-title class="text-subtitle-1 pa-0 pb-2">Personal Information</v-card-title>
                    
                    <!-- Age Group Selection -->
                    <v-select
                      v-model="editForm.age_group"
                      label="Age Group"
                      outlined
                      dense
                      :items="ageGroupOptions"
                      item-title="text"
                      item-value="value"
                      prepend-icon="mdi-calendar-account"
                      class="mb-4"
                      return-object
                    >
                    </v-select>

                    <!-- Gender Selection -->
                    <v-radio-group
                      v-model="editForm.gender"
                      row
                      class="mt-0"
                    >
                      <template v-slot:label>
                        <div class="d-flex align-center">
                          <v-icon class="mr-2">mdi-gender-male-female</v-icon>
                          <span>Gender</span>
                        </div>
                      </template>
                      <v-radio
                        label="Male"
                        value="M"
                        color="blue"
                      >
                        <template v-slot:label>
                          <div class="d-flex align-center">
                            <v-icon color="blue" class="mr-1">mdi-gender-male</v-icon>
                            <span>Male</span>
                          </div>
                        </template>
                      </v-radio>
                      <v-radio
                        label="Female"
                        value="F"
                        color="pink"
                      >
                        <template v-slot:label>
                          <div class="d-flex align-center">
                            <v-icon color="pink" class="mr-1">mdi-gender-female</v-icon>
                            <span>Female</span>
                          </div>
                        </template>
                      </v-radio>
                    </v-radio-group>
                  </v-card>

                  <v-file-input
                    v-model="editForm.profile_image"
                    label="Profile Image"
                    prepend-icon="mdi-camera"
                    outlined
                    dense
                    accept="image/*"
                    class="mb-4"
                  />

                  <v-btn
                    color="primary"
                    type="submit"
                    class="mr-4"
                    prepend-icon="mdi-content-save"
                  >
                    Save
                  </v-btn>
                  <v-btn
                    color="grey"
                    @click="cancelEditing"
                    prepend-icon="mdi-close"
                  >
                    Cancel
                  </v-btn>
                </v-form>
              </v-col>
            </v-row>
          </v-card-text>

          <!-- Loading state indicator -->
          <v-card-text v-else class="text-center pa-6">
            <v-progress-circular
              indeterminate
              color="primary"
              size="64"
            />
          </v-card-text>
        </v-card>

        <!-- Likes and reviews tabs -->
        <v-card class="mx-auto mt-6" elevation="3">
          <v-tabs v-model="activeTab" background-color="primary" dark>
            <v-tab value="likes">
              <v-icon left>mdi-heart</v-icon>
              Liked Destinations
            </v-tab>
            <v-tab value="reviews">
              <v-icon left>mdi-comment</v-icon>
              Your Reviews
            </v-tab>
          </v-tabs>

          <v-card-text class="pa-0">
            <v-window v-model="activeTab">
              <!-- Liked destinations tab content -->
              <v-window-item value="likes">
                <div class="pa-4">
                  <user-likes />
                </div>
              </v-window-item>

              <!-- User reviews tab content -->
              <v-window-item value="reviews">
                <div class="pa-4">
                  <user-reviews />
                </div>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>

        <!-- Account deletion confirmation dialog -->
        <v-dialog v-model="deleteAccountDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 error white--text">
              Delete Account
            </v-card-title>
            <v-card-text class="pt-4">
              <p class="mb-4">If you delete your account, all data will be permanently deleted and cannot be recovered. Are you sure you want to delete it?</p>
              <v-form @submit.prevent="deleteAccount">
                <v-text-field
                  v-model="deleteAccountPassword"
                  label="Confirm Password"
                  type="password"
                  outlined
                  dense
                  :error-messages="deleteAccountError"
                  required
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="grey" text @click="deleteAccountDialog = false">
                Cancel
              </v-btn>
              <v-btn color="error" @click="deleteAccount" :loading="isDeleting">
                Delete Account
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import UserLikes from '@/components/UserLikes.vue'
import UserReviews from '@/components/UserReviews.vue'

/**
 * My Page Component
 * User profile management interface with profile editing capabilities
 * Features:
 * - Profile information display and editing
 * - Profile image upload
 * - Account deletion
 * - Tabs for liked destinations and user reviews
 */
export default {
  name: 'MyPage',
  components: {
    UserLikes,
    UserReviews
  },
  data() {
    return {
      profile: null, // User profile data
      isEditing: false, // Profile editing mode
      activeTab: 'likes', // Active tab selection
      editForm: {
        nickname: '', // Nickname editing field
        bio: '', // Bio editing field
        age_group: '', // Age group field
        gender: '', // Gender field
        profile_image: null // Profile image upload field
      },
      // Age Group Selection Options - using simple strings as values
      ageGroupOptions: [
        { text: "Under 18", value: "under18" },
        { text: "18-24", value: "18to24" },
        { text: "25-34", value: "25to34" },
        { text: "35-44", value: "35to44" },
        { text: "45-54", value: "45to54" },
        { text: "55-64", value: "55to64" },
        { text: "65 and Above", value: "65plus" }
      ],
      deleteAccountDialog: false, // Account deletion dialog visibility
      deleteAccountPassword: '', // Password confirmation for account deletion
      deleteAccountError: '', // Error message for account deletion
      isDeleting: false // Account deletion loading state
    }
  },
  methods: {
    /**
     * Get readable text for age group value
     */
    getAgeGroupText(ageGroupValue) {
      if (!ageGroupValue) return null;
      const found = this.ageGroupOptions.find(opt => opt.value === ageGroupValue);
      return found ? found.text : ageGroupValue;
    },
    
    /**
     * Get readable text for gender value
     */
    getGenderText(genderValue) {
      if (!genderValue) return null;
      return genderValue === 'M' ? 'Male' : genderValue === 'F' ? 'Female' : genderValue;
    },
    
    /**
     * Get proper URL for profile image
     * @param {String} imagePath - The image path from the API
     */
    getProfileImageUrl(imagePath) {
      if (!imagePath) {
        const defaultAvatar = `https://ui-avatars.com/api/?name=${this.profile.user.username}&background=random&size=200`;
        console.log('Using default avatar:', defaultAvatar);
        return defaultAvatar;
      }
      
      // Check if the image path starts with http or https
      if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
        console.log('Using absolute image URL:', imagePath);
        return imagePath;
      }
      
      // Handle case where image is stored in the old directory structure
      // This is a temporary fix - eventually all images should be in the media directory
      const baseUrl = process.env.VUE_APP_API_URL || 'http://localhost:8000';
      let normalizedPath = '';
      
      // Check if the path already includes /media/
      if (imagePath.includes('/media/')) {
        normalizedPath = imagePath;
      } else if (imagePath.startsWith('/')) {
        // Prepend /media if needed
        normalizedPath = `/media${imagePath}`;
      } else {
        // Handle paths like profile_images/image.jpg
        normalizedPath = `/media/${imagePath}`;
      }
      
      const fullUrl = `${baseUrl}${normalizedPath}`;
      console.log('Constructed image URL:', fullUrl);
      return fullUrl;
    },
    
    /**
     * Fetch user profile data from API
     * Loads the current user's profile information
     */
    async fetchProfile() {
      try {
        const response = await axios.get('/api/mypage/profile/')
        this.profile = response.data
        console.log('Fetched profile data:', JSON.stringify(this.profile))
        console.log('Profile image path:', this.profile.profile_image)
      } catch (error) {
        console.error('Failed to load profile:', error)
      }
    },
    
    /**
     * Begin profile editing mode
     * Populates the edit form with current profile data
     */
    startEditing() {
      // Find the age group option that matches the user's value
      const ageOption = this.ageGroupOptions.find(option => 
        option.value === this.profile.user.age_group
      ) || '';
      
      this.editForm = {
        nickname: this.profile.nickname,
        bio: this.profile.bio,
        age_group: ageOption,
        gender: this.profile.user.gender || ''
      }
      
      this.isEditing = true
    },
    
    /**
     * Cancel profile editing mode
     * Reverts to display mode without saving changes
     */
    cancelEditing() {
      this.isEditing = false
    },
    
    /**
     * Handle profile image file selection
     * @param {Event} event - Input change event with selected file
     */
    handleImageChange(event) {
      this.editForm.profile_image = event.target.files[0]
    },
    
    /**
     * Update profile information
     * Saves changes to nickname, bio, and profile image
     */
    async updateProfile() {
      try {
        // Extract age group value from the object
        const ageGroupValue = this.editForm.age_group && this.editForm.age_group.value ? 
          this.editForm.age_group.value : '';
        
        const formData = new FormData()
        formData.append('nickname', this.editForm.nickname)
        formData.append('bio', this.editForm.bio)
        formData.append('age_group', ageGroupValue)
        formData.append('gender', this.editForm.gender)
        
        if (this.editForm.profile_image) {
          formData.append('profile_image', this.editForm.profile_image)
        }

        await axios.put('/api/mypage/profile/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        await this.fetchProfile()
        this.isEditing = false
      } catch (error) {
        console.error('Failed to update profile:', error)
      }
    },
    
    /**
     * Show account deletion confirmation dialog
     * Resets error messages and password field
     */
    showDeleteAccountDialog() {
      this.deleteAccountDialog = true
      this.deleteAccountPassword = ''
      this.deleteAccountError = ''
    },
    
    /**
     * Delete user account
     * Requires password confirmation for security
     */
    async deleteAccount() {
      if (!this.deleteAccountPassword) {
        this.deleteAccountError = 'Please enter your password.'
        return
      }
      
      this.isDeleting = true
      
      try {
        await axios.delete('/api/accounts/delete-account/', {
          data: {
            password: this.deleteAccountPassword
          }
        })
        
        // Clear authentication data
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        
        // Remove auth header
        delete axios.defaults.headers.common['Authorization']
        
        // Trigger auth state change event
        document.dispatchEvent(new Event('auth-changed'))
        
        // Show confirmation message
        alert('Your account has been successfully deleted.')
        
        // Reload page and redirect to home
        window.location.href = '/'
      } catch (error) {
        console.error('Failed to delete account:', error)
        
        if (error.response && error.response.data && error.response.data.error) {
          this.deleteAccountError = error.response.data.error
        } else {
          this.deleteAccountError = 'An error occurred while deleting your account.'
        }
      } finally {
        this.isDeleting = false
      }
    },
    
    /**
     * Handle image loading error
     */
    handleImageError() {
      console.error('Failed to load profile image:', this.profile.profile_image);
      // If image fails to load, try a fallback
      if (this.profile.profile_image) {
        // Mark the current path as invalid
        console.log('Trying with fallback image path');
        // We could implement additional fallback logic here if needed
      }
    }
  },
  created() {
    this.fetchProfile()
  }
}
</script>

<style scoped>
/* Main container styling */
.mypage {
  padding-top: 40px;
  padding-bottom: 40px;
}

/* Profile avatar styling with border and shadow */
.profile-avatar {
  border: 4px solid #1976d2;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Bio card background styling */
.bio-card {
  background-color: #f5f5f5;
  min-height: 100px;
}

/* User info cards styling */
.info-card {
  padding: 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
}

.info-card:hover {
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.info-card-empty {
  background-color: #f5f5f5;
  border: 1px dashed #bdbdbd;
}

/* Card styling with rounded corners */
.v-card {
  border-radius: 16px;
}

/* Card title styling */
.v-card-title {
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
}

/* Responsive design for mobile devices */
@media (max-width: 600px) {
  .profile-avatar {
    margin-bottom: 20px;
  }
  
  .v-card-title {
    font-size: 1.5rem !important;
  }
}
</style> 