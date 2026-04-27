<script setup lang="ts">
// @ts-nocheck
import { ref, computed, watch } from "vue";
import { useChatMsgStore, useChatStateStore } from "../stores/chatStore";
import { MsgContent, MsgThought } from "lke-component-vue3";
import "lke-component-vue3/style.css";

import dayjs from "dayjs";

const chatMsgStore = useChatMsgStore();
const chatStateStore = useChatStateStore();

// 获取当前会话的消息列表
const messageList = computed(() => {
  return chatMsgStore.chatHistory.find(item => item.sessionId === chatStateStore.currentSessionId).chatContent;
});

// 内容DOM引用
const contentDomRef = ref<HTMLDivElement | null>(null);

// 滚动到底部
const scrollToBottom = (element: HTMLElement, targetY: number) => {
  element.scrollTo({
    top: targetY,
    behavior: "smooth"
  });
};

// 监听消息列表变化，自动滚动到底部
watch(
  messageList,
  () => {
    if (!contentDomRef.value) return;

    const lastItem = messageList.value[messageList.value.length - 1];
    if (lastItem && lastItem.role === "user") {
      scrollToBottom(contentDomRef.value, contentDomRef.value.scrollHeight);
    }

    const scrollHeight = contentDomRef.value.scrollHeight;
    const clientHeight = contentDomRef.value.clientHeight;
    const scrollTop = contentDomRef.value.scrollTop;

    if (scrollHeight - clientHeight - scrollTop < 100) {
      scrollToBottom(contentDomRef.value, scrollHeight);
    }
  },
  { deep: true }
);

// 是否显示时间戳
const shouldShowTimestamp = (item: UserChatContent, index: number) => {
  if (index === 0) return true;

  return dayjs(item.timestamp).diff(dayjs(messageList.value[index - 1].timestamp), "minute") > 5;
};

// 更新思考状态
const handleThoughtTitleClick = (detailVisible: boolean, requestId: string, thoughtIndex: number) => {
  chatMsgStore.updateThoughts(requestId, { is_final: detailVisible ? false : true }, thoughtIndex);
};
</script>

