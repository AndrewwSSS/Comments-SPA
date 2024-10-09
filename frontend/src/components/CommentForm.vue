<template>
  <div class="comment-form">
    <div class="tag-buttons">
      <button type="button" @click="insertTag('a href=\'\' title=\'\'', '</a>')">Link</button>
      <button type="button" @click="insertTag('code', '</code>')">Code</button>
      <button type="button" @click="insertTag('i', '</i>')">Italic</button>
      <button type="button" @click="insertTag('strong', '</strong>')">Bold</button>
    </div>

    <form @submit.prevent="submitComment">
      <textarea
          v-model="content"
          placeholder="Enter your comment"
          required
          class="comment-textarea"
          ref="commentTextarea"
      ></textarea>

      <div class="homepage-url-input">
        <label for="homepage_url">Homepage URL:</label>
        <input
          type="text"
          v-model="homepage_url"
          id="homepage_url"
          class="url-input"
          placeholder="https://example.com(optional)"
        />
        <div v-if="urlError" class="error">{{ urlError }}</div>
      </div>

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

      <!-- Preview Section -->
      <div v-if="image || text_file" class="file-preview-section">
        <div v-if="image" class="file-preview">
          <div class="preview-container">
            <img :src="imagePreview" alt="Preview Image" class="image-preview" />
            <button @click="removeFile('image')" class="remove-file-button" type="button">
              &times;
            </button>
          </div>
        </div>

        <div v-if="text_file" class="file-preview">
          <div class="preview-container">
            <p>{{ text_file.name }}</p>
            <button @click="removeFile('text_file')" class="remove-file-button" type="button">
              &times;
            </button>
          </div>
        </div>
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
    parentMessageId: Number,
  },
  data() {
    return {
      content: '',
      homepage_url: '',
      image: null,
      imagePreview: null,
      text_file: null,
      error: null,
      urlError: null,
    };
  },
  methods: {
    onFileChange(field, event) {
      const file = event.target.files[0];
      if (!file) return;

      if (field === 'image') {
        this.handleImage(file);
      } else if (field === 'text_file') {
        this.handleTextFile(file);
      }

      event.target.value = '';
    },
    handleImage(file) {
      const fileTypes = ['image/jpeg', 'image/png', 'image/gif'];
      const maxWidth = 320;
      const maxHeight = 240;

      if (!fileTypes.includes(file.type)) {
        this.error = 'Invalid image format. Please upload a JPG, PNG, or GIF file.';
        return;
      }

      const img = new Image();
      const reader = new FileReader();

      reader.onload = (e) => {
        img.src = e.target.result;
        img.onload = () => {
          let { width, height } = img;

          if (width > maxWidth || height > maxHeight) {
            const aspectRatio = width / height;
            if (width > height) {
              width = maxWidth;
              height = Math.round(maxWidth / aspectRatio);
            } else {
              height = maxHeight;
              width = Math.round(maxHeight * aspectRatio);
            }
          }

          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          canvas.width = width;
          canvas.height = height;
          ctx.drawImage(img, 0, 0, width, height);

          canvas.toBlob(
            (blob) => {
              if (this.imagePreview) {
                URL.revokeObjectURL(this.imagePreview);
              }
              this.image = new File([blob], file.name, { type: file.type });
              this.imagePreview = URL.createObjectURL(blob);
              this.error = null;
            },
            file.type,
            0.95
          );
        };
      };

      reader.readAsDataURL(file);
    },
    handleTextFile(file) {
      if (file.size > 100 * 1024) {
        this.error = 'Text file size must not exceed 100 KB.';
        return;
      }
      this.text_file = file;
      this.error = null;
    },
    removeFile(field) {
      if (field === 'image') {
        if (this.imagePreview) {
          URL.revokeObjectURL(this.imagePreview);
        }
        this.image = null;
        this.imagePreview = null;
      } else if (field === 'text_file') {
        this.text_file = null;
      }
    },
    insertTag(openTag, closeTag) {
      const textarea = this.$refs.commentTextarea;
      const { selectionStart, selectionEnd } = textarea;
      const beforeText = this.content.substring(0, selectionStart);
      const afterText = this.content.substring(selectionEnd);
      const selectedText = this.content.substring(selectionStart, selectionEnd);

      this.content = `${beforeText}<${openTag}>${selectedText}${closeTag}${afterText}`;

      this.$nextTick(() => {
        textarea.focus();
        textarea.setSelectionRange(
          selectionStart + openTag.length + 2,
          selectionEnd + openTag.length + 2
        );
      });
    },
    validateURL() {
      if (this.homepage_url) {
        const urlPattern = new RegExp(
          '^(https?:\\/\\/)?' + // Protocol
          '((([a-zA-Z\\d]([a-zA-Z\\d-]*[a-zA-Z\\d])*)\\.)+[a-zA-Z]{2,}|' + // Domain name
          '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR IP (v4) address
          '(\\:\\d+)?(\\/[-a-zA-Z\\d%_.~+]*)*' + // Port and path
          '(\\?[;&a-zA-Z\\d%_.~+=-]*)?' + // Query string
          '(\\#[-a-zA-Z\\d_]*)?$',
          'i'
        );
        if (!urlPattern.test(this.homepage_url)) {
          this.urlError = 'Please enter a valid URL.';
          return false;
        } else {
          this.urlError = null;
        }
      }
      return true;
    },
    submitComment() {
      // Проверка URL
      if (!this.validateURL()) {
        return;
      }

      const strippedContent = this.content.replace(/<\/?[^>]+(>|$)/g, '').trim();

      if (!strippedContent && !this.image && !this.text_file) {
        this.error = 'Comment cannot be empty!';
        return;
      }

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

      if (this.homepage_url) {
        formData.append('homepage_url', this.homepage_url);
      }

      send_message(formData)
        .then(() => {
          this.resetForm();
        })
        .catch((error) => {
          console.error('Error sending message:', error);
          this.error = 'Failed to submit comment. Please try again.';
        });
    },
    resetForm() {
      this.content = '';
      this.homepage_url = ''; // Сброс поля URL

      if (this.imagePreview) {
        URL.revokeObjectURL(this.imagePreview);
      }
      this.image = null;
      this.imagePreview = null;
      this.text_file = null;
      this.error = null;
      this.urlError = null;
    },
  },
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.comment-form {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
}

/* Tag insertion buttons styling */
.tag-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.tag-buttons button {
  padding: 8px 12px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background-color 0.3s ease;
}

.tag-buttons button:hover {
  background-color: #66b1ff;
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

/* Поле для ввода URL */
.homepage-url-input {
  margin-bottom: 1rem;
}

.url-input {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  font-size: 1rem;
  box-sizing: border-box;
}

.url-input:focus {
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

.file-preview-section {
  margin-top: 10px;
}

.file-preview {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.preview-container {
  position: relative;
  display: inline-block;
}

.image-preview {
  max-width: 100px;
  border-radius: 8px;
}

.remove-file-button {
  position: absolute;
  top: -10px;
  right: -10px;
  background-color: red;
  color: white;
  border: none;
  padding: 5px 8px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-file-button:hover {
  background-color: darkred;
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
