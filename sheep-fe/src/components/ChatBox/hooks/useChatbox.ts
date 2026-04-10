import { onMounted, watch, ref } from "vue";
import { useEstablishSocketConnection } from "../api";
import { useChatMsgStore, useChatStateStore, useModelStore, useSocketStore } from "../stores/chatStore";
import { v4 as uuidv4 } from "uuid";
import { ReplyPayload, ReplyQuoteInfo } from "../typings/reply-response";
import { generateSessionId, getShowType, handeLittleTagsData } from "../utils";
import { ThoughtPayload } from "thought-response";

export function useChatbox() {
  const { socket, errMsg } = useEstablishSocketConnection();
  const chatMsgStore = useChatMsgStore();
  const chatStateStore = useChatStateStore();
  const modelStore = useModelStore();
  const socketStore = useSocketStore();

  // 监听socket变化
  watch(
    () => socket.value,
    () => {
      if (!socket.value) return;

      // 监听回复消息
      socket.value.on("reply", ({ payload: data }: { payload: ReplyPayload }) => {
        if (data.session_id !== chatStateStore.currentSessionId) return; // 若新消息不属于当前机器人时，则不做处理

        // 首次回复初始化
        if (data.reply_method === 0 && data.is_final) {
          chatMsgStore.updateChatContentByRequestIdAndRole<"user">(
            {
              isFinal: true
            },
            data.request_id,
            "user"
          );
          chatMsgStore.addQBotChatContent({
            role: "assistant",
            content: "",
            recordId: data.record_id,
            requestId: data.request_id,
            isFinal: false,
            quoteInfos: data.quote_infos,
            references: [],
            anchorAttributes: { target: "_blank" },
            loadingMessage: false, // 是否加载中
            isMdExpand: false, // 是否展开所有的消息
            isReplaceLinks: false, // 是否替换链接为第三方提示
            isPrintAnimate: false, // 是否显示打字的效果
            styleObj: {}, // MD消息体的style
            clazzTable: "", // MD消息体的 table 样式
            clazzMd: "", // MD消息体的类名
            linkify: false, // markdown-it 的props透传
            timestamp: data.timestamp * 1000,
            modelType: modelStore.getModelType
          });
          return;
        }

        const findedMsg = chatMsgStore.findMsgByRequestIdAndRole<"assistant">(data.request_id, "assistant");

        if (findedMsg && findedMsg.isFinal) return; // 若消息已经"停止生成"，则新消息抛弃

        if (data.quote_infos && data.quote_infos.length > 0) {
          const quoteMock = data.quote_infos.reduce((acc: ReplyQuoteInfo[], curr: any) => {
            const existingItem = acc.find(item => item.position === curr.position);
            let res = {};
            if (findedMsg && findedMsg.references && findedMsg.references.length > 0) {
              res = findedMsg.references.find(i => i.id === curr.index) || {};
            }
            if (existingItem) {
              existingItem.tag.push({ ...res, id: curr.index });
            } else {
              acc.push({
                tag: [{ ...res, id: curr.index }],
                position: curr.position
              });
            }
            return acc;
          }, []);

          data.quote_infos = quoteMock.sort((a, b) => b.position - a.position);

          // 遍历数组，对每个元素进行操作
          data.quote_infos.forEach(item => {
            // 提取id数组并转换为字符串
            const tagIds = item.tag.map(tag => tag.id);
            const tagString = `[${tagIds.join(",")}](@ref)`;

            // 在指定位置插入字符串
            data.content = data.content.slice(0, item.position) + tagString + data.content.slice(item.position);
          });
        }

        // 更新消息内容
        chatMsgStore.updateChatContentByRequestIdAndRole<"assistant">(
          {
            role: "assistant",
            content: data.content,
            recordId: data.record_id,
            requestId: data.request_id,
            isFinal: data.is_final,
            quoteInfos: data.quote_infos,
            references: [],
            anchorAttributes: { target: "_blank" },
            loadingMessage: false,
            isMdExpand: false,
            isReplaceLinks: false,
            isPrintAnimate: false,
            styleObj: {},
            clazzTable: "",
            clazzMd: "",
            linkify: false
          },
          data.request_id,
          "assistant"
        );
      });

      // 监听思考消息
      socket.value.on("thought", ({ payload: data }: { payload: ThoughtPayload }) => {
        if (data.session_id !== chatStateStore.currentSessionId) return; // 若新消息不属于当前机器人时，则不做处理

        const findedMsg = chatMsgStore.findMsgByRequestIdAndRole<"assistant">(data.request_id, "assistant");

        // console.log("findedMsg", findedMsg);

        if (findedMsg && findedMsg.thoughts && findedMsg.thoughts.length > 0) {
          // 已有思考内容
        } else {
          // 初始化thought状态
          chatMsgStore.updateChatContentByRequestIdAndRole<"assistant">(
            {
              thoughts: [
                {
                  content: "",
                  title: "思考中",
                  titleIcon: "",
                  nodeName: "",
                  status: "processing",
                  elapsed: 0,
                  detailVisible: true,
                  index: 0
                }
              ]
            },
            data.request_id,
            "assistant"
          );
        }

        if (data && data.procedures && data.procedures.length > 0) {
          data.procedures.forEach(el => {
            el.show_type = getShowType(el);
            if (getShowType(el) === "search-reference" && el.debugging) {
              const quote_infos = el.debugging.quote_infos;
              // 给reference备注id index
              const references =
                el.debugging.references &&
                el.debugging.references.map((m: any) => ({
                  ...m,
                  id: m.index
                }));

              if (el.debugging.references) {
                el.debugging.references = references || [];
              }

              const content = el.debugging.display_content;
              if (quote_infos && quote_infos.length > 0 && references) {
                el.display_content = handeLittleTagsData(quote_infos, references, content || "");
              } else {
                el.display_content = content || "";
              }
            } else if (el.debugging) {
              const content = el.debugging.display_content;
              el.display_content = content || "";
            }
          });
        }

        // 更新store
        data.procedures.forEach((item, index) => {
          chatMsgStore.updateThoughts(data.request_id, item, index);
        });
      });
    }
  );

  // 创建发送问题的方法
  const sendQuestion = (content: string): void => {
    if (!socket.value || !content.trim()) return;

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
      isFinal: false,
      timestamp: Date.now()
    });

    // 发送消息到服务器
    socket.value.emit("send", {
      payload: {
        content,
        request_id: requestId,
        session_id: chatStateStore.currentSessionId
      }
    });
  };

  // 设置发送问题的方法到store
  socketStore.setSendQuestion(sendQuestion);

  return {
    errMsg,
    socket,
    sendQuestion
  };
}
