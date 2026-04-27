<template>
  <div
    class="absolute left-1/2 top-16 z-50 flex max-h-[400px] w-11/12 -translate-x-1/2 flex-col rounded-md border bg-white shadow-md"
  >
    <div class="flex flex-row justify-between p-3">
      <span class="flex items-center font-bold leading-none text-black"> 历史会话 </span>
      <HistoryCloseButton @click="setIsChatSwitching(false)" />
    </div>
    <div class="flex flex-col gap-1 p-2">
      <template v-if="!hasHistory">
        <div class="flex h-40 flex-row items-center justify-center">
          <div class="flex flex-col items-center gap-1">
            <ChatBubbleLeftIcon class="h-7 w-7 stroke-1 text-gray-500" />
            <span class="text-sm text-gray-500">没有历史会话</span>
          </div>
        </div>
      </template>
      <template v-else>
        <template v-for="timeGroup in timeGroupedChats" :key="timeGroup.title">
          <!-- 时间分组标题 -->
          <div v-if="timeGroup.chats.length > 0" class="flex flex-row px-1 text-xs text-black text-opacity-50">
            {{ timeGroup.title }}
          </div>
          <!-- 聊天记录按钮 -->
          <div
            v-for="chat in timeGroup.chats"
            :key="chat.sessionId"
            :class="[
              'flex cursor-pointer flex-row justify-between rounded-md p-1.5',
              chat.sessionId === currentSessionId ? 'bg-gray-300 bg-opacity-95' : 'hover:bg-gray-100 hover:bg-opacity-95'
            ]"
            @click="switchChat(chat.sessionId)"
          >
            <div class="flex min-w-0 flex-1 flex-row items-center gap-1">
              <ChatBubbleLeftIcon class="h-4 w-4 shrink-0 stroke-1 text-black" />
              <p class="truncate text-[13px] text-black">
                {{ chat.chatContent[0]?.content }}
              </p>
            </div>
            <button class="shrink-0" @click.stop="deleteChat(chat.sessionId)">
              <TrashIcon class="h-4 w-4 stroke-1 text-red-500" />
            </button>
          </div>
        </template>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { ChatBubbleLeftIcon, TrashIcon } from "@heroicons/vue/24/outline";
import HistoryCloseButton from "./buttons/HistoryCloseButton.vue";
import { useChatMsgStore, useChatStateStore } from "../stores/chatStore";
import dayjs from "dayjs";

const props = defineProps<{
  setIsChatSwitching: (value: boolean) => void;
}>();

const chatMsgStore = useChatMsgStore();
const chatStateStore = useChatStateStore();

const hasHistory = computed(() => chatMsgStore.chatHistory.some(item => item.chatContent.length !== 0));

const currentSessionId = computed(() => chatStateStore.currentSessionId);

// 按时间分组的聊天记录
const timeGroupedChats = computed(() => {
  const groups = [
    { title: "今天", chats: [] },
    { title: "一天以前", chats: [] },
    { title: "一周以前", chats: [] },
    { title: "一个月以前", chats: [] },
    { title: "一年以前", chats: [] }
  ];

  chatMsgStore.chatHistory.forEach(item => {
    if (!item.chatContent.length) return;

    const timestamp = item.chatContent[0].timestamp;
    const diff = dayjs(timestamp).diff(dayjs(), "year");

    if (diff >= 1) {
      groups.find(g => g.title === "一年以前")?.chats.push(item);
    } else if (dayjs(timestamp).diff(dayjs(), "month") >= 1) {
      groups.find(g => g.title === "一个月以前")?.chats.push(item);
    } else if (dayjs(timestamp).diff(dayjs(), "week") >= 1) {
      groups.find(g => g.title === "一周以前")?.chats.push(item);
    } else if (dayjs(timestamp).diff(dayjs(), "day") >= 1) {
      groups.find(g => g.title === "一天以前")?.chats.push(item);
    } else {
      groups.find(g => g.title === "今天")?.chats.push(item);
    }
  });

  return groups;
});

// 切换到指定会话
const switchChat = (sessionId: string) => {
  chatStateStore.setCurrentSessionId(sessionId);
  chatStateStore.setIsLandingPage(false);
  props.setIsChatSwitching(false);
};

// 删除会话
const deleteChat = (sessionId: string) => {
  chatMsgStore.deleteChatHistory(sessionId);
};
</script>
