<template>
  <div class="comments-section">
    <h3>Comments</h3>
    <CommentForm :parentMessageId="null" />
    <div v-if="comments.length === 0" class="no-comments">
      <p>No comments yet. Be the first to comment!</p>
    </div>
    <div v-else class="comment-list">
      <CommentItem
          v-for="comment in comments"
          :key="comment.id"
          :comment="comment"
      />
    </div>
  </div>
</template>

<script>
import CommentItem from './CommentItem.vue';
import CommentForm from './CommentForm.vue';
import { get_comments, subscribe_to_new_messages, connectWebSocket } from "@/api";

export default {
  components: { CommentItem, CommentForm },
  data() {
    return {
      comments: [],
    };
  },
  methods: {
    add_comment(newComment) {
      if (newComment.parent_message === null || newComment.parent_message === undefined) {
        // New top-level comment
        this.comments.unshift(newComment);
      } else {
        // New reply, find the parent comment and update its has_replies flag
        const parentComment = this.findCommentById(this.comments, newComment.parent_message);
        if (parentComment) {
          parentComment.has_replies = true;
          // Optionally, you can decide whether to load replies immediately or prompt the user
        } else {
          console.warn(`Parent comment with id ${newComment.parent_message} not found`);
        }
      }
    },
    findCommentById(commentsArray, id) {
      for (let comment of commentsArray) {
        if (comment.id === id) {
          return comment;
        } else if (comment.replies && comment.replies.length > 0) {
          const result = this.findCommentById(comment.replies, id);
          if (result) {
            return result;
          }
        }
      }
      return null;
    },
    update_comments(comments) {
      this.comments = comments;
    },
    fetchComments() {
      get_comments(this.update_comments);
    },
  },
  mounted() {
    connectWebSocket();
    this.fetchComments();
    subscribe_to_new_messages(this.add_comment);
  },
};
</script>

<style scoped>
.comments-section {
  max-width: 700px;
  margin: 40px auto;
  padding: 0 15px;
}

h3 {
  font-size: 1.75rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.no-comments {
  text-align: center;
  padding: 20px;
  color: #909399;
}

.comment-list {
  margin-top: 20px;
}
</style>
