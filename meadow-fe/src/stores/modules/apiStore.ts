import { defineStore } from "pinia";

// 定义一个 Pinia Store，用于管理与接口调用相关的状态
export const useTempStore = defineStore("tempStore", {
  // 状态
  state: () => ({
    //apiParam: null as string | null, // 用于保存 API 参数
    Data: JSON.parse(localStorage.getItem("usetempInfo") || "null")
  }),

  // 动作
  actions: {
    setMEssageInfo(info) {
      this.Data = info;
      localStorage.setItem("usetempInfo", JSON.stringify(info)); // 保存到localStorage
    },
    // 动态改变 Data
    updateMessageInfo(newData: any) {
      this.Data = newData; // 直接修改 state 中的 Data
      // 更新 sessionStorage 和 localStorage 中的数据
      localStorage.setItem("usetempInfo", JSON.stringify(newData));
    },
    clearMEssageInfo() {
      this.Data = null;
      localStorage.removeItem("usetempInfo"); // 清除localStorage中的缓存
    }
  }
});
