<template>
  <v-container class="new-post-container">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="new-post-card" elevation="4">
          <v-card-title class="text-center text-h4 font-weight-bold primary--text">
            Create New Post
          </v-card-title>

          <v-card-text>
            <v-form @submit.prevent="createPost" ref="form">
              <v-text-field
                v-model="title"
                label="Title"
                outlined
                dense
                required
                :rules="[v => !!v || 'Write your Title']"
                class="mb-4"
                placeholder="Please Write your Title..."
              ></v-text-field>

              <v-textarea
                v-model="content"
                label="내용"
                outlined
                dense
                required
                :rules="[v => !!v || 'Write your Content']"
                rows="10"
                class="mb-6"
                placeholder="Please Write your Content..."
              ></v-textarea>

              <div class="d-flex justify-space-between">
                <v-btn
                  color="grey"
                  text
                  @click="$router.push('/community')"
                >
                  <v-icon left>mdi-arrow-left</v-icon>
                  Back to List
                </v-btn>
                <v-btn
                  color="primary"
                  type="submit"
                  :loading="loading"
                  :disabled="!title.trim() || !content.trim()"
                >
                  <v-icon left>mdi-check</v-icon>
                  Upload Post
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      title: '',
      content: '',
      loading: false
    };
  },
  methods: {
    async createPost() {
      if (!this.title.trim() || !this.content.trim()) return;
      
      this.loading = true;
      try {
        const userId = localStorage.getItem('user_id');
        const response = await axios.post(`http://localhost:8000/api/community/posts/`, {
          title: this.title,
          content: this.content,
          author_id: userId
        });

        console.log("✅ 게시글 작성 성공:", response.data);
        this.$router.push('/community');
      } catch (error) {
        console.error("🚨 게시글 작성 실패:", error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.new-post-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%);
  padding: 40px 0;
}

.new-post-card {
  border-radius: 12px;
  overflow: hidden;
}

.v-card-title {
  padding: 24px 16px;
  border-bottom: 2px solid #eee;
}

.v-card-text {
  padding: 24px 16px;
}

.v-text-field {
  background-color: #f8f9fa;
  border-radius: 4px;
}

.v-textarea {
  background-color: #f8f9fa;
  border-radius: 4px;
}

.v-btn {
  text-transform: none;
  letter-spacing: 0.5px;
}

.v-form {
  max-width: 100%;
}
</style>
