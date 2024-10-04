import { createRouter, createWebHistory } from 'vue-router';
import UserHome from '../components/Home.vue';
import UserLogin from '../components/Login.vue';
import UserRegister from '../components/Register.vue';
import UserProfile from '../components/Profile.vue';
import CommentList from "../components/CommentList.vue";

const routes = [
  { path: '/', component: UserHome },
  { path: '/login', component: UserLogin },
  { path: '/register', component: UserRegister },
  { path: '/profile', component: UserProfile },
  { path: '/comments', component: CommentList },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
