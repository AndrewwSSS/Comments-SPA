const initialState = {
  visibleForm: 'main',
};

export const commentForm = {
  namespaced: true,
  state: initialState,
  actions: {
    toggleForm({ commit, state }, formId) {
      if (state.visibleForm === formId) {
        commit('hideForm');
      } else {
        commit('showForm', formId);
      }
    },
  },
  mutations: {
    showForm(state, formId) {
      state.visibleForm = formId;
    },
    hideForm(state) {
      state.visibleForm = null;
    },
  },
  getters: {
    visibleForm: (state) => state.visibleForm,
  },
};