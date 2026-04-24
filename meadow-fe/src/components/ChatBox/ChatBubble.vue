<script setup lang="ts">
import { useAppStateStore } from "@/components/ChatBox/stores/globalStore";
import { ref, watch } from "vue";
import "./style/index.css";

const chatBubbleRef = ref<HTMLImageElement>();
// 拖拽相关
const dragOffset = ref({ x: 0, y: 0 });
const isDragging = ref(false);

const handleDrag = (e: MouseEvent) => {
  if (!chatBubbleRef.value) return;
  // 记录初始位置和鼠标偏移
  const rect = chatBubbleRef.value.getBoundingClientRect();
  dragOffset.value = {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top
  };

  // 添加鼠标移动和释放事件监听
  document.addEventListener("mousemove", handleDragMove);
  document.addEventListener("mouseup", handleDragEnd);
};

const handleDragMove = (e: MouseEvent) => {
  if (!chatBubbleRef.value) return;
  isDragging.value = true;
  chatBubbleRef.value.style.left = `${e.clientX - dragOffset.value.x}px`;
  chatBubbleRef.value.style.top = `${e.clientY - dragOffset.value.y}px`;
};

const handleDragEnd = () => {
  // 移除事件监听
  if (!chatBubbleRef.value) return;
  const { left, top, width } = chatBubbleRef.value.getBoundingClientRect();
  const windowWidth = window.innerWidth;

  // 判断靠近哪边边缘
  const isNearLeft = left < windowWidth / 2;

  // 设置吸附位置
  chatBubbleRef.value.style.left = isNearLeft ? "5px" : `${windowWidth - width - 10}px`;
  chatBubbleRef.value.style.top = `${top}px`;
  chatBubbleRef.value.style.transition = "left 0.3s ease-out, top 0.3s ease-out";
  document.removeEventListener("mousemove", handleDragMove);
  document.removeEventListener("mouseup", handleDragEnd);
  setTimeout(() => {
    isDragging.value = false; // 拖拽结束后延迟重置标志
  }, 10);
  setTimeout(() => {
    if (!chatBubbleRef.value) return;
    chatBubbleRef.value.style.transition = "none";
  }, 300);
};
const appState = useAppStateStore();

const handleClick = (e: MouseEvent) => {
  if (isDragging.value) {
    e.preventDefault();
    e.stopPropagation();
    return;
  }
  chatBubbleRef.value?.classList.remove("bubble-appear");
  chatBubbleRef.value?.classList.remove("select-auto");
  chatBubbleRef.value?.classList.add("bubble-disappear");
  chatBubbleRef.value?.classList.add("select-none");

  appState.setIsChatboxShow(!appState.isChatboxShow);
};

watch(
  () => appState.isChatboxShow,
  () => {
    if (!appState.isChatboxShow) {
      chatBubbleRef.value?.classList.remove("bubble-disappear");
      chatBubbleRef.value?.classList.remove("select-none");
      chatBubbleRef.value?.classList.add("bubble-appear");
      chatBubbleRef.value?.classList.add("select-auto");
    }
  }
);
</script>

<template>
  <button
    ref="chatBubbleRef"
    className="chatbox-bubble absolute right-5 bottom-10 z-50 size-14 rounded-full overflow-hidden cursor-pointer active:cursor-grabbing"
    @mousedown="handleDrag"
    @click="handleClick"
  ></button>
</template>

<style scoped>
.chatbox-bubble {
  background-image: url("/chatbox/4.png");
  background-repeat: no-repeat; /* 防止重复 */
  background-position: center; /* 居中显示 */
  background-size: contain; /* 确保图片完整显示 */
}

/* 出现动画 */
.bubble-appear {
  animation: bubble-appear 0.1s ease-out forwards;
}

@keyframes bubble-appear {
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
.bubble-disappear {
  animation: bubble-disappear 0.1s ease-in forwards;
}

@keyframes bubble-disappear {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.5);
  }
}
</style>
