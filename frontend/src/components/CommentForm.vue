<template>
  <div class="comment-form">
    <form @submit.prevent="submitComment">
      <textarea
          v-model="content"
          placeholder="Enter your comment"
          required
          class="comment-textarea"
      ></textarea>

      <div class="file-inputs">
        <label class="file-label">
          <input
              type="file"
              @change="onFileChange('image', $event)"
              accept="image/*"
              class="file-input"
          />
          <span class="file-button">
            <i class="fas fa-image"></i> Attach Image
          </span>
        </label>

        <label class="file-label">
          <input
              type="file"
              @change="onFileChange('text_file', $event)"
              accept=".txt"
              class="file-input"
          />
          <span class="file-button">
            <i class="fas fa-file-alt"></i> Attach Text File
          </span>
        </label>
      </div>

      <button type="submit" class="submit-button">Post Comment</button>
      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </div>
</template>

<script>
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
      if (fileInput.files.length > 0) {
        this[field] = fileInput.files[0];
      } else {
        this[field] = null;
      }
    },

    submitComment() {
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

      send_message(formData)
          .then(() => {
            this.$emit('commentAdded');
            this.content = '';
            this.image = null;
            this.text_file = null;
          })
          .catch((error) => {
            console.error('Error sending message:', error);
            this.error = 'Failed to submit comment. Please try again.';
          });
    },
  },
};
</script>

<style scoped>
/* Import FontAwesome for icons */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.comment-form {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
}

.comment-textarea {
  width: 100%;
  min-height: 100px;
  padding: 15px;
  margin-bottom: 1rem;
  font-size: 1rem;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  resize: vertical;
  font-family: 'Roboto', sans-serif;
  box-sizing: border-box;
  transition: border-color 0.3s;
}

.comment-textarea:focus {
  border-color: #409eff;
  outline: none;
}

.file-inputs {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.file-label {
  position: relative;
  display: inline-block;
}

.file-input {
  display: none;
}

.file-button {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background-color: #409eff;
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background-color 0.3s;
}

.file-button i {
  margin-right: 6px;
}

.file-button:hover {
  background-color: #66b1ff;
}

.submit-button {
  padding: 10px 20px;
  background-color: #67c23a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #85ce61;
}

.error {
  color: red;
  margin-top: 10px;
  font-size: 0.9rem;
}
</style>
