<script setup lang="ts">
import { ref } from "vue";
import Tooltip from "./Tooltip.vue";
import { useChatStateStore } from "../stores/chatStore";
import NewChatButton from "./buttons/NewChatButton.vue";
import ChatHistoriesButton from "./buttons/ChatHistoriesButton.vue";
import ChatHistories from "./ChatHistories.vue";

const isChatSwitching = ref(false);
const chatStateStore = useChatStateStore();

const setIsChatSwitching = (value: boolean) => {
  isChatSwitching.value = value;
};

const setIsLandingPage = (value: boolean) => {
  chatStateStore.setIsLandingPage(value);
};
</script>

<template>
  <div className="header grid grid-cols-3 grid-rows-1 bg-gradient-to-r from-teal-300 to-teal-600 p-2 pt-7">
    <div className="col-start-2 flex items-center justify-center">
      <div className="flex flex-row items-center justify-center">
        <div className="whitespace-nowrap text-base text-white/90">病虫害监测助手</div>
      </div>
    </div>
    <div className="flex flex-1 flex-row justify-end gap-1">
      <Tooltip title="新建会话" placement="bottom" shadow="shadow-md " font-size="xs" padding="px-[5px] py-1.5" :no-arrow="true">
        <NewChatButton @click="setIsLandingPage(true)" />
      </Tooltip>
      <Tooltip
        title="会话历史"
        placement="bottom"
        shadow="shadow-md"
        font-size="xs"
        padding="px-[5px] py-1.5"
        translate-offset="-translate-x-11"
        :no-arrow="true"
      >
        <ChatHistoriesButton @click="setIsChatSwitching(true)" />
      </Tooltip>
    </div>
  </div>
  <div
    v-if="isChatSwitching"
    className="absolute left-0 top-0 z-20 h-full w-full bg-gray-500 bg-opacity-50"
    @click="setIsChatSwitching(false)"
  ></div>
  <ChatHistories v-if="isChatSwitching" :set-is-chat-switching="setIsChatSwitching" />
</template>
