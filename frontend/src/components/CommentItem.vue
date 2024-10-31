<template>
  <div :class="['comment-item', isReply ? 'reply-item' : '']">
    <div class="comment-body">
      <div class="comment-header">
        <div class="comment-user-info">
          <strong class="comment-username">{{ comment.user || 'Anonymous' }}</strong>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>
        <div class="comment-actions">
          <span @click="toggleForm(comment.id)" class="icon" title="Reply">
            <i class="fas fa-reply"></i>
          </span>
        </div>
      </div>

      <p class="comment-text" v-html="sanitizedContent"></p>

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
          v-if="comment.replies_count"
          @click="toggleReplies"
          class="load-replies-button"
      >
        <i class="fas fa-comments"></i> {{ showReplies ? 'Hide Replies' : 'View Replies' }} ({{ comment.replies_count }})
      </button>

      <div v-if="showReplies" class="comment-replies">
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

      <div v-if="isReplyFormVisible" class="reply-form">
        <comment-form :parentMessageId="comment.id" />
      </div>
    </div>
  </div>
</template>

<script>
import CommentItem from './CommentItem.vue';
import CommentForm from "@/components/CommentForm.vue";
import { get_replies } from "@/api";
import { useStore } from 'vuex';
import { computed, ref } from 'vue';
import DOMPurify from 'dompurify';

export default {
  components: { CommentForm, CommentItem },
  props: {
    comment: Object,
    isReply: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['updateReplies'],
  setup(props, { emit }) {
    const store = useStore();
    const repliesLoaded = ref(false);
    const nextPageURL = ref(null);
    const previewVisible = ref(false);
    const showReplies = ref(false);


    const formattedContent = computed(() => props.comment.content.replace(/\n/g, '<br>'));
    const sanitizedContent = computed(() => DOMPurify.sanitize(formattedContent.value));
    const nextPageNumber = computed(() => nextPageURL.value ? Number(new URLSearchParams(new URL(nextPageURL.value).search).get("page")) : null);
    const isReplyFormVisible = computed(() => store.getters['commentForm/visibleForm'] === props.comment.id);

    function formatDate(date) {
      return new Date(date).toLocaleString();
    }

    function handleUpdateReplies({ comment, newReplies, nextPageURL }) {
      emit('updateReplies', { comment, newReplies, nextPageURL });
    }

    function toggleForm(id) {
      store.dispatch('commentForm/toggleForm', id);
    }

    function loadReplies() {
      const page = nextPageNumber.value || 1;
      get_replies(props.comment.id, page)
          .then((response) => {
            if (response.status === 200) {
              const data = response.data;
              const newReplies = data.results.map((reply) => ({
                ...reply,
                replies: [],
              }));
              emit('updateReplies', {
                comment: props.comment,
                newReplies,
                nextPageURL: data.next,
              });
              nextPageURL.value = data.next;
              repliesLoaded.value = true;
            }
          })
          .catch((error) => {
            console.error('Error fetching replies:', error);
          });
    }

    function showPreview() {
      previewVisible.value = true;
    }

    function hidePreview() {
      previewVisible.value = false;
    }

    function toggleReplies() {
      if (!repliesLoaded.value && !showReplies.value) {
        loadReplies();
      }
      showReplies.value = !showReplies.value;
    }

    async function downloadFile(fileUrl) {
      try {
        const response = await fetch(fileUrl);
        if (!response.ok) throw new Error('Failed to download file.');

        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = getFileName(fileUrl);
        document.body.appendChild(link);
        link.click();
        URL.revokeObjectURL(link.href);
        document.body.removeChild(link);
      } catch (error) {
        console.error('Download error:', error);
      }
    }

    function getFileName(fileUrl) {
      return fileUrl.substring(fileUrl.lastIndexOf('/') + 1);
    }

    return {
      formattedContent,
      sanitizedContent,
      nextPageNumber,
      isReplyFormVisible,
      formatDate,
      handleUpdateReplies,
      toggleForm,
      loadReplies,
      showPreview,
      hidePreview,
      toggleReplies,
      downloadFile,
      getFileName,
      previewVisible,
      showReplies
    };
  }
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
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 1000;
}

.image-modal-content {
  max-width: 90%;
  max-height: 90%;
}

.image-modal-content img {
  max-width: 100%;
  max-height: 100%;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

/* Other styles for download button and replies */
.download-button {
  padding: 5px 10px;
  background-color: #409eff;
  color: white;
  border-radius: 5px;
}

.load-replies-button,
.load-more-button {
  margin-top: 15px;
  padding: 8px 15px;
  background-color: #ecf5ff;
  color: #409eff;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>
