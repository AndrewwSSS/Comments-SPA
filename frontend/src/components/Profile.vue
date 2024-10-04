<template>
  <div class="profile">
    <h2>Welcome, {{ user?.username }}</h2>
  </div>
</template>

<script>
export default {
  name: 'UserProfile',
  computed: {
    user() {
      return this.$store.state.auth.user;
    },
  },
};
</script>
