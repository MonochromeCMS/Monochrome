type fakeBoolean = 0 | 1;

interface ReaderState {
  direction: fakeBoolean;
  readerMode: string;
  parity: fakeBoolean;
  width: string;
  fit: string;
}

const state = (): ReaderState => ({
  direction: 0,
  parity: 0,
  width: "75%",
  readerMode: "Single",
  fit: "default",
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
  getFit(state: ReaderState): string {
    return state.fit;
  },
  getWidth(state: ReaderState): string {
    return state.width;
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
  setFit(state: ReaderState, payload: string): void {
    state.fit = payload;
  },
  setWidth(state: ReaderState, payload: string): void {
    state.width = payload;
  },
};

export default {
  state,
  getters,
  mutations,
};
