import axios from 'axios';
import store from '../store';

axios.interceptors.request.use(
    config => {
        const user = JSON.parse(localStorage.getItem('user'));

        if (user && user.access) {
            config.headers['Authorization'] = 'Bearer ' + user.access;
        }
        return config;
    },
    async error => {
        if (!error.response || error.response.status !== 401) {
            return Promise.reject(error);
        }

        const originalRequest = error.config;

        if (originalRequest.url.includes('/api/users/token/refresh/')) {
            await store.dispatch('auth/logout');
            window.location.href = '/login';
            return
        }
        //
        // let user = JSON.parse(localStorage.getItem('user'));
        //
        // if (!user) {
        //     await store.dispatch('auth/logout');
        //     window.location.href = '/login';
        //     return Promise.reject(error);
        // }

        return Promise.reject(error);
    }
);


axios.interceptors.response.use(
    response => {
      return response;
    },
    async error => {
      if (!error.response || error.response.status !== 401) {
        return Promise.reject(error);
      }

      let user = JSON.parse(localStorage.getItem('user'));

      if (!user) {
        await store.dispatch('auth/logout');
        window.location.href = '/login';
        return Promise.reject(error);
      }

      let refresh_token = user.refresh;
      try {
        const response = await axios.post(
            `http://127.0.0.1:8000/api/users/token/refresh/`,
            { refresh: refresh_token }
        );

        if (response.status === 200) {
          user.access = response.data.access;
          localStorage.setItem('user', JSON.stringify(user));

          error.config.headers['Authorization'] = 'Bearer ' + response.data.access;
          return axios(error.config);
        }
      } catch (refreshError) {
        await store.dispatch('auth/logout');
        window.location.href = '/login';
      }

      return Promise.reject(error);
    }
);
