<template>
  <div class="register-container">
    <div class="register-box">
      <h2>Register</h2>
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="input-group">
          <label for="username">Username:</label>
          <input id="username" v-model="username" type="text" required />
        </div>
        <div class="input-group">
          <label for="email">Email:</label>
          <input id="email" v-model="email" type="email" required />
        </div>
        <div class="input-group">
          <label for="password">Password:</label>
          <input id="password" v-model="password" type="password" required />
        </div>
        <button class="register-button">Register</button>
        <div v-if="error" class="error-message">{{ error }}</div>
      </form>
    </div>
  </div>
</template>


<script>
import { mapActions } from 'vuex';

export default {
  name: 'UserRegister',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      error: null,
    };
  },
  methods: {
    ...mapActions({
      register: 'auth/register',
    }),
    handleRegister() {
      this.register({ username: this.username, email: this.email, password: this.password })
        .then(() => {
          this.$router.push('/login');
        })
        .catch((err) => {
          console.log(err);
          this.error = err.response.data;
        });
    },
  },
};
</script>

<style scoped>
/* Container for centering the form */
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

/* Styling the registration box */
.register-box {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

/* Title styling */
h2 {
  font-family: 'Roboto', sans-serif;
  font-weight: 500;
  margin-bottom: 1.5rem;
  color: #333;
}

/* Form layout */
.register-form {
  display: flex;
  flex-direction: column;
}

/* Input groups */
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
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
  box-sizing: border-box; /* Prevents overflow of the input fields */
}

.input-group input:focus {
  border-color: #00aaff;
  outline: none;
}

/* Register button */
.register-button {
  padding: 0.8rem;
  background-color: #00aaff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.register-button:hover {
  background-color: #008ecc;
}

/* Error message styling */
.error-message {
  margin-top: 1rem;
  color: red;
  font-size: 0.9rem;
}
</style>