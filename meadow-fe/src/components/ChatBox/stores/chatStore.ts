import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { Socket } from "socket.io-client";
import { generateSessionId } from "../utils";
import piniaPersistConfig from "@/stores/helper/persist";

// 聊天消息存储
export const useChatMsgStore = defineStore(
  "chatMsg",
  () => {
    const chatStateStore = useChatStateStore();
    const chatHistory = ref<ChatInfo[]>([]);

    // 新建聊天历史
    const newChatHistory = () => {
      const sessionId = generateSessionId();
      chatHistory.value = [...chatHistory.value, { sessionId, chatContent: [] }];
      chatStateStore.setCurrentSessionId(sessionId);
    };

    // 添加用户聊天内容
    const addUserChatContent = (data: UserChatContent) => {
      const chatContent = chatHistory.value.find(item => item.sessionId === chatStateStore.currentSessionId)!.chatContent;
      chatHistory.value = chatHistory.value.map(item => {
        if (item.sessionId === chatStateStore.currentSessionId) {
          return {
            ...item,
            chatContent: [...chatContent, data]
          };
        }
        return item;
      });
    };

    // 添加机器人聊天内容
    const addQBotChatContent = (data: BotChatContent) => {
      const chatContent = chatHistory.value.find(item => item.sessionId === chatStateStore.currentSessionId)!.chatContent;
      chatHistory.value = chatHistory.value.map(item => {
        if (item.sessionId === chatStateStore.currentSessionId) {
          return {
            ...item,
            chatContent: [...chatContent, data]
          };
        }
        return item;
      });
    };

    // 根据requestId和角色查找消息
    const findMsgByRequestIdAndRole = <T extends "user" | "assistant">(requestId: string, role: T) => {
      const session = chatHistory.value.find(item => item.sessionId === chatStateStore.currentSessionId);
      if (session) {
        return session.chatContent.find(item => item.requestId === requestId && item.role === role) as T extends "assistant"
          ? BotChatContent | undefined
          : UserChatContent | undefined;
      }
      return undefined;
    };

    // 根据requestId和角色更新聊天内容
    const updateChatContentByRequestIdAndRole = <T extends "user" | "assistant">(
      data: Partial<T extends "user" ? UserChatContent : BotChatContent>,
      requestId: string,
      role: T
    ) => {
      const msgIndex = chatHistory.value.findIndex(item => item.sessionId === chatStateStore.currentSessionId);
      const index = chatHistory.value[msgIndex].chatContent.findIndex(item => item.requestId === requestId && item.role === role);
      if (index !== -1) {
        const content = chatHistory.value[msgIndex].chatContent[index];
        chatHistory.value[msgIndex].chatContent[index] = { ...content, ...data };
      }
    };

    // 更新思考内容
    const updateThoughts = (requestId: string, procedure: any, index: number) => {
      const { debugging, ...data } = procedure;
      const msgIndex = chatHistory.value.findIndex(item => item.sessionId === chatStateStore.currentSessionId);
      const contentIndex = chatHistory.value[msgIndex].chatContent.findIndex(
        item => item.requestId === requestId && item.role === "assistant"
      );
      if (msgIndex !== -1 && chatHistory.value[msgIndex].chatContent[contentIndex]) {
        const content = chatHistory.value[msgIndex].chatContent[contentIndex] as BotChatContent;
        const thoughts = [...(content.thoughts || [])];
        thoughts[index] = {
          ...data,
          content: debugging.content
        };
        chatHistory.value[msgIndex].chatContent[contentIndex] = {
          ...content,
          thoughts
        };
      }
    };
    const deleteChatHistory = (sessionId: string) => {
      chatHistory.value = chatHistory.value.filter(item => item.sessionId !== sessionId);
      if (chatStateStore.currentSessionId === sessionId) {
        chatStateStore.setCurrentSessionId("");
        chatStateStore.setIsLandingPage(true);
      }
    };
    return {
      chatHistory,
      newChatHistory,
      addUserChatContent,
      addQBotChatContent,
      findMsgByRequestIdAndRole,
      updateChatContentByRequestIdAndRole,
      updateThoughts,
      deleteChatHistory
    };
  },
  {
    persist: piniaPersistConfig("chatbox-msg")
  }
);

// 聊天状态存储
export const useChatStateStore = defineStore("chatState", () => {
  const isLandingPage = ref(true);
  const currentSessionId = ref("");

  const setIsLandingPage = (value: boolean) => {
    isLandingPage.value = value;
  };

  const setCurrentSessionId = (id: string) => {
    currentSessionId.value = id;
  };

  return {
    isLandingPage,
    currentSessionId,
    setIsLandingPage,
    setCurrentSessionId
  };
});

// 模型存储
export const useModelStore = defineStore("model", () => {
  const modelType = ref("GLM-4.6V");

  const getModelType = computed(() => modelType.value);

  const setModelType = (type: string) => {
    modelType.value = type;
  };
  const modelList = [
    {
      name: "GLM-4.7-Flash",
      power: "免费使用",
      powerstyle: "text-green-500 bg-green-500/10"
    },
    {
      name: "GLM-4.6V",
      power: "最新版本",
      powerstyle: "text-blue-500 bg-blue-500/10"
    }
  ];
  return {
    modelType,
    modelList,
    getModelType,
    setModelType
  };
});

// Socket存储
export const useSocketStore = defineStore("socket", () => {
  const socket = ref<Socket | null>(null);
  const sendQuestion = ref<((content: string) => void) | null>(null);
  const InputLenLimit = ref(0);
  const WsToken = ref("");
  const setSocket = (s: Socket) => {
    socket.value = s;
  };

  const setSendQuestion = (fn: (content: string) => void) => {
    sendQuestion.value = fn;
  };
  const setInputLenLimit = (len: number) => {
    InputLenLimit.value = len;
  };

  const setWsToken = (token: string) => {
    WsToken.value = token;
  };
  return {
    socket,
    sendQuestion,
    setSocket,
    setSendQuestion,
    InputLenLimit,
    setInputLenLimit,
    WsToken,
    setWsToken
  };
});

interface ChatNotification {
  id: number; // 唯一标识符，用于删除通知
  type: "error" | "info" | "success" | "warning";
  message: string;
}

interface ChatNotificationStore {
  notifications: ChatNotification[];
  addNotification: (notification: Omit<ChatNotification, "id">) => void;
  clearNotification: () => void;
  shiftNotification: (notificationId: number) => void;
}

export const useChatNotificationStore = defineStore("chatNotification", () => {
  let id = 0;
  const notifications = ref<ChatNotification[]>([]);

  const addNotification = (notification: Omit<ChatNotification, "id">) => {
    notifications.value = [...notifications.value, { ...notification, id: id++ }];
  };

  const clearNotification = () => {
    notifications.value = [];
  };
  const shiftNotification = (notificationId: number) => {
    notifications.value = notifications.value.filter(notification => notification.id !== notificationId);
  };
  return {
    notifications,
    addNotification,
    clearNotification,
    shiftNotification
  };
});
