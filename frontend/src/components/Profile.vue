<template>
  <div class="profile">
    <h2>Welcome, {{ user?.username }}</h2>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'UserProfile',
  setup() {
    const store = useStore();
    const user = computed(() => store.state.auth.user);

    return {
      user,
    };
  },
};
</script>
