<template>
  <button class="rounded-md p-1 backdrop-blur-md duration-500 hover:bg-black hover:bg-opacity-10" v-bind="$attrs">
    <span class="sr-only">Send</span>
    <PaperAirplaneIcon class="w-4" :style="{ opacity: iconOpacity }" stroke="black" />
  </button>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { PaperAirplaneIcon } from "@heroicons/vue/24/outline";

const props = defineProps<{
  inputValue?: boolean;
}>();

const iconOpacity = computed(() => (props.inputValue ? 1 : 0.25));
</script>
