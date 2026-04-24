import { ref, onMounted, onUnmounted, watch } from "vue";
import { io, Socket } from "socket.io-client";
import { useChatNotificationStore, useModelStore, useSocketStore } from "../stores/chatStore";
import { useUserStore } from "@/stores/modules/user";
import http from "@/api";

const PORT1 = "/api/chatbox";

interface ApiResponse {
  Balance: number;
  InputLenLimit: number;
  Pattern: string;
  RequestId: string;
  SingleWorkflow: {
    IsEnable: boolean;
    Status: string;
    WorkflowDesc: string;
    WorkflowId: string;
    WorkflowName: string;
  };
  Token: string;
}

interface ApiResponseWrapper {
  apiResponse: ApiResponse;
}

export function useGetWsToken() {
  const socketStore = useSocketStore();
  const modelStore = useModelStore();
  const chatNotificationStore = useChatNotificationStore();

  const errMsg = ref("");
  watch(
    () => modelStore.modelType,
    async newModel => {
      try {
        const result = await http.get<ApiResponseWrapper>(`${PORT1}/getWsToken?model_type=${newModel}`);

        if (result.code === 200) {
          socketStore.setWsToken(result.data.apiResponse.Token);
          socketStore.setInputLenLimit(result.data.apiResponse.InputLenLimit);
          console.log("【-------------- WsToken --------------->】", result.data.apiResponse.Token);
        } else {
          chatNotificationStore.addNotification({
            type: "error",
            message: "获取Token失败,请联系管理员"
          });
          console.log("获取 WsToken 失败");
          errMsg.value = result.msg;
        }
      } catch (error) {
        chatNotificationStore.addNotification({
          type: "error",
          message: "获取Token失败,请联系管理员"
        });
        console.error("获取 WsToken 出错:请刷新重试或联系管理员", error);
        errMsg.value = "请求失败";
      } finally {
      }
    },
    { immediate: true }
  );

  return { errMsg };
}

export function useZhipuChat() {
  const errMsg = ref("");
  const isLoading = ref(false);
  const userStore = useUserStore();
  const modelStore = useModelStore();

  async function sendMessage(message: string, onChunk: (content: string) => void): Promise<string> {
    isLoading.value = true;
    errMsg.value = "";
    let fullContent = "";

    try {
      const response = await fetch(`${PORT1}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${userStore.token}`
        },
        body: JSON.stringify({
          message,
          model_type: modelStore.modelType || "GLM-4.7-Flash"
        })
      });

      if (!response.ok) {
        throw new Error(`请求失败: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error("无法读取响应");
      }

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = decoder.decode(value, { stream: true });
        fullContent += text;
        onChunk(text);
      }

      return fullContent;
    } catch (error: any) {
      console.error("智谱AI调用错误:", error);
      errMsg.value = error.message || "调用失败";
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    sendMessage,
    errMsg,
    isLoading
  };
}

export function useEstablishSocketConnection() {
  const { errMsg } = useGetWsToken();
  const socket = ref<Socket | null>(null);
  const socketStore = useSocketStore();

  watch(
    () => socketStore.WsToken,
    (newVal, oldVal, onCleanup) => {
      try {
        const socketInstance = io("wss://wss.lke.cloud.tencent.com/", {
          path: "/v1/qbot/chat/conn/", // 替换为你的路径
          transports: ["websocket", "polling"],
          withCredentials: true,
          reconnection: true,
          reconnectionAttempts: 5,
          auth: async cb => {
            cb({ token: socketStore.WsToken });
          }
        });

        socketInstance.on("connect", () => {
          socket.value = socketInstance;
          socketStore.setSocket(socketInstance);
        });

        socketInstance.on("connect_error", err => {
          console.error("连接错误:", err);
          errMsg.value = "连接服务器失败，请稍后重试";
        });

        socketInstance.on("disconnect", reason => {
          console.log("断开连接:", reason);
          if (reason === "io server disconnect") {
            // 服务器断开连接，需要重新连接
            socketInstance.connect();
          }
        });
      } catch (error) {
        console.error("Socket初始化错误:", error);
        errMsg.value = "初始化连接失败，请刷新页面重试";
      }
      onCleanup(() => {
        if (socket.value) {
          socket.value.disconnect();
        }
      });
    }
  );

  return {
    socket,
    errMsg
  };
}
