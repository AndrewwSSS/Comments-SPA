<template>
  <div :class="['comment-item', isReply ? 'reply-item' : '']">
    <div class="comment-body">
      <div class="comment-header">
        <div>
          <strong class="comment-username">{{ comment.user || 'Anonymous' }}</strong>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>
        <div class="comment-actions">
          <span
              @click="toggleReplyForm"
              class="icon"
              title="Reply"
          >
            <i class="fas fa-reply"></i>
          </span>
        </div>
      </div>
      <p class="comment-text" v-html="formattedContent"></p>

      <img
          v-if="comment.image"
          :src="comment.image"
          alt="comment image"
          class="comment-image"
      />
      <a
          v-if="comment.text_file"
          :href="comment.text_file"
          class="comment-file-link"
          download
      >
        <i class="fas fa-file-download"></i> Download file
      </a>

      <!-- Load Replies Button -->
      <button
          v-if="comment.replies_count && !repliesLoaded"
          @click="loadReplies"
          class="load-replies-button"
      >
        <i class="fas fa-comments"></i> View Replies ({{ comment.replies_count }})
      </button>

      <!-- Display Replies -->
      <div v-if="comment.replies" class="comment-replies">
        <CommentItem
            v-for="reply in comment.replies"
            :key="reply.id"
            :comment="reply"
            :isReply="true"
            @updateReplies="handleUpdateReplies"
        />
        <!-- Load More Replies Button -->
        <button
            v-if="nextPageNumber"
            @click="loadReplies"
            class="load-more-button"
        >
          <i class="fas fa-chevron-down"></i> Load More Replies
        </button>
      </div>

      <!-- Reply Form -->
      <div v-if="showReplyForm" class="reply-form">
        <comment-form
            :parentMessageId="comment.id"
        />
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
    };
  },
  computed: {
    formattedContent() {
      return this.comment.content.replace(/\n/g, '<br>');
    },
    nextPageNumber() {
      if (!this.nextPageURL)
        return null;

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
    handleUpdateReplies({ commentId, newReplies, nextPageURL }) {
      this.$emit('updateReplies', { commentId, newReplies, nextPageURL });
    },
    loadReplies() {
      const page = this.nextPageNumber || 1;
      get_replies(this.comment.id, page)
          .then(response => {
            if (response.status === 200) {
              const data = response.data;
              const newReplies = data.results.map(reply => ({
                ...reply,
                replies: [],
              }));
              console.log("newReplies", newReplies);
              this.$emit('updateReplies', { commentId: this.comment.id, newReplies, nextPageURL: data.next });

              this.nextPageURL = data.next;
              this.repliesLoaded = true;
            }
          })
          .catch(error => {
            console.error('Error fetching replies:', error);
          });
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
