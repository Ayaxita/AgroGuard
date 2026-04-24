<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from "vue";
import SendButton from "./buttons/SendButton.vue";
import QuoteButton from "./buttons/QuoteButton.vue";
import Tooltip from "./Tooltip.vue";
import { useModelStore, useChatStateStore, useSocketStore, useChatNotificationStore } from "../stores/chatStore";
import ModelSelectorMenu from "./ModelSelectorMenu.vue";
import ModelSelectorButton from "./ModelSelectorButton.vue";
import Textarea from "./Textarea.vue";

const props = defineProps<{
  sendQuestion: (question: string) => void;
}>();

const chatStateStore = useChatStateStore();
const chatNotificationStore = useChatNotificationStore();

const inputVal = ref<string>("");

// 是否展示错误信息
const showErr = ref<boolean>(false);
// 错误提示
const errMsg = ref<string>("");

// 处理错误
const handleError = (msg: string) => {
  errMsg.value = msg;
  showErr.value = true;
  setTimeout(() => {
    showErr.value = false;
  }, 2000);
};

// 发送问题
const handleSend = async () => {
  if (!inputVal.value.trim()) {
    handleError("请输入问题后再发送");
    return;
  }
  props.sendQuestion(inputVal.value);
  inputVal.value = "";
};

// 监听回车，按下回车键发送
const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
};

const handleQuoteClick = () => {
  chatNotificationStore.addNotification({
    type: "info",
    message: "该功能开发中..."
  });
};
// 模型选择

const modelStore = useModelStore();
const isModelSwitching = ref(false);
</script>

<template>
  <div className="question-input w-full p-3">
    <div className="flex flex-col rounded-md border border-gray-300 focus-within:border-blue-500">
      <Textarea
        name="question-input"
        id="1"
        rows="1"
        placeholder="输入消息"
        v-model="inputVal"
        @keydown="handleKeydown"
      ></Textarea>
      <div className="relative flex w-full justify-between p-1">
        <div className="flex">
          <Tooltip
            title="引用信息"
            placement="top"
            shadow="shadow-md"
            font-size="xs"
            padding="px-[5px] py-1.5"
            translate-offset="-translate-x-7"
            :no-arrow="true"
          >
            <QuoteButton @click="handleQuoteClick" />
          </Tooltip>
        </div>
        <div className="flex items-center justify-center gap-1">
          <div>
            <ModelSelectorMenu
              v-if="isModelSwitching"
              :on-close="
                () => {
                  isModelSwitching = false;
                }
              "
            />
            <ModelSelectorButton @click="isModelSwitching = true">
              {{ modelStore.modelType }}
            </ModelSelectorButton>
          </div>
          <Tooltip
            title="发送↩"
            placement="top"
            shadow="shadow-md"
            font-size="xs"
            padding="px-[5px] py-1.5"
            translate-offset="-translate-x-7"
            :no-arrow="true"
          >
            <SendButton :input-value="!!inputVal" @click="handleSend" />
          </Tooltip>
        </div>
      </div>
    </div>
  </div>
  <div v-if="isModelSwitching" className="absolute left-0 top-0 z-20 h-full w-full" @click="isModelSwitching = false"></div>
</template>

<style scoped></style>
