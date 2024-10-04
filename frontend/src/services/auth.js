import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';

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
          localStorage.setItem('user', JSON.stringify(response.data));
        }
        return response.data;
      });
    }
}

export default new AuthService();
