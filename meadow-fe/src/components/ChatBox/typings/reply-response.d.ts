interface ReplyExtraInfo {
  e_charts_info: null;
}

interface ReplyKnowledge {
  id: string;
  type: 1 | 2;
}

interface ReplyQuoteInfo {
  index: number;
  position: number;
}

interface ReplyPayload {
  can_feedback: boolean;
  can_rating: boolean;
  content: string;
  docs: null;
  extra_info: ReplyExtraInfo;
  file_infos: null;
  from_avatar: string;
  from_name: string;
  intent_category: string;
  is_evil: boolean;
  is_final: boolean;
  is_from_self: boolean;
  is_llm_generated: boolean;
  knowledge: ReplyKnowledge[] | [];
  option_cards: string[] | [];
  quote_infos: ReplyQuoteInfo[] | null;
  record_id: string;
  related_record_id: string;
  reply_method: number;
  request_id: string;
  session_id: string;
  timestamp: number;
  trace_id: string;
}

interface ReplyData {
  type: "reply";
  payload: ReplyPayload;
  message_id: string;
}

type ReplyResponse = ["reply", ReplyData];

export { ReplyData, ReplyPayload, ReplyResponse, ReplyExtraInfo, ReplyKnowledge, ReplyQuoteInfo };
