import { createStore } from 'vuex';
import { auth } from './auth.module';


const store = new createStore({
  modules: {
    auth,
  },
});


export default store;