<template>
  <button
    :class="[
      'flex flex-row items-center justify-between rounded-md border p-1 backdrop-blur-md duration-500',
      selected ? 'bg-gray-200' : 'hover:bg-gray-100 hover:bg-opacity-95'
    ]"
    v-bind="$attrs"
  >
    <span class="text-xs font-bold text-black">{{ name }}</span>
    <span :class="['rounded-md border px-[2px] text-[10px]', powerstyle || 'text-gray-500']">
      {{ power }}
    </span>
  </button>
</template>

<script setup lang="ts">
defineProps<{
  name?: string;
  power?: string;
  powerstyle?: string;
  selected?: boolean;
}>();
</script>
