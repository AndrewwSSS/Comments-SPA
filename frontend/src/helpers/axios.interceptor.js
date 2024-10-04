import axios from 'axios';
import store from '../store';  // Assuming the Vuex store is exported from 'store/index.js'

axios.interceptors.request.use(
  config => {
    const token = JSON.parse(localStorage.getItem('user')).access;
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  },
);

axios.interceptors.response.use(
  response => {
    return response;
  },
  async error => {
    // await store.dispatch('auth/logout');
    // window.location.href = '/login';
    if (error.response.status !== 401) {
        return Promise.reject(error);
    }
    let user = JSON.parse(localStorage.getItem('user'))
    if (!user) {
        await store.dispatch('auth/logout');
        window.location.href = '/login';
    }
    let refresh_token = user.refresh;
    const response = await axios.post(
        `http://127.0.0.1:8000/api/users/token/refresh/`,
        {
            refresh: refresh_token,
        }
    )
    if (response.status === 200) {
        user.access = response.data.access;
        localStorage.setItem('user', JSON.stringify(user));
        return axios(error.config);
    }
    else {
        await store.dispatch('auth/logout');
        window.location.href = '/login';
    }
    return Promise.reject(error);
  },
);
