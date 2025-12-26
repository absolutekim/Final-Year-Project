<template>
  <!-- Registration page container with gradient background -->
  <div class="register-container">
    <!-- Registration form card box -->
    <div class="register-box">
      <h2>Create Account</h2>
      <!-- User registration form -->
      <form @submit.prevent="register" class="register-form">
        <div class="form-group">
          <label>Username</label>
          <input type="text" v-model="form.username" required placeholder="Enter your username" />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input type="email" v-model="form.email" required placeholder="Enter your email" />
        </div>

        <div class="form-group">
          <label>Nickname</label>
          <input type="text" v-model="form.nickname" required placeholder="Enter your nickname" />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="form.password" required placeholder="Enter your password" />
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input type="password" v-model="form.password2" required placeholder="Confirm your password" />
        </div>

        <div class="form-group gender-group">
          <label>Gender</label>
          <div class="radio-group">
            <label class="radio-label">
              <input type="radio" v-model="form.gender" value="M" required />
              <span>Male</span>
            </label>
            <label class="radio-label">
              <input type="radio" v-model="form.gender" value="F" required />
              <span>Female</span>
            </label>
          </div>
        </div>
        
        <!-- Age Group Selection -->
        <div class="form-group">
          <label>Age Group</label>
          <select v-model="form.age_group" class="form-select" required>
            <option value="" disabled selected>Select your age group</option>
            <option value="under18">Under 18</option>
            <option value="18to24">18-24</option>
            <option value="25to34">25-34</option>
            <option value="35to44">35-44</option>
            <option value="45to54">45-54</option>
            <option value="55to64">55-64</option>
            <option value="65plus">65 and Above</option>
          </select>
        </div>

        <!-- Tag selection component -->
        <TagChoose v-model="form.selected_tags" />
        
        <!-- Debug information panel (toggleable) -->
        <div class="debug-info" v-if="showDebug">
          <p>Selected tags count: {{ form.selected_tags.length }}</p>
          <p>Selected tags: {{ form.selected_tags.join(', ') }}</p>
          <p>Form validity: {{ isFormValid ? 'Valid' : 'Invalid' }}</p>
          <p>Username: {{ !!form.username }}</p>
          <p>Email: {{ !!form.email }}</p>
          <p>Nickname: {{ !!form.nickname }}</p>
          <p>Password: {{ !!form.password }}</p>
          <p>Password2: {{ !!form.password2 }}</p>
          <p>Gender: {{ !!form.gender }}</p>
          <p>Age Group: {{ !!form.age_group }}</p>
          <p>Tags Valid: {{ form.selected_tags.length >= 3 && form.selected_tags.length <= 7 }}</p>
        </div>

        <!-- Form submission button -->
        <button type="submit" class="submit-btn" :disabled="!isFormValid">Create Account</button>
        <!-- Debug toggle button -->
        <button type="button" class="debug-btn" @click="toggleDebug">{{ showDebug ? 'Hide' : 'Show' }} Debug Info</button>
      </form>
      <!-- Success/Error message display -->
      <p v-if="message" :class="['message', message.includes('failed') ? 'error' : 'success']">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import TagChoose from '@/components/TagChoose.vue';

/**
 * Registration View Component
 * Allows users to create a new account with detailed profile information
 * Features:
 * - User details collection (username, email, password, etc.)
 * - Gender selection
 * - Interest tag selection with min/max validation
 * - Form validation with real-time feedback
 * - Debug mode for development
 */