<template>
  <div ref="contentDomRef" class="content h-full w-full overflow-y-scroll px-3">
    <!-- 用户消息 -->
    <div v-for="(item, index) in messageList" :key="item.recordId || index" class="mb-4">
      <!-- 用户消息 -->
      <template v-if="item.role === 'user'">
        <div v-if="shouldShowTimestamp(item, index)" class="time-tick m-4 text-center text-xs font-thin text-gray-400">
          {{ dayjs(item.timestamp).format("HH:mm") }}
        </div>
        <div class="user-question flex w-full flex-row justify-end">
          <div class="ml-11 flex flex-row items-center">
            <img
              v-if="!item.isFinal"
              src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAABYlAAAWJQFJUiTwAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAUUSURBVHgBvVfPb1RVFD7n3Ptep53+nmkrpYWBltIIBREXYkHHuCAYWWhk6YIVMTFG/w0XLtzpxpUxhgQ2GhMhZCCiEGICtUFbKk5/2bR0psx0Zjrz3rv3eu5gtSml1PQNX3rzXue+Oee873znnDsI28TAweNXkHDIANwHg7f5elUV3e/u37+c28r3EbaJ/qETrxGYS2xK8b8BL8VGNQfylTL4yR+j16ahlgFY7Bs6fgkRh0GDYosKjAkAUVcDQvOFLvmfTkzczG/0XQEhoCvWc82QmOTbskHoQ2Dn1QCMNgZfEI443da844dsdvaxIEJhYC36+081U13hTbb8Ma9um45qMMZMaoPv3xu99tumARgOmWFgm+g7+GqvQPMR23ub7TEToBFhGj393tjY9b+eFACZRxFsO4BV7Dt0/EN2/QGCUYZTQ4gz4Kl3OYhlu/+fBs6cEcnOTjp71qYyBWEhOz91M96VsIJ8iapM6KgRwskuTP60NgBMlDrdQmEG9+yZxHPnzplUKhUaC5mFyVvtHbsaDZiDSMR2zYFoW++3+cz0cjWARCIZWWnOis6GPszlZuHChQsKQkZHe+8ISnqHRSa5Sowj0WQWpm7YADCRSDTGI+2Yd3N4706bB5DWEDIymWkv1rXbYXdHDBprf5eI771IXDau51WoVFoWlaLDAaVCf/tVSCW+5kp4iAZtt4w0C/8EsUzqKhLlYmVFyEK9jSy03K/H3bupAveE32235LJU/LaHiajedZ0m0SabZEuLCKDG0FpdZR0o2xtYCwmJUd9VASE4BLmcqhn9qyCD84YgYAb4DzrIKxtHEMjAr4QyF54GnyjPb28Z4GEJ9VJKElIgBLz8YCX02bAeiGTTz6k2SCwGyZ0Ji0WfRzpgsQEkPANozePadnwSRQoCV1kWBK8OqLhQYzgYJFh8imwKDMyRW1fxdeCzfxK+EK1QYyhlBqvOefFs+pPKWpSEIKFUIFihjWd4KEGNMDCQjLMIjnABKJ63XHE4SlODO/J2AiuuBB+0e2d85jmoEQLpD7Jjm/+AK0AVF0u3CM6fVzISWRKEwi4IsDuZTIYuxsHBN2JC4GkQdiQzA1qn5uZ+KZHd9HLOvDaCtCYBEutmFr3dEDK067/Fl1bbBVlumpR/0X5ezXc2O6FinT0u9+UWweXJ2WiNte3CTGbyIYSAgaHhU3xJ2t6H1qVRl8fu3rhl92j1oZ0xOcW68DythMJAakf19z2f7Idtov/wiZOI4iQLzp6QNWvgwfjo9W9W9/9VfDqd1s31ezNu1HQRUh2PTcEr3h7fE62TsXyhMOfD/4A95MR39pxiI6/b0yCXnX3bLAWVzxYXZ1dWn3us9cb3Dze1uvQit8kod0nioyzLBsrSEWNLOvtgfmSkuLnjREQ29rzMiRxGrRrYMWsbhVYmh9L9cvzOldm1z2/Y+3uOHatvKMpXmK5GViwTgoI7NstDCSI5p3w97xtYimhmlDfcJowEHrUqoP08UrqZ6wbLLg8cwfvMMuXKoD+f+vXHpfW+njh8jh496hS96CD3h31cHtUA0M4OqjLy6B4NO/jnnsuIm7u0TpXiTiv4np0z+T97y86VdDpV3sjPU6df16FD0Zag5QA767OOwDLCk0Oz8Sq1GriLg7ABGKsbw29N1eE6UkZxM307tWklbXn8WkbyXn0vd/FuEBTnHxst7KrBBsXHGJ8lVmRriwF4M7TSOj4x8X1lK3b/BqtpRMYSS0peAAAAAElFTkSuQmCC"
              alt="loading-icon"
              class="mr-2 size-4 animate-spin rounded-full"
            />
            <div class="rounded-md bg-blue-100 p-3">
              <p class="break-all text-sm text-black whitespace-pre-wrap">
                {{ item.content }}
              </p>
            </div>
          </div>
        </div>
      </template>

      <!-- 机器人消息 -->
      <template
        v-else-if="
          item.role === 'assistant' && (item.content !== '' || (item.thoughts && !item.thoughts.some(t => t.content === '')))
        "
      >
        <div class="qbot-answer flex w-full flex-row">
          <img src="/chatbox/deepseek-icon.png" alt="deepseek-icon" class="mr-2 mt-1 h-8 w-8 rounded-full" />
          <div class="flex flex-col">
            <span class="p-1 text-xs text-gray-400">{{ item.modelType }}</span>
            <div class="rounded-md w-fit bg-gray-100 p-3">
              <div class="qbot-ans-main">
                <!-- 思考内容 -->
                <template v-if="item.thoughts">
                  <div class="pb-3" v-for="thought in item.thoughts" :key="thought.index">
                    <MsgThought
                      :content="thought.content"
                      :title="thought.title"
                      :title-icon="thought.icon"
                      :node-name="thought.node_name"
                      :status="thought.status"
                      :elapsed="thought.elapsed"
                    />
                  </div>
                </template>

                <!-- 回复内容 -->
                <div class="text-sm text-black">
                  <MsgContent
                    :key="item.recordId"
                    :content="item.content"
                    :is-final="item.isFinal"
                    :style-obj="{}"
                    :clazz-table="item.clazzTable"
                    :line-numbers="false"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
