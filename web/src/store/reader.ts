interface ReaderState {
  direction: boolean;
  readerMode: string;
}

const state = (): ReaderState => ({
  direction: true,
  readerMode: "Single",
});

const getters = {
  getReaderMode(state: ReaderState) {
    return state.readerMode;
  },
  getDirection(state: ReaderState) {
    return state.direction;
  },
}

const mutations = {
  setReaderMode(state: ReaderState, payload: string): void {
    state.readerMode = payload;
  },
  setDirection(state: ReaderState, payload: boolean): void {
    state.direction = payload;
  },
};

export default {
  state,
  getters,
  mutations,
};
