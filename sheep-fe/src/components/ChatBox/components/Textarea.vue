<template>
  <textarea
    ref="textareaRef"
    v-bind="$attrs"
    :value="modelValue"
    className="max-h-[10.5rem] min-h-[1.75rem] w-full resize-none overflow-y-auto rounded-md p-2 text-sm text-black focus:border-none focus:outline-none"
    @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
  ></textarea>
</template>

<script setup lang="ts">
import { onUpdated, ref } from "vue";

defineProps<{
  modelValue: string;
}>();

defineEmits<{
  "update:modelValue": [value: string];
}>();

const textareaRef = ref<HTMLTextAreaElement>();

const updateHeight = () => {
  const textarea = textareaRef.value;
  if (!textarea) return;

  textarea.style.height = "auto";
  const newHeight = Math.min(
    textarea.scrollHeight,
    7 * 24 // 7行高度
  );
  textarea.style.height = `${newHeight}px`;
};

onUpdated(() => {
  updateHeight();
});
</script>
