<template>
  <div ref="chartEl" :style="{ height }"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import * as echarts from "echarts";

const props = defineProps({
  chartData: Object,
  title: String,
  color: String,
  height: {
    type: String,
    default: "100%"
  }
});

const chartEl = ref(null);
let chartInstance = null;

const initChart = () => {
  chartInstance = echarts.init(chartEl.value);

  const option = {
    title: {
      text: props.title,
      left: "center",
      textStyle: {
        fontSize: 14,
        color: "#666"
      }
    },
    tooltip: {
      trigger: "axis"
    },
    xAxis: {
      type: "category",
      data: props.chartData.xData
    },
    yAxis: {
      type: "value",
      axisLabel: {
        formatter: "¥{value}"
      }
    },
    series: [
      {
        data: props.chartData.series,
        type: "line",
        smooth: true,
        lineStyle: {
          color: props.color,
          width: 2
        },
        areaStyle: {
          color: echarts.color.lift(props.color, 0.8)
        }
      }
    ]
  };

  chartInstance.setOption(option);
};

onMounted(() => {
  initChart();
  window.addEventListener("resize", () => chartInstance.resize());
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", () => chartInstance.resize());
  chartInstance.dispose();
});

watch(
  () => props.chartData,
  () => {
    chartInstance.setOption({
      xAxis: { data: props.chartData.xData },
      series: [{ data: props.chartData.series }]
    });
  },
  { deep: true }
);
</script>
