<template>
  <div class="comment-item">
<!--    <div class="comment-avatar">-->
<!--      <img :src="comment.user.avatar || defaultAvatar" alt="avatar" />-->
<!--    </div>-->
    <div class="comment-body">
      <div class="comment-header">
        <strong class="comment-username">{{ comment.user || 'Anonymous' }}</strong>
        <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        <div class="comment-actions">
          <span @click="toggleReplyForm" class="icon">&#128172;</span> <!-- Reply -->
        </div>
      </div>
      <p class="comment-text">{{ comment.content }}</p>

      <img v-if="comment.image" :src="comment.image" alt="comment image" class="comment-image" />
      <a v-if="comment.text_file" :href="comment.text_file" class="comment-file-link" download>Download file</a>

      <div v-if="comment.replies" class="comment-replies">
        <CommentItem
          v-for="reply in comment.replies"
          :key="reply.id"
          :comment="reply"
           @commentAdded="fetchReplies"
        />
      </div>

      <div v-if="showReplyForm" class="reply-form">
        <comment-form @commentAdded="fetchReplies" :parentMessageId="comment.id"/>
      </div>
    </div>
  </div>
</template>

<script>
import CommentItem from './CommentItem.vue';
import CommentForm from "@/components/CommentForm.vue";

export default {
  components: {CommentForm, CommentItem },
  props: {
    comment: Object,
  },
  data() {
    return {
      showReplyForm: false,
      replyContent: '',
      defaultAvatar: '/default-avatar.png', // Default avatar path
    };
  },
  methods: {
    toggleReplyForm() {
      this.showReplyForm = !this.showReplyForm;
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    fetchReplies() {
      this.$emit('commentAdded');
      this.showReplyForm = false;
    },
  },
};
</script>

<style scoped>
.comment-item {
  display: flex;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #fff;
  margin-bottom: 1rem;
}

.comment-avatar {
  margin-right: 10px;
}

.comment-avatar img {
  width: 50px;
  height: 50px;
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
  font-weight: bold;
  color: #333;
}

.comment-date {
  color: #999;
  font-size: 0.9rem;
}

.comment-actions {
  display: flex;
  gap: 10px;
}

.icon {
  cursor: pointer;
  font-size: 1.2rem;
  color: #007bff;
}

.comment-text {
  margin: 10px 0;
  color: #333;
}

.comment-image {
  max-width: 100%;
  margin-top: 10px;
  border-radius: 5px;
}

.comment-file-link {
  display: inline-block;
  margin-top: 10px;
  color: #007bff;
  text-decoration: none;
}

.comment-file-link:hover {
  text-decoration: underline;
}

/* Replies */
.comment-replies {
  margin-top: 1rem;
  padding-left: 20px;
  border-left: 2px solid #f0f0f0;
}

/* Reply Form */
.reply-form {
  margin-top: 10px;
}

.reply-form textarea {
  width: 100%;
  height: 60px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: vertical;
}

.reply-form button {
  margin-top: 5px;
  padding: 6px 12px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
