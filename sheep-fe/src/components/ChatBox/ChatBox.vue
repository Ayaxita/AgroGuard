<script setup lang="ts">
import { ref, watch } from "vue";
import { useChatbox } from "./hooks/useChatbox";
import HeaderUtils from "./components/HeaderUtils.vue";
import CommonHeader from "./components/CommonHeader.vue";
import WelcomingPage from "./components/WelcomingPage.vue";
import ClientChat from "./components/ClientChat.vue";
import QuestionInput from "./components/QuestionInput.vue";
import { useChatStateStore } from "./stores/chatStore";
import Notifications from "./components/err-msg/Notifications.vue";
import { useAppStateStore } from "@/components/ChatBox/stores/globalStore";

// 获取相关store
const chatStateStore = useChatStateStore();

// 初始化聊天功能
const { sendQuestion } = useChatbox();

// wrapper引用
const wrapperRef = ref<HTMLDivElement | null>(null);

const appState = useAppStateStore();
const isShow = ref(false);
watch(
  () => appState.isChatboxShow,
  () => {
    if (appState.isChatboxShow) {
      isShow.value = true;
    } else {
      wrapperRef.value?.classList.toggle("chatbox-appear");
      wrapperRef.value?.classList.toggle("chatbox-disappear");
      setTimeout(() => {
        isShow.value = false;
        appState.setIsChatboxShow(false);
      }, 300);
    }
  }
);
</script>

<template>
  <div
    class="chatbox-appear opacity-1 absolute right-20 top-20 z-50 h-[600px] min-h-[600px] w-[350px] min-w-[350px] p-2"
    ref="wrapperRef"
    v-if="isShow"
  >
    <div class="wrapper relative flex h-full w-full flex-col overflow-hidden rounded-md bg-white shadow-md">
      <!-- 组件内容 -->
      <HeaderUtils :wrapper-ref="wrapperRef" />
      <CommonHeader />
      <WelcomingPage v-if="chatStateStore.isLandingPage" />
      <ClientChat v-else />
      <!-- 输入区域 -->
      <QuestionInput :send-question="sendQuestion" />
      <Notifications />
    </div>
  </div>
</template>

<style scoped>
/* 出现动画 */
.chatbox-appear {
  animation: chatbox-appear 0.1s ease-out forwards;
}

@keyframes chatbox-appear {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 消失动画 */
.chatbox-disappear {
  animation: chatbox-disappear 0.1s ease-in forwards;
}

@keyframes chatbox-disappear {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.5);
  }
}

/* 自定义滚动条样式 */
:deep(*::-webkit-scrollbar) {
  width: 6px;
  height: 6px;
}

/* ::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
} */
:deep(*::-webkit-scrollbar-thumb) {
  background: rgb(0 0 0 / 10%);
  border-radius: 4px;
}
:deep(*::-webkit-scrollbar-thumb:hover) {
  cursor: pointer;
  background: rgb(0 0 0 / 20%);
}
</style>
