<script setup lang="ts">
// 无需额外的props
</script>

<template>
  <button
    class="cursor-grab rounded-full px-3 py-2 bg-opacity duration-200 hover:bg-white hover:bg-opacity-25 hover:backdrop-blur-md active:cursor-grabbing active:bg-white active:bg-opacity-50"
  >
    <span class="sr-only">drag</span>
    <span class="block h-[3px] w-12 bg-blue-500" />
  </button>
</template>
