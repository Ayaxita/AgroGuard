<script setup lang="ts">
import { ref } from "vue";
import QrcodeVue from "qrcode.vue";
import type { Level, RenderAs } from "qrcode.vue";
import { useRoute, useRouter } from "vue-router";
import QRCode from "qrcode";
const router = useRouter();
const route = useRoute();
// const href = router.resolve(`/basic/basicinfo/detail?ele_num=${route.query.ele_num}`);
// console.log(href);
const href = window.location.origin + `/#/basic/basicinfo/detail?ele_num=${route.query.ele_num}`;
const src = ref();
QRCode.toDataURL(href)
  .then(url => {
    console.log(url);
    src.value = url;
  })
  .catch(err => {
    console.error(err);
  });
const value = ref<any>(href);
const level = ref<Level>("M");
const renderAs = ref<RenderAs>("svg");
</script>
<template>
  <main>
    <!-- <qrcode-vue :value="value" :level="level" :render-as="renderAs" /> -->
    <img :src="src" alt="" />
  </main>
</template>
<style scoped>
main {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
</style>
