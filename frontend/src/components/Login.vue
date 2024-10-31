<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <label for="username">Username:</label>
          <input id="username" v-model="username" type="text" required />
        </div>
        <div class="input-group">
          <label for="password">Password:</label>
          <input id="password" v-model="password" type="password" required />
        </div>
        <button class="login-button">Login</button>
        <div v-if="error" class="error-message">{{ error }}</div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
  name: 'UserLogin',
  setup() {
    const store = useStore();
    const router = useRouter();

    const username = ref('');
    const password = ref('');
    const error = ref(null);

    const handleLogin = () => {
      store.dispatch('auth/login', { username: username.value, password: password.value })
        .then(() => {
          router.push('/comments');
        })
        .catch(() => {
          error.value = 'Invalid username or password.';
          password.value = '';
        });
    };

    return {
      username,
      password,
      error,
      handleLogin,
    };
  },
};
</script>


<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Full height of the viewport */
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.login-box {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

h2 {
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
  margin-bottom: 1.5rem;
  color: #333;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.input-group {
  margin-bottom: 1.2rem;
}

.input-group label {
  display: block;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: #555;
}

.input-group input {
  width: 100%; /* Make the input fill the available width of its container */
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
  box-sizing: border-box; /* Ensures padding and borders are included in the element's width */
}

.input-group input:focus {
  border-color: #00aaff;
  outline: none;
}

.login-button {
  padding: 0.8rem;
  background-color: #00aaff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #008ecc;
}

.error-message {
  margin-top: 1rem;
  color: red;
  font-size: 0.9rem;
}
</style>