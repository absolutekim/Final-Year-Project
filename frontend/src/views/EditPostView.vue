<template>
  <!-- Post editing form container -->
  <div>
    <h1>Modify Post</h1>
    <!-- Post edit form with title and content fields -->
    <form @submit.prevent="updatePost">
      <label>Title:</label>
      <input type="text" v-model="title" required>
      <label>Content:</label>
      <textarea v-model="content" required></textarea>
      <button type="submit">Upload Post</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

/**
 * Edit Post View Component
 * Allows users to modify their existing community posts
 * Loads existing post data and handles form submission for updates
 */
export default {
  data() {
    return {
      title: '', // Post title field
      content: '' // Post content field
    };
  },
  /**
   * Fetch the current post data when component is created
   * Populates form fields with existing post data
   */
  async created() {
    const postId = this.$route.params.id;
    const response = await axios.get(`/api/posts/${postId}/`);
    this.title = response.data.title;
    this.content = response.data.content;
  },
  methods: {
    /**
     * Submit the updated post data to the server
     * Validates inputs and redirects to the post page on success
     */
    async updatePost() {
      if (!this.title.trim() || !this.content.trim()) return;
      await axios.put(`/api/posts/${this.$route.params.id}/`, {
        title: this.title,
        content: this.content
      });
      this.$router.push(`/community/${this.$route.params.id}`);
    }
  }
};
</script>

<style scoped>
/* Form container styling */
div {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

/* Page title styling */
h1 {
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 2rem;
}

/* Form element styling */
form {
  display: flex;
  flex-direction: column;
}

/* Form label styling */
label {
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #2c3e50;
}

/* Input field styling */
input[type="text"] {
  padding: 0.75rem;
  margin-bottom: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

/* Textarea styling */
textarea {
  padding: 0.75rem;
  margin-bottom: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-height: 200px;
  font-size: 1rem;
  resize: vertical;
}

/* Submit button styling */
button[type="submit"] {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  align-self: flex-start;
  transition: background-color 0.2s;
}

/* Submit button hover state */
button[type="submit"]:hover {
  background-color: #2980b9;
}
</style>
