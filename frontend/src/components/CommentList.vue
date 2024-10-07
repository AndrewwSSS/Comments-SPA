<template>
  <div class="comments-section">
    <h3>Comments</h3>
    <CommentForm :parentMessageId="null" />

    <div v-if="comments.length === 0 && !isLoading" class="no-comments">
      <p>No comments yet. Be the first to comment!</p>
    </div>

    <div v-else class="comment-list">
      <CommentItem
          v-for="comment in comments"
          :key="comment.id"
          :comment="comment"
          @updateReplies="updateCommentReplies"
      />
    </div>

    <div v-if="nextPageNumber && !isLoading" class="load-more">
      <button @click="loadMoreComments">Load More</button>
    </div>

    <div v-if="isLoading" class="loading">
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import CommentItem from './CommentItem.vue';
import CommentForm from './CommentForm.vue';
import {
  get_comments,
  subscribe_to_new_messages,
  connectWebSocket
} from "@/api";

export default {
  components: { CommentItem, CommentForm },
  data() {
    return {
      comments: [],
      isLoading: false,
      nextPageURL: null,
    };
  },
  methods: {
    updateCommentReplies({ commentId, newReplies, nextPageURL }) {
      const parentComment = this.findCommentById(this.comments, commentId);
      console.log("parent", parentComment)
      if (parentComment) {
        if (!parentComment.replies) {
          parentComment.replies = [];
        }

        parentComment.replies = [...parentComment.replies, ...newReplies];
        parentComment.nextPageURL = nextPageURL;

        console.log("test", parentComment);
      }
    },
    add_comment(newComment) {
      if (newComment.parent_message === null || newComment.parent_message === undefined) {
        this.comments.unshift(newComment);
      } else {
        const parentComment = this.findCommentById(this.comments, newComment.parent_message);
        if (parentComment) {
          console.log(parentComment);
          parentComment.replies = [...parentComment.replies, newComment];
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
    update_comments(data) {
      this.comments = [...this.comments, ...data.results];
      this.nextPageURL = data.next
      this.isLoading = false;
    },
    fetchComments(page = 1) {
      this.isLoading = true;
      get_comments(page, this.update_comments)
    },
    loadMoreComments() {
      if(this.nextPageNumber) {
        this.fetchComments(
            this.nextPageNumber,
        )
      }
    },
  },
  computed: {
    nextPageNumber() {
      if (!this.nextPageURL)
        return null

      const url = new URL(this.nextPageURL);
      const params = new URLSearchParams(url.search);
      return Number(params.get("page"));
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

.load-more {
  text-align: center;
  margin: 20px 0;
}

.load-more button {
  padding: 10px 20px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.load-more button:hover {
  background-color: #66b1ff;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #409eff;
}
</style>
