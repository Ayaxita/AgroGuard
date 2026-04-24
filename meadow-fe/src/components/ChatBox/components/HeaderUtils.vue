<!-- eslint-disable vue/no-mutating-props -->
<script setup lang="ts">
import { ref, watch } from "vue";
import NarrowButton from "./buttons/NarrowButton.vue";
import MinimizeButton from "./buttons/MinimizeButton.vue";
import DragButton from "./buttons/DragButton.vue";
import CloseButton from "./buttons/CloseButton.vue";
import { useAppStateStore } from "@/components/ChatBox/stores/globalStore";

const props = defineProps<{
  wrapperRef: HTMLElement | null;
}>();

// 拖拽相关
const dragOffset = ref({ x: 0, y: 0 });

const handleDrag = (e: MouseEvent) => {
  if (!props.wrapperRef) return;
  // 记录初始位置和鼠标偏移
  const rect = props.wrapperRef.getBoundingClientRect();
  dragOffset.value = {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top
  };

  // 添加鼠标移动和释放事件监听
  document.addEventListener("mousemove", handleDragMove);
  document.addEventListener("mouseup", handleDragEnd);
};

const handleDragMove = (e: MouseEvent) => {
  if (!props.wrapperRef) return;
  props.wrapperRef.style.userSelect = "none";
  props.wrapperRef.style.left = `${e.clientX - dragOffset.value.x}px`;
  props.wrapperRef.style.top = `${e.clientY - dragOffset.value.y}px`;
};

const handleDragEnd = () => {
  // 移除事件监听
  if (!props.wrapperRef) return;
  props.wrapperRef.style.userSelect = "auto";

  document.removeEventListener("mousemove", handleDragMove);
  document.removeEventListener("mouseup", handleDragEnd);
};

const appState = useAppStateStore();
// 关闭窗口
const handleCloseClick = () => {
  if (!props.wrapperRef) return;

  appState.setIsChatboxShow(false);
};

// 最小化窗口
const handleMinimizeClick = () => {
  if (!props.wrapperRef) return;
  props.wrapperRef.style.transition = "all 0.2s ease-in-out";
  props.wrapperRef.style.width = "350px";
  props.wrapperRef.style.height = "600px";
  setTimeout(() => {
    if (!props.wrapperRef) return;
    props.wrapperRef.style.transition = "none";
  }, 200);
};

// 窗口调整大小相关
const isResizing = ref(false);
const direction = ref("");
const initialSize = ref({ width: 0, height: 0 });
const initialPosition = ref({ x: 0, y: 0 });
const dragingStyle = ref(["outline outline-2 outline-blue-500 duration-100", "outline outline-0 duration-100"]);

// 处理窗口调整大小
watch(
  () => props.wrapperRef,
  (newVal, oldVal, onCleanup) => {
    if (!props.wrapperRef) return;
    const element = props.wrapperRef;
    const edgeSize = 15; // 边缘检测范围(px)

    const handleMouseMove = (e: MouseEvent) => {
      if (!props.wrapperRef) return;
      props.wrapperRef.style.userSelect = "none";

      if (isResizing.value) {
        // 处理resize逻辑
        const { width, height } = initialSize.value;
        const { x, y } = initialPosition.value;

        if (direction.value.includes("e")) {
          props.wrapperRef.style.width = `${width + (e.clientX - x)}px`;
        }
        if (direction.value.includes("s")) {
          props.wrapperRef.style.height = `${height + (e.clientY - y)}px`;
        }
      } else {
        props.wrapperRef.style.userSelect = "auto";

        // 检测鼠标是否在边缘
        const rect = element.getBoundingClientRect();
        const isNearRight = e.clientX > rect.right - edgeSize && e.clientX < rect.right;
        const isNearBottom = e.clientY > rect.bottom - edgeSize && e.clientY < rect.bottom;

        if (isNearRight && isNearBottom) {
          element.style.cursor = "se-resize";
          direction.value = "se";
        } else if (isNearRight) {
          element.style.cursor = "e-resize";
          direction.value = "e";
        } else if (isNearBottom) {
          element.style.cursor = "s-resize";
          direction.value = "s";
        } else {
          element.style.cursor = "";
          direction.value = "";
        }
      }
    };

    const handleMouseDown = (e: MouseEvent) => {
      if (direction.value && props.wrapperRef) {
        props.wrapperRef.firstElementChild?.classList.remove(...dragingStyle.value[1].split(" "));
        props.wrapperRef.firstElementChild?.classList.add(...dragingStyle.value[0].split(" "));
        isResizing.value = true;
        initialSize.value = {
          width: props.wrapperRef.offsetWidth,
          height: props.wrapperRef.offsetHeight
        };
        initialPosition.value = { x: e.clientX, y: e.clientY };
      }
    };

    const handleMouseUp = () => {
      if (direction.value && props.wrapperRef) {
        props.wrapperRef.firstElementChild?.classList.remove(...dragingStyle.value[0].split(" "));
        props.wrapperRef.firstElementChild?.classList.add(...dragingStyle.value[1].split(" "));
        isResizing.value = false;
      }
    };

    window.addEventListener("mousemove", handleMouseMove);
    element.addEventListener("mousedown", handleMouseDown);
    document.addEventListener("mouseup", handleMouseUp);
    onCleanup(() => {
      window.removeEventListener("mousemove", handleMouseMove);
      element.removeEventListener("mousedown", handleMouseDown);
      document.removeEventListener("mouseup", handleMouseUp);
    });
  }
);

const emit = defineEmits(["close"]);
</script>

<template>
  <div className="header-utils absolute left-0 top-0 grid w-full grid-cols-3 grid-rows-1 bg-transparent px-1 pt-1">
    <div className="grid grid-cols-2 grid-rows-1">
      <div>
        <NarrowButton @click="handleMinimizeClick" />
      </div>
      <div>
        <MinimizeButton />
      </div>
    </div>
    <div className="flex flex-row justify-center justify-self-center">
      <DragButton @mousedown="handleDrag" />
    </div>
    <div className="justify-self-end">
      <CloseButton @click="handleCloseClick" />
    </div>
  </div>
</template>
