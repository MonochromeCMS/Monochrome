type fakeBoolean = 0 | 1;

interface ReaderState {
  direction: fakeBoolean;
  readerMode: string;
  parity: fakeBoolean;
}

const state = (): ReaderState => ({
  direction: 0,
  parity: 0,
  readerMode: "Single",
});

const getters = {
  getReaderMode(state: ReaderState): string {
    return state.readerMode;
  },
  getDirection(state: ReaderState): fakeBoolean {
    return state.direction;
  },
  getParity(state: ReaderState): fakeBoolean {
    return state.parity;
  },
};

const mutations = {
  setReaderMode(state: ReaderState, payload: string): void {
    state.readerMode = payload;
  },
  setDirection(state: ReaderState, payload: fakeBoolean): void {
    state.direction = payload;
  },
  setParity(state: ReaderState, payload: fakeBoolean): void {
    state.parity = payload;
  },
};

export default {
  state,
  getters,
  mutations,
};
