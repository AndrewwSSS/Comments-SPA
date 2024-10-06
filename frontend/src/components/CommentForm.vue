<template>
  <div class="comment-form">
    <form @submit.prevent="submitComment"> <!-- This handles form submission -->
      <textarea v-model="content" placeholder="Enter your comment" required class="comment-textarea"></textarea>

      <label class="file-label">
        <span>Attach Image:</span>
        <input type="file" @change="onFileChange('image', $event)" accept="image/*" class="file-input" />
      </label>

      <label class="file-label">
        <span>Attach Text File:</span>
        <input type="file" @change="onFileChange('text_file', $event)" accept=".txt" class="file-input" />
      </label>

      <!-- Remove the @click event -->
      <button type="submit" class="submit-button">Reply</button>

      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </div>
</template>

<script>
// import axios from 'axios';
import { send_message } from "@/api";

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
    onFileChange(field, event) {
      const fileInput = event.target;
      console.log(field);
      if (fileInput.files.length > 0) {
        this[field] = fileInput.files[0];
      } else {
        this[field] = null; // Handle the case where no file is selected
      }
    },

    submitComment() {
      const messageData = {
        content: this.content,
      };

      if (this.image) {
        messageData.image = this.image;
      }

      if (this.text_file) {
        messageData.text_file = this.text_file;
      }

      if (this.parentMessageId) {
        messageData.parent_message = this.parentMessageId;
      }

      send_message(messageData);
      this.$emit('commentAdded');
      this.content = '';
      this.image = null;
      this.text_file = null;
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
