<template>
  <button class="rounded-md p-1 duration-500 hover:bg-white hover:bg-opacity-10 hover:backdrop-blur-md" v-bind="$attrs">
    <span class="sr-only">NewChat</span>
    <PlusIcon class="w-4 stroke-slate-700 stroke-2" />
  </button>
</template>

<script setup lang="ts">
import { PlusIcon } from "@heroicons/vue/24/outline";
</script>
