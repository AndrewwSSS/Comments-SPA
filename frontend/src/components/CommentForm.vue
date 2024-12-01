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
import {ref, nextTick} from 'vue';
import { send_message } from "@/api";
import DOMPurify from 'dompurify';

export default {
  props: {
    parentMessageId: Number,
  },
  setup(props) {
    const content = ref('');
    const image = ref(null);
    const imagePreview = ref(null);
    const text_file = ref(null);
    const error = ref(null);
    const commentTextarea = ref(null);

    const onFileChange = (field, event) => {
      const file = event.target.files[0];
      if (!file) return;

      if (field === 'image') {
        handleImage(file);
      } else if (field === 'text_file') {
        handleTextFile(file);
      }

      event.target.value = '';
    };

    const handleImage = (file) => {
      const fileTypes = ['image/jpeg', 'image/png', 'image/gif'];
      const maxWidth = 1920;
      const maxHeight = 1080;

      if (!fileTypes.includes(file.type)) {
        error.value = 'Invalid image format. Please upload a JPG, PNG, or GIF file.';
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
                if (imagePreview.value) {
                  URL.revokeObjectURL(imagePreview.value);
                }
                image.value = new File([blob], file.name, { type: file.type });
                imagePreview.value = URL.createObjectURL(blob);
                error.value = null;
              },
              file.type,
              0.95
          );
        };
      };

      reader.readAsDataURL(file);
    };

    const handleTextFile = (file) => {
      if (file.size > 100 * 1024) {
        error.value = 'Text file size must not exceed 100 KB.';
        return;
      }
      text_file.value = file;
      error.value = null;
    };

    const removeFile = (field) => {
      if (field === 'image') {
        if (imagePreview.value) {
          URL.revokeObjectURL(imagePreview.value);
        }
        image.value = null;
        imagePreview.value = null;
      } else if (field === 'text_file') {
        text_file.value = null;
      }
    };

    const insertTag = (openTag, closeTag) => {
      const textarea = commentTextarea.value;
      const { selectionStart, selectionEnd } = textarea;
      const beforeText = content.value.substring(0, selectionStart);
      const afterText = content.value.substring(selectionEnd);
      const selectedText = content.value.substring(selectionStart, selectionEnd);

      content.value = `${beforeText}<${openTag}>${selectedText}${closeTag}${afterText}`;

      nextTick(() => {
        textarea.focus();
        textarea.setSelectionRange(
            selectionStart + openTag.length + 2,
            selectionEnd + openTag.length + 2
        );
      });
    };

    const submitComment = async () => {
      const strippedContent = content.value.replace(/<\/?[^>]+(>|$)/g, '').trim();

      if (!strippedContent && !image.value && !text_file.value) {
        error.value = 'Comment cannot be empty!';
        return;
      }

      const formData = new FormData();
      if (!DOMPurify.sanitize(content.value)) {
        error.value = "Invalid content"
        return;
      }
      formData.append('content', content.value);

      if (image.value) {
        formData.append('image', image.value);
      }

      if (text_file.value) {
        formData.append('text_file', text_file.value);
      }

      if (props.parentMessageId) {
        formData.append('parent_message', props.parentMessageId);
      }

      try {
        await send_message(formData);
        resetForm();
      } catch (error) {
        console.error('Error sending message:', error);
        if (error.response && error.response.data && error.response.data.message) {
          error.value = error.response.data.message;
        } else {
          error.value = 'Failed to submit comment. Please try again.';
        }
      }
    };

    const resetForm = () => {
      content.value = '';

      if (imagePreview.value) {
        URL.revokeObjectURL(imagePreview.value);
      }
      image.value = null;
      imagePreview.value = null;
      text_file.value = null;
      error.value = null;
    };

    return {
      content,
      image,
      imagePreview,
      text_file,
      error,
      commentTextarea,
      onFileChange,
      insertTag,
      submitComment,
      removeFile,
    };
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

.captcha-section {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1rem;
}

.captcha-image {
  cursor: pointer;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
}

.captcha-input {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  font-size: 1rem;
  box-sizing: border-box;
}

.captcha-input:focus {
  border-color: #409eff;
  outline: none;
}

.refresh-captcha-button {
  padding: 8px 12px;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background-color 0.3s;
}

.refresh-captcha-button:hover {
  background-color: #ff7875;
}
</style>
