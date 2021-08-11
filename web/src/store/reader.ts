interface ReaderState {
  direction: boolean;
  readerMode: string;
  parity: boolean;
}

const state = (): ReaderState => ({
  direction: false,
  parity: false,
  readerMode: "Single",
});

const getters = {
  getReaderMode(state: ReaderState): string {
    return state.readerMode;
  },
  getDirection(state: ReaderState): boolean {
    return state.direction;
  },
  getParity(state: ReaderState): boolean {
    return state.parity;
  },
};

const mutations = {
  setReaderMode(state: ReaderState, payload: string): void {
    state.readerMode = payload;
  },
  setDirection(state: ReaderState, payload: boolean): void {
    state.direction = payload;
  },
  setParity(state: ReaderState, payload: boolean): void {
    state.parity = payload;
  },
};

export default {
  state,
  getters,
  mutations,
};
