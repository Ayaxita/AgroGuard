<script setup lang="ts">
import { useChatNotificationStore } from "../../stores/chatStore";
import "./index.css";
import ErrMsgPopup from "./NotificationPopup.vue";

const chatNotificationStore = useChatNotificationStore();
</script>

<template>
  <ErrMsgPopup v-for="notification in chatNotificationStore.notifications" :key="notification.id" :notification="notification" />
</template>
