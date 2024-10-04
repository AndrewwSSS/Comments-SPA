<template>
  <div class="home">
    <h1>Welcome to the Home Page</h1>
    <p>This is the home page of your Vue.js application.</p>
  </div>
</template>

<script>
export default {
  name: 'UserHome',  // Make sure the name is multi-word compliant if you're using ESLint rules
};
</script>

<style scoped>
.home {
  text-align: center;
}

h1 {
  color: #42b983;
}
</style>
