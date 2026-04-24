<script setup lang="ts">
// 无需额外的props
</script>

<template>
  <button
    class="rounded-full bg-white bg-opacity-25 p-1 backdrop-blur-md duration-200 hover:bg-opacity-35 active:bg-white active:bg-opacity-50"
  >
    <span class="sr-only">minimize</span>
    <svg xmlns="http://www.w3.org/2000/svg" width="12px" height="12px" viewBox="0 0 24 24">
      <path fill="#0a0a0a" d="M6 13v-2h12v2z" stroke-width="2" stroke="#0a0a0a" />
    </svg>
  </button>
</template>
