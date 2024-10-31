<template>
  <div class="comments-section">
    <h3>Comments</h3>

    <div class="sorting-controls">
      <label for="sortBy">Sort By:</label>
      <select v-model="sortBy">
        <option value="created_at">Date</option>
        <option value="user">Username</option>
      </select>

      <button @click="toggleSortOrder">
        {{ sortOrder === 'asc' ? 'Ascending' : 'Descending' }}
      </button>
    </div>

    <CommentForm :parentMessageId="null" />

    <div v-if="comments.length === 0 && !isLoading" class="no-comments">
      <p>No comments yet. Be the first to comment!</p>
    </div>

    <div v-else class="comment-list">
      <CommentItem
          v-for="comment in sortedComments"
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
import { ref, computed, onMounted } from "vue";
import CommentItem from './CommentItem.vue';
import CommentForm from './CommentForm.vue';
import { get_comments, subscribe_to_new_messages, connectWebSocket } from "@/api";

export default {
  components: { CommentItem, CommentForm },
  setup() {
    const comments = ref([]);
    const isLoading = ref(false);
    const nextPageURL = ref(null);
    const sortBy = ref("created_at");
    const sortOrder = ref("desc");

    const sortedComments = computed(() => {
      return [...comments.value].sort((a, b) => {
        let compare = 0;
        if (sortBy.value === "created_at") {
          compare = new Date(a.created_at) - new Date(b.created_at);
        } else if (sortBy.value === "user") {
          compare = a.user.localeCompare(b.user);
        }
        return sortOrder.value === "asc" ? compare : -compare;
      });
    });

    const nextPageNumber = computed(() => {
      if (!nextPageURL.value) return null;
      const url = new URL(nextPageURL.value);
      const params = new URLSearchParams(url.search);
      return Number(params.get("page"));
    });

    const updateCommentReplies = ({ comment, newReplies, nextPageURL: newNextPageURL }) => {
      const parentComment = comment;
      if (parentComment) {
        if (!parentComment.replies) {
          parentComment.replies = [];
        }
        const existingIds = new Set(parentComment.replies.map((reply) => reply.id));
        const uniqueNewComments = newReplies.filter((reply) => !existingIds.has(reply.id));
        parentComment.replies = [...parentComment.replies, ...uniqueNewComments];
        parentComment.nextPageURL = newNextPageURL;
      }
    };

    const add_comment = (newComment) => {
      if (newComment.parent_message === null || newComment.parent_message === undefined) {
        comments.value.unshift(newComment);
      } else {
        const parentComment = findCommentById(comments.value, newComment.parent_message);
        if (parentComment) {
          if (!parentComment.replies) {
            parentComment.replies = [];
          }
          parentComment.replies.push(newComment);
          parentComment.replies_count = parentComment.replies.length;
        }
      }
    };

    const findCommentById = (commentsArray, id) => {
      for (let comment of commentsArray) {
        if (comment.id === id) {
          return comment;
        } else if (comment.replies && comment.replies.length > 0) {
          const result = findCommentById(comment.replies, id);
          if (result) return result;
        }
      }
      return null;
    };

    const update_comments = (data) => {
      const newComments = data.results;
      const existingIds = new Set(comments.value.map((comment) => comment.id));
      const uniqueNewComments = newComments.filter((comment) => !existingIds.has(comment.id));
      comments.value = [...comments.value, ...uniqueNewComments];
      nextPageURL.value = data.next;
      isLoading.value = false;
    };

    const fetchComments = (page = 1) => {
      isLoading.value = true;
      get_comments(page, update_comments);
    };

    const loadMoreComments = () => {
      if (nextPageNumber.value) {
        fetchComments(nextPageNumber.value);
      }
    };

    const toggleSortOrder = () => {
      sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
    };

    onMounted(() => {
      connectWebSocket();
      fetchComments();
      subscribe_to_new_messages(add_comment);
    });

    return {
      comments,
      isLoading,
      sortedComments,
      nextPageNumber,
      sortBy,
      sortOrder,
      nextPageURL,
      updateCommentReplies,
      add_comment,
      findCommentById,
      update_comments,
      fetchComments,
      loadMoreComments,
      toggleSortOrder,
    };
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
  transition: background-color 0.3s ease;
}

.load-more button:hover {
  background-color: #66b1ff;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #409eff;
}

.sorting-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  gap: 10px;
}

.sorting-controls label {
  font-size: 1rem;
  font-weight: 500;
  color: #333;
}

.sorting-controls select {
  padding: 8px 12px;
  background-color: #f5f5f5;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  font-size: 1rem;
  color: #333;
  appearance: none; /* Hides the default dropdown arrow */
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  outline: none;
  cursor: pointer;
}

.sorting-controls select:focus {
  border-color: #409eff;
  box-shadow: 0 0 5px rgba(64, 158, 255, 0.3);
}

.sorting-controls select:hover {
  background-color: #e6f7ff;
}

.sorting-controls button {
  padding: 8px 12px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.sorting-controls button:hover {
  background-color: #66b1ff;
}

.sorting-controls select::after {
  content: '▼';
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.8rem;
  pointer-events: none;
  color: #999;
}
</style>

