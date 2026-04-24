<script setup lang="ts">
import { ref, onMounted } from "vue";
import { XCircleIcon } from "@heroicons/vue/24/solid";
import { useChatNotificationStore } from "../../stores/chatStore";
import "./index.css";

interface ChatNotification {
  id: number;
  type: "error" | "info" | "success" | "warning";
  message: string;
}
interface Props {
  notification: ChatNotification;
}

const props = defineProps<Props>();
const chatNotificationStore = useChatNotificationStore();
const isShow = ref(true);

const getNotificationClass = (type: string) => {
  const baseClass =
    "absolute left-1/2 top-8 z-50 flex max-w-[70%] items-center rounded-md px-4 py-3 text-sm leading-none shadow-md";

  const typeClasses = {
    error: "border-red-100 bg-red-50 text-red-500",
    info: "border-blue-100 bg-blue-50 text-blue-500",
    success: "border-green-100 bg-green-50 text-green-500",
    warning: "border-yellow-100 bg-yellow-50 text-yellow-500"
  };

  const animationClass = isShow.value ? "errMsgShow" : "errMsgClose";

  return `${baseClass} ${typeClasses[type]} ${animationClass}`;
};

const closeNotification = (notificationId: number) => {
  isShow.value = false;
  setTimeout(() => {
    chatNotificationStore.shiftNotification(notificationId);
  }, 300);
};

onMounted(() => {
  setTimeout(() => {
    closeNotification(props.notification.id);
  }, 3000);
});
</script>

<template>
  <div :class="getNotificationClass(props.notification.type)">
    <XCircleIcon class="mr-1 w-4 h-4 shrink-0" />
    <p class="min-w-0">{{ props.notification.message }}</p>
  </div>
</template>
