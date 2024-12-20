import axios from "axios";

let socket;
let user = JSON.parse(localStorage.getItem('user'));


function refreshToken() {
  user = JSON.parse(localStorage.getItem('user'));

  return axios
      .post(`${process.env.VUE_APP_API_URL}users/token/refresh/`, {
        refresh: user.refresh,
      })
      .then(response => {
        if (response.status === 200) {
          const newUser = {
            access: response.data.access,
            refresh: user.refresh,
            username: user.username,
          };
          localStorage.setItem('user', JSON.stringify(newUser));
          return newUser.access;
        } else {
          throw new Error('Failed to refresh token');
        }
      })
      .catch(error => {
        console.error("Failed to refresh token", error);
        return null;
      });
}

export const fetch_captcha = () => {
  return axios.get(`${process.env.VUE_APP_API_URL}captcha`).then(response => response.data);
};


export function connectWebSocket() {
  user = JSON.parse(localStorage.getItem('user'));
  if(!user) {
    console.log("UNAUTHORIZED")
  }
  socket = new WebSocket(`${process.env.VUE_APP_WS_URL}ws/comments/?token=${user.access}`);

  socket.onopen = () => {
    console.log("WebSocket connected");
  };

  socket.onclose = async (event) => {
    if (event.code === 4001) {
      console.log("Token expired, refreshing token...");
      const newToken = await refreshToken();
      if (newToken) {
        connectWebSocket();
      } else {
        console.error("Failed to refresh token");
      }
    } else {
      console.log("WebSocket disconnected, attempting to reconnect...");
      setTimeout(() => connectWebSocket(), 1000);
    }
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
}

export function subscribe_to_new_messages(cb) {
  socket.addEventListener("message", (event) => {
    let data = JSON.parse(event.data);
    console.log("Received message", data);
    if(data.action === "chat_message") {
      cb(data.comment)
    }
  })
}

export async function send_message(msg) {
  return axios.post(`${process.env.VUE_APP_API_URL}comments/`, msg);
}

export function get_comments(page = 1, cb) {
  axios
      .get(`${process.env.VUE_APP_API_URL}comments/`, {
        params: { page },
      })
      .then((response) => {
        cb(response.data);
      })
      .catch((error) => {
        console.error("Failed to fetch comments:", error);
      });
}

export function get_replies(commentId, page = 1) {
  return axios.get(
      `${process.env.VUE_APP_API_URL}comments/${commentId}/replies/`,
      {
        params: {
          page: page,
        },
      }
  );
}