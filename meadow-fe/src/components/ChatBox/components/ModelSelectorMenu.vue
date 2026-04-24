<template>
  <div class="absolute bottom-full right-0 z-50 w-52 rounded-md border border-gray-300 bg-white p-2 shadow-lg">
    <div class="flex flex-col gap-1">
      <p class="text-[10px] font-bold text-black">选择模型</p>
      <ModelButton
        v-for="item in modelList"
        :key="item.name"
        :name="item.name"
        :power="item.power"
        :powerstyle="item.powerstyle"
        :selected="item.name === modelType"
        @click="handleSelect(item.name)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ModelButton from "./ModelButton.vue";
import { useModelStore } from "../stores/chatStore";

const props = defineProps<{
  onClose: () => void;
}>();

const { modelType, modelList, setModelType } = useModelStore();

const handleSelect = (modelName: string) => {
  setModelType(modelName);
  props.onClose();
};
</script>
