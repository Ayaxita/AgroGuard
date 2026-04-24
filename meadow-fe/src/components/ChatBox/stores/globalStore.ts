import { defineStore } from "pinia";

interface AppStateState {
  isChatboxShow: boolean;
}

export const useAppStateStore = defineStore("appState", {
  state: (): AppStateState => ({
    isChatboxShow: false
  }),
  actions: {
    setIsChatboxShow(isChatboxShow: boolean) {
      this.isChatboxShow = isChatboxShow;
    }
  }
});
