<template>
  <div :class="['comment-item', isReply ? 'reply-item' : '']">
    <div class="comment-body">
      <div class="comment-header">
        <div class="comment-user-info">
          <strong class="comment-username">{{ comment.user || 'Anonymous' }}</strong>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>

        <div class="comment-actions">
          <button
            v-if="comment.homepage_url"
            @click="handleHomepageClick"
            class="homepage-button"
          >
            <i class="fas fa-external-link-alt"></i> Visit Homepage
          </button>

          <span @click="toggleReplyForm" class="icon" title="Reply">
            <i class="fas fa-reply"></i>
          </span>
        </div>
      </div>

      <p class="comment-text" v-html="formattedContent"></p>

      <div v-if="comment.image" class="image-container">
        <img
          :src="comment.image"
          alt="comment image"
          class="comment-image"
          @click="showPreview"
        />
      </div>

      <div v-if="previewVisible" class="image-modal" @click="hidePreview">
        <div class="image-modal-content">
          <img :src="comment.image" alt="Full size image" />
        </div>
      </div>

      <div v-if="comment.text_file" class="file-container">
        <a
          href="#"
          class="download-button"
          @click.prevent="downloadFile(comment.text_file)"
        >
          <i class="fas fa-file-download"></i> Download {{ getFileName(comment.text_file) }}
        </a>
      </div>

      <button
        v-if="comment.replies_count && !repliesLoaded"
        @click="loadReplies"
        class="load-replies-button"
      >
        <i class="fas fa-comments"></i> View Replies ({{ comment.replies_count }})
      </button>

      <div v-if="comment.replies" class="comment-replies">
        <CommentItem
          v-for="reply in comment.replies"
          :key="reply.id"
          :comment="reply"
          :isReply="true"
          @updateReplies="handleUpdateReplies"
        />
        <button
          v-if="nextPageNumber"
          @click="loadReplies"
          class="load-more-button"
        >
          <i class="fas fa-chevron-down"></i> Load More Replies
        </button>
      </div>

      <div v-if="showReplyForm" class="reply-form">
        <comment-form :parentMessageId="comment.id" />
      </div>
    </div>
  </div>
</template>

<script>
import CommentItem from './CommentItem.vue';
import CommentForm from "@/components/CommentForm.vue";
import { get_replies } from "@/api";

export default {
  components: { CommentForm, CommentItem },
  props: {
    comment: Object,
    isReply: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      showReplyForm: false,
      repliesLoaded: false,
      nextPageURL: null,
      previewVisible: false,
      showModal: false,
    };
  },
  computed: {
    formattedContent() {
      return this.comment.content.replace(/\n/g, '<br>');
    },
    nextPageNumber() {
      if (!this.nextPageURL) return null;

      const url = new URL(this.nextPageURL);
      const params = new URLSearchParams(url.search);
      return Number(params.get("page"));
    },
  },
  methods: {
    toggleReplyForm() {
      this.showReplyForm = !this.showReplyForm;
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    handleHomepageClick() {
      if (this.comment.homepage_url) {
        window.open(this.comment.homepage_url, '_blank');
      }
    },
    closeModal() {
      this.showModal = false;
    },
    handleUpdateReplies({commentId, newReplies, nextPageURL}) {
      this.$emit('updateReplies', {commentId, newReplies, nextPageURL});
    },
    loadReplies() {
      const page = this.nextPageNumber || 1;
      get_replies(this.comment.id, page)
          .then((response) => {
            if (response.status === 200) {
              const data = response.data;
              const newReplies = data.results.map((reply) => ({
                ...reply,
                replies: [],
              }));
              this.$emit('updateReplies', {
                commentId: this.comment.id,
                newReplies,
                nextPageURL: data.next,
              });

              this.nextPageURL = data.next;
              this.repliesLoaded = true;
            }
          })
          .catch((error) => {
            console.error('Error fetching replies:', error);
          });
    },
    showPreview() {
      this.previewVisible = true;
    },
    hidePreview() {
      this.previewVisible = false;
    },
    async downloadFile(fileUrl) {
      try {
        const response = await fetch(fileUrl);
        if (!response.ok) {
          throw new Error('Failed to download file.');
        }

        const blob = await response.blob();
        const link = document.createElement('a');
        const objectURL = URL.createObjectURL(blob);

        link.href = objectURL;
        link.download = this.getFileName(fileUrl);
        document.body.appendChild(link);
        link.click();
        URL.revokeObjectURL(objectURL); // Освобождаем память
        document.body.removeChild(link); // Удаляем ссылку из DOM
      } catch (error) {
        console.error('Download error:', error);
      }
    },
    getFileName(fileUrl) {
      return fileUrl.substring(fileUrl.lastIndexOf('/') + 1);
    },
  },
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.comment-item {
  display: flex;
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
  background-color: #fff;
}

.reply-item {
  margin-left: 50px;
  border-left: 2px solid #ebeef5;
}

.comment-avatar {
  margin-right: 15px;
}

.comment-avatar img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.comment-body {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-user-info {
  display: flex;
  align-items: center;
}

.comment-username {
  font-weight: 500;
  color: #333;
  margin-right: 10px;
}

.comment-date {
  color: #909399;
  font-size: 0.85rem;
}

.comment-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.icon {
  cursor: pointer;
  font-size: 1rem;
  color: #909399;
  transition: color 0.3s;
}

.icon:hover {
  color: #409eff;
}

.comment-text {
  margin: 10px 0;
  color: #606266;
  line-height: 1.6;
}

/* Кнопка для перехода на домашнюю страницу */
.homepage-button {
  background-color: #409eff;
  color: white;
  padding: 6px 10px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
}

.homepage-button:hover {
  background-color: #66b1ff;
}

.comment-image {
  max-width: 100%;
  margin-top: 10px;
  border-radius: 8px;
  cursor: pointer;
}

.comment-image:hover {
  opacity: 0.8;
}

.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.image-modal-content {
  position: relative;
  max-width: 100%;
  max-height: 100%;
}

.image-modal-content img {
  max-width: 90%;
  max-height: 90%;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.comment-file-link {
  display: inline-block;
  margin-top: 10px;
  color: #409eff;
  text-decoration: none;
  font-size: 0.95rem;
}

.comment-file-link:hover {
  text-decoration: underline;
}

.file-container {
  margin-top: 10px;
}

.download-button {
  display: inline-block;
  padding: 5px 10px;
  background-color: #409eff;
  color: white;
  border-radius: 5px;
  text-decoration: none;
}

.download-button:hover {
  background-color: #66b1ff;
}

.load-replies-button,
.load-more-button {
  margin-top: 15px;
  padding: 8px 15px;
  background-color: #ecf5ff;
  color: #409eff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 6px;
}

.load-replies-button:hover,
.load-more-button:hover {
  background-color: #d9ecff;
}

.comment-replies {
  margin-top: 1rem;
}

.reply-form {
  margin-top: 20px;
}
</style>
