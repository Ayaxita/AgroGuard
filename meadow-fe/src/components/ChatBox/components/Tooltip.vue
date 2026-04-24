<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    title: string;
    placement?: "top" | "bottom" | "left" | "right";
    fontSize?: string;
    fontColor?: string;
    bgColor?: string;
    padding?: string;
    shadow?: string;
    translateOffset?: string;
    noArrow?: boolean;
  }>(),
  {
    placement: "right",
    fontSize: "sm",
    fontColor: "text-black",
    bgColor: "bg-blue-500",
    padding: "p-2",
    shadow: "",
    translateOffset: "",
    noArrow: false
  }
);
</script>

<template>
  <div class="group relative w-fit">
    <div
      :class="[
        'pointer-events-none flex absolute opacity-0 rounded-sm duration-300 before:absolute before:block before:rotate-45 before:content-[\' \'] before:size-2 group-hover:opacity-100 group-hover:delay-300',
        padding,
        bgColor,
        shadow,
        noArrow ? 'before:hidden' : '',
        placement === 'top'
          ? 'bottom-full left-1/2 -translate-x-1/2 -translate-y-2 before:-bottom-[2px] before:left-1/2 before:-translate-x-1/2'
          : placement === 'bottom'
            ? 'top-full left-1/2 -translate-x-1/2 translate-y-2 before:-top-[2px] before:left-1/2 before:-translate-x-1/2'
            : placement === 'left'
              ? 'right-full top-1/2 -translate-y-1/2 -translate-x-2 before:-right-[2px] before:top-1/2 before:-translate-y-1/2'
              : 'left-full top-1/2 -translate-y-1/2 translate-x-2 before:-left-[2px] before:top-1/2 before:-translate-y-1/2',
        translateOffset,
        `before:${bgColor}`
      ]"
    >
      <span :class="[`text-nowrap ${fontColor} leading-none text-${fontSize}`]">
        {{ title }}
      </span>
    </div>
    <slot></slot>
  </div>
</template>
