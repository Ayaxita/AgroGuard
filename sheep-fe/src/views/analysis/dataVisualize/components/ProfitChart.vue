<template>
  <div ref="chartContainer" class="chart-container"></div>
</template>

<script>
import * as echarts from "echarts";

export default {
  name: "LargeAreaChart",
  data() {
    return {
      chart: null
    };
  },
  mounted() {
    this.initChart();
    window.addEventListener("resize", this.handleResize);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.handleResize);
    if (this.chart) {
      this.chart.dispose();
    }
  },
  methods: {
    initChart() {
      // 初始化 echarts 实例
      this.chart = echarts.init(this.$refs.chartContainer);

      // 生成数据
      let base = +new Date(1988, 9, 3);
      const oneDay = 24 * 3600 * 1000;
      const data = [[base, Math.random() * 300]];
      for (let i = 1; i < 20000; i++) {
        let now = new Date((base += oneDay));
        data.push([+now, Math.round((Math.random() - 0.5) * 20 + data[i - 1][1])]);
      }

      // 配置项
      const option = {
        tooltip: {
          trigger: "axis",
          position: function (pt) {
            return [pt[0], "10%"];
          }
        },
        title: {
          left: "center",
          text: "Large Area Chart"
        },
        toolbox: {
          feature: {
            dataZoom: {
              yAxisIndex: "none"
            },
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: "time",
          boundaryGap: false
        },
        yAxis: {
          type: "value",
          boundaryGap: [0, "100%"]
        },
        dataZoom: [
          {
            type: "inside",
            start: 0,
            end: 20
          },
          {
            start: 0,
            end: 20
          }
        ],
        series: [
          {
            name: "Fake Data",
            type: "line",
            smooth: true,
            symbol: "none",
            areaStyle: {},
            data: data
          }
        ]
      };

      // 设置配置项
      this.chart.setOption(option);
    },
    handleResize() {
      if (this.chart) {
        this.chart.resize();
      }
    }
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
}
</style>
