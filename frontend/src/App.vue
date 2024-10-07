<template>
  <div id="app">
    <header>
      <nav>
        <!-- Left side: Home link -->
        <div class="nav-group-left">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link v-if="isLoggedIn" to="/profile" class="nav-link">Profile</router-link>
          <router-link v-if="isLoggedIn" to="/comments" class="nav-link">Comments</router-link>
        </div>
        <!-- Right side: Login, Register, and Logout -->
        <div class="nav-group-right">
          <router-link v-if="!isLoggedIn" to="/login" class="nav-link">Login</router-link>
          <router-link to="/register" class="nav-link">Register</router-link>
          <button v-if="isLoggedIn" @click="logout" class="logout-button">Logout</button>
        </div>
      </nav>
    </header>

    <!-- Wrap router-view in main -->
    <main>
      <router-view></router-view>
    </main>

    <footer>
      <p>&copy; 2024 MyApp. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
// import AuthService from './services/auth'
import { mapState } from 'vuex';

export default {
  name: 'App',
  computed: {
    user() {
        return this.$store.state.auth.user;
    },
    ...mapState('auth', {
      isLoggedIn: state => state.status.loggedIn,
    }),
  },
  methods: {
    logout() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    },
  }
};
</script>

<style src="@/assets/global.css"></style>

<style scoped>

#app {
  display: flex;
  flex-direction: column;
  font-family: 'Roboto', sans-serif;
}

header {
  background-color: #007bff;
  padding: 1rem 2rem;
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.nav-group-left {
  display: flex;
  justify-content: flex-start;
  align-items: center;

.nav-group-right {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  transition: color 0.3s ease;
  margin-right: 10px;
}

.nav-link:hover {
  color: #d1e7ff;
}

.logout-button {
  background-color: #dc3545;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #c82333;
}

main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  width: 100%;
}

footer {
  background-color: #007bff;
  color: #fff;
  text-align: center;
  padding: 1rem 0;
  font-size: 0.875rem;
  width: 100%;
  position: relative;
  bottom: 0;
  left: 0;
  margin-top: auto;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  nav {
    flex-direction: column;
    gap: 0.5rem;
  }

  .nav-link, .logout-button {
    font-size: 0.9rem;
  }
}}

</style>