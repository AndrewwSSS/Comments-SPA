<template>
  <div v-if="!comments" class="no-comments">
    <p>No comments yet. Be the first to comment!</p>
  </div>
  <div v-else class="comment-list">
    <CommentItem
      v-for="comment in comments"
      :key="comment.id"
      :comment="comment"
    />
  </div>
  <CommentForm :parentMessageId="null" socket="socket" />
</template>

<script>
//import axios from 'axios';
import CommentItem from './CommentItem.vue';
import CommentForm from './CommentForm.vue';
import { get_comments, subscribe_to_new_messages } from "../api";

export default {
  components: { CommentItem, CommentForm },
  data() {
    return {
      comments: [],
    };
  },
  methods: {
    add_comment(comment) {
      console.log("New comment", comment);
    },
    update_comments(comments) {
      this.comments = comments;
    }
  },
  mounted() {
    get_comments(this.update_comments);
    subscribe_to_new_messages(this.add_comment)
  },
};
</script>

<style scoped>

.comments-section {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Title for the comments section */
h3 {
  font-size: 1.5rem;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

/* Styling for the no-comments message */
.no-comments {
  text-align: center;
  padding: 20px;
  color: #555;
}

/* Styling for the list of comments */
.comment-list {
  margin-top: 20px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .comments-section {
    padding: 15px;
  }

  h3 {
    font-size: 1.2rem;
  }

  .no-comments {
    font-size: 1rem;
  }

  .comment-list {
    margin-top: 15px;
  }
}
</style>
