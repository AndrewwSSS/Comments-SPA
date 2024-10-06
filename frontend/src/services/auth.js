import axios from 'axios';

const API_URL = process.env. VUE_APP_API_URL;

class AuthService {
  login(user) {
    return axios
      .post(API_URL + 'users/token/', {
        username: user.username,
        password: user.password,
      })
      .then(response => {
        if (response.data.access && response.data.refresh) {
           let user_obj = response.data
           user_obj.username = user.username
           localStorage.setItem('user', JSON.stringify(user_obj));
        }
        return response.data;
      });
  }

  logout() {
    localStorage.removeItem('user');
  }

  register(user) {
    return axios.post(API_URL + 'users/register/', {
      username: user.username,
      email: user.email,
      password: user.password,
    });
  }

  refreshToken() {
    let user = localStorage.getItem('user');
    return axios
      .post(API_URL + 'users/token/refresh/', {
        refresh: user.refresh,
      })
      .then(response => {
        if (response.data.access) {
          user.update(response.data);
          localStorage.setItem('user', JSON.stringify(response.data));
        }
        return user;
      });
    }
}

export default new AuthService();
