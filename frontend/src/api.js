import axios from "axios";

let user = JSON.parse(localStorage.getItem('user'));

const socket = new WebSocket(`${process.env.VUE_APP_WS_URL}ws/comments/?token=${user.access}`);

function refreshToken() {
  user = JSON.parse(localStorage.getItem('user'));
  console.log(user);
  console.log(process.env.VUE_APP_API_URL);

  return axios
    .post(process.env.VUE_APP_API_URL + 'users/token/refresh/', {
      refresh: user.refresh,
    })
    .then(response => {
      if (response.status === 200) {
        localStorage.setItem('user', JSON.stringify({
          access: response.data.access,
          refresh: user.refresh,
          username: user.username,
        }));
      }
      return user;
    });
}

function sendToWebSocket(message) {
  const stringifiedMessage = JSON.stringify(message);

  if (socket.readyState === WebSocket.OPEN) {
    socket.send(stringifiedMessage);
    return;
  }

  socket.addEventListener(
    "open",
    () => {
      socket.send(stringifiedMessage);
    },
    { once: true }
  );
}


socket.onerror = (error) => {
  console.error("WebSocket error:", error);
};

socket.onclose = () => {
  console.log("WebSocket disconnected");
}

socket.addEventListener("message", (event) => {
   const data = JSON.parse(event.data);
    if (data.action === "disconnect") {
      console.log(event);
      let test = refreshToken()
      console.log(test)
    }
});

export function subscribe_to_message_list(cb) {
  sendToWebSocket({action: "list_comments"});

  socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    if (data.action === "list_comments") {
      cb(data.comments)
    }
  });
}

export function send_message(msg) {
  const test = {action: "create_comment", ...msg}
  console.log(test);
  sendToWebSocket(test);
}