export default {
  components: {
    TagChoose // Tag selection component
  },
  data() {
    return {
      form: {
        username: '', // Username input
        email: '', // Email input
        nickname: '', // Display name input
        password: '', // Password input
        password2: '', // Password confirmation input
        gender: '', // Gender selection (M/F)
        age_group: '', // Age group selection
        selected_tags: [] // Array of selected interest tags
      },
      message: '', // Success/Error message
      showDebug: false // Debug information panel toggle
    };
  },
  mounted() {
    // Ensure tag array is properly initialized
    if (!Array.isArray(this.form.selected_tags)) {
      this.form.selected_tags = [];
    }
    console.log('RegisterView mounted, selected_tags:', this.form.selected_tags);
  },
  computed: {
    /**
     * Calculate overall form validity
     * Validates all required fields and tag selection limits
     * @returns {boolean} True if form is valid and can be submitted
     */
    isFormValid() {
      // Check if all required fields are filled
      const hasUsername = !!this.form.username;
      const hasEmail = !!this.form.email;
      const hasNickname = !!this.form.nickname;
      const hasPassword = !!this.form.password;
      const hasPassword2 = !!this.form.password2;
      const hasGender = !!this.form.gender;
      const hasAgeGroup = !!this.form.age_group;
      
      // Validate tag selection count (3-7 tags required)
      const hasValidTags = Array.isArray(this.form.selected_tags) && 
                          this.form.selected_tags.length >= 3 && 
                          this.form.selected_tags.length <= 7;
      
      // Debug logging for form validation
      console.log('Form validation:', {
        hasUsername,
        hasEmail,
        hasNickname,
        hasPassword,
        hasPassword2,
        hasGender,
        hasAgeGroup,
        selectedTagsLength: this.form.selected_tags?.length || 0,
        hasValidTags
      });
      
      // All conditions must be true for form to be valid
      return hasUsername && 
             hasEmail && 
             hasNickname && 
             hasPassword && 
             hasPassword2 && 
             hasGender && 
             hasAgeGroup && 
             hasValidTags;
    }
  },
  methods: {
    /**
     * Toggle debug information panel visibility
     */
    toggleDebug() {
      this.showDebug = !this.showDebug;
    },
    
    /**
     * Submit registration form
     * Validates tag selection and sends registration request to API
     */
    async register() {
      try {
        if (this.form.selected_tags.length < 3) {
          this.message = 'Please select at least 3 tags.';
          return;
        }
        
        if (this.form.selected_tags.length > 7) {
          this.message = 'You can select a maximum of 7 tags.';
          return;
        }
        
        console.log('Registration attempt:', this.form);
        
        const response = await axios.post('/api/accounts/register/', this.form);
        this.message = response.data.message;
        
        if (!this.message.includes('failed')) {
          setTimeout(() => {
            this.$router.push('/login');
          }, 1500);
        }
      } catch (error) {
        console.error('Registration failed:', error.response?.data || error);
        this.message = error.response?.data?.selected_tags || 
                       error.response?.data?.message || 
                       'Registration failed.';
      }
    }
  }
};
</script>

<style scoped>
/* Main container with gradient background */
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

/* Registration form card styling */
.register-box {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

/* Page title styling */
h2 {
  color: #2d3748;
  text-align: center;
  margin-bottom: 30px;
  font-size: 28px;
  font-weight: 600;
}

/* Form layout styling */
.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Form group container styling */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Form label styling */
label {
  color: #4a5568;
  font-size: 14px;
  font-weight: 500;
}

/* Input field styling */
input[type="text"],
input[type="email"],
input[type="password"],
select.form-select {
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.2s;
}

/* Input field focus styling */
input[type="text"]:focus,
input[type="email"]:focus,
input[type="password"]:focus,
select.form-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Gender field group styling */
.gender-group {
  margin-top: 10px;
}

/* Radio button group layout */
.radio-group {
  display: flex;
  gap: 20px;
}

/* Radio button label styling */
.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

/* Radio button input styling */
.radio-label input[type="radio"] {
  margin: 0;
}

/* Submit button styling */
.submit-btn {
  background: #667eea;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 20px;
}

/* Submit button hover state */
.submit-btn:hover {
  background: #5a67d8;
}

/* Submit button disabled state */
.submit-btn:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}

/* Debug toggle button styling */
.debug-btn {
  background: #e2e8f0;
  color: #4a5568;
  padding: 8px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  margin-top: 10px;
  cursor: pointer;
}

/* Debug information panel styling */
.debug-info {
  background: #f7fafc;
  padding: 15px;
  border-radius: 6px;
  font-size: 14px;
  margin-top: 10px;
  border: 1px solid #e2e8f0;
}

/* Debug information paragraph spacing */
.debug-info p {
  margin: 5px 0;
}

/* Message styling (success/error) */
.message {
  margin-top: 20px;
  padding: 12px;
  border-radius: 6px;
  text-align: center;
  font-size: 14px;
}

/* Error message styling */
.error {
  background: #fed7d7;
  color: #c53030;
}

/* Success message styling */
.success {
  background: #c6f6d5;
  color: #2f855a;
}

/* Responsive design for mobile screens */
@media (max-width: 640px) {
  .register-box {
    padding: 20px;
  }
  
  h2 {
    font-size: 24px;
  }
}
</style>
