<template>
  <div class="comment-form">
    <form @submit.prevent="submitComment"> <!-- This handles form submission -->
      <textarea v-model="content" placeholder="Enter your comment" required class="comment-textarea"></textarea>

      <label class="file-label">
        <span>Attach Image:</span>
        <input type="file" @change="onFileChange('image')" accept="image/*" class="file-input" />
      </label>

      <label class="file-label">
        <span>Attach Text File:</span>
        <input type="file" @change="onFileChange('text_file')" accept=".txt" class="file-input" />
      </label>

      <!-- Remove the @click event -->
      <button type="submit" class="submit-button">Reply</button>

      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    parentMessageId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      content: '',
      image: null,
      text_file: null,
      error: null,
    };
  },
  methods: {
    onFileChange(field) {
      const fileInput = event.target;
      if (fileInput.files.length > 0) {
        this[field] = fileInput.files[0];
      }
    },
    submitComment() {
      console.log("submit");
      const formData = new FormData();
      formData.append('content', this.content);
      if (this.image) {
        formData.append('image', this.image);
      }
      if (this.text_file) {
        formData.append('text_file', this.text_file);
      }
      if (this.parentMessageId) {
        formData.append('parent_message', this.parentMessageId);
      }
      console.log(formData);

      axios.post('http://127.0.0.1:8000/api/comments/', formData)
        .then(() => {
          this.$emit('commentAdded');
          this.content = '';
          this.image = null;
          this.text_file = null;
        })
        .catch((error) => {
          this.error = 'Error submitting the comment.';
          console.error('Error:', error);
        });
    },
  },
};
</script>

<style scoped>
/* General Styling */
.comment-form {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 1rem;
}

.comment-textarea {
  width: 100%;
  height: 120px;
  padding: 10px;
  margin-bottom: 1rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  resize: vertical;
  font-family: 'Roboto', sans-serif;
  box-sizing: border-box;
}

/* File Input Styling */
.file-label {
  display: block;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.file-input {
  display: block;
  margin-top: 5px;
  padding: 5px;
  font-size: 0.9rem;
}

/* Submit Button */
.submit-button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #0056b3;
}

/* Error Styling */
.error {
  color: red;
  margin-top: 10px;
  font-size: 0.9rem;
}
</style>
