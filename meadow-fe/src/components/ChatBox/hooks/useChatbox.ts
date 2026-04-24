import { onMounted, watch, ref } from "vue";
import { useZhipuChat } from "../api";
import { useChatMsgStore, useChatStateStore, useModelStore, useSocketStore } from "../stores/chatStore";
import { v4 as uuidv4 } from "uuid";
import { generateSessionId, getShowType, handeLittleTagsData } from "../utils";

export function useChatbox() {
  const { sendMessage: zhipuSendMessage, errMsg } = useZhipuChat();
  const chatMsgStore = useChatMsgStore();
  const chatStateStore = useChatStateStore();
  const modelStore = useModelStore();
  const socketStore = useSocketStore();

  let currentContent = "";

  // 创建发送问题的方法
  const sendQuestion = async (content: string): Promise<void> => {
    if (!content.trim()) return;

    // 从欢迎页切换到聊天页
    if (chatStateStore.isLandingPage) {
      // 创建新的聊天记录
      chatMsgStore.newChatHistory();
      chatStateStore.setIsLandingPage(false);
    }

    // 添加用户消息到历史
    const requestId = uuidv4();

    chatMsgStore.addUserChatContent({
      role: "user",
      content,
      requestId,
      recordId: uuidv4(),
      isFinal: true,
      timestamp: Date.now()
    });

    // 添加 AI 消息占位
    chatMsgStore.addQBotChatContent({
      role: "assistant",
      content: "",
      recordId: uuidv4(),
      requestId: requestId,
      isFinal: false,
      quoteInfos: [],
      references: [],
      anchorAttributes: { target: "_blank" },
      loadingMessage: false,
      isMdExpand: false,
      isReplaceLinks: false,
      isPrintAnimate: false,
      styleObj: {},
      clazzTable: "",
      clazzMd: "",
      linkify: false,
      timestamp: Date.now(),
      modelType: modelStore.getModelType
    });

    currentContent = "";

    try {
      // 调用智谱AI
      await zhipuSendMessage(content, (chunk: string) => {
        currentContent += chunk;

        // 逐块更新消息内容
        chatMsgStore.updateChatContentByRequestIdAndRole<"assistant">(
          {
            role: "assistant",
            content: currentContent,
            isFinal: false
          },
          requestId,
          "assistant"
        );
      });

      // 标记完成
      chatMsgStore.updateChatContentByRequestIdAndRole<"assistant">(
        {
          role: "assistant",
          content: currentContent,
          isFinal: true
        },
        requestId,
        "assistant"
      );
    } catch (error: any) {
      // 处理错误
      chatMsgStore.updateChatContentByRequestIdAndRole<"assistant">(
        {
          role: "assistant",
          content: `调用智谱AI失败: ${error.message}`,
          isFinal: true
        },
        requestId,
        "assistant"
      );
    }
  };

  // 设置发送问题的方法到store
  socketStore.setSendQuestion(sendQuestion);

  return {
    errMsg,
    sendQuestion
  };
}
