interface ChatInfo {
  sessionId: string; // 会话id，用于区分历史记录里不同的会话
  chatContent: (BotChatContent | UserChatContent)[]; // 聊天内容
}

interface ReferenceState {
  id: number; // 引用的id
  type: number;
  url: string; // 引用的url
  name: string;
  docId: number;
  docBizId: number;
  docName: string;
  qaBizId: string;
}

interface UserChatContent {
  role: "user"; // 消息角色，用户
  timestamp: number; // 时间戳
  content: string; // 消息内容
  recordId: string; // 消息id
  requestId: string;
  isFinal: boolean; // 消息是否输出结束
  references?: ReferenceState[];
}

interface ThoughtData {
  // 融合了api回复的precedures
  index: number;
  title: string; // 标题
  titleIcon: string; // 标题旁的icon，后端一般返回 emoji 图标地址
  nodeName?: string; // 非必传，显示大模型名称
  status: string; // 思考状态，用来显示不同状态 icon
  detailVisible?: boolean; // 控制思考内容区域是否显示，配合onTitleClick，可以控制思考内容展开和收起
  elapsed: number; // 思考时间，单位 ms
  content: string; // 思考内容
}

interface BotChatContent {
  role: "assistant"; // 消息角色，机器人
  content: string; // 消息内容
  isFinal: boolean; // 消息是否输出结束
  loadingMessage: boolean; // 是否加载中
  isMdExpand: boolean; // 是否展开所有的消息
  isReplaceLinks: boolean; // 是否替换链接为第三方提示
  isPrintAnimate: boolean; // 是否显示打字的效果
  styleObj: object; // MD消息体的style
  clazzTable: string; // MD消息体的 table 样式
  clazzMd: string; // MD消息体的类名
  anchorAttributes: object; // 为链接添加自定义属性，如{target: '_blank'}
  recordId: string;
  requestId: string;
  references?: ReferenceState[];
  quoteInfos?: ReplyQuoteInfo[] | null;
  linkify: boolean; // markdown-it 的props透传
  thoughts?: ThoughtData[];
  timestamp?: number;
  modelType?: string;
}

interface ChatMsgState {
  ChatHistories: ChatInfo[];

  // 会话管理
  newChatHistory: () => void;
  setChatHistory: (content: []) => void;

  // 消息操作
  addQBotChatContent: (content: BotChatContent) => void;
  addUserChatContent: (content: UserChatContent) => void;
  updateChatContentByRequestIdAndRole: <T extends "user" | "assistant">(
    content: T extends "assistant" ? Partial<BotChatContent> : Partial<UserChatContent>,
    request_id: string,
    role: "assistant" | "user"
  ) => void;
  findMsgByRequestIdAndRole: <T extends "user" | "assistant">(
    requestId: string,
    role: T
  ) => T extends "assistant" ? BotChatContent | undefined : UserChatContent | undefined;
  getCurrentChatContent: () => ChatInfo | undefined;
  updateThoughts: (content: Partial<ThoughtData>, requestId: string, thoughtIndex: number) => void;
  deleteChatHistory: (sessionId: string) => void;
}

interface modelListProps {
  name: string;
  power: string;
  powerstyle: string;
}

interface ModelStore {
  model: string;
  setModel: (model: string) => void;
  getModelType: () => string;
  modelList: modelListProps[];
}

interface SocketStore {
  WsToken: string;
  InputLenLimit: number;
  sendQuestion: ((content: string) => void) | undefined;
  setSendQuestion: (sendQuestion: (content: string) => void) => void;
  updateWsToken: (token: string) => void;
  updateInputLenLimit: (limit: number) => void;
  setTokenState: (token: string, limit: number) => void;
  resetSocketState: () => void;
}

interface ChatStateStore {
  currentSessionId: string;
  isLandingPage: boolean;
  setIsLandingPage: (isLandingPage: boolean) => void;
  getIsLandingPage: () => boolean;
  getCurrentSessionId: () => string;
  switchToSession: (sessionId: string) => void;
}
