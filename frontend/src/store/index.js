import { createStore } from 'vuex';
import { auth } from './modules/auth';
import {commentForm} from "./modules/commentForm";


const store = new createStore({
  modules: {
    auth,
    commentForm
  },
});


export default store;