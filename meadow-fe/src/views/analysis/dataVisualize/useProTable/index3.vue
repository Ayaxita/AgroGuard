<template>
  <div class="dashboard-container">
    <!-- 时间选择按钮 -->
    <div class="time-selector">
      <el-button @click="changeTimeRange('day')">日</el-button>
      <el-button @click="showMonthSelector = true">月</el-button>
      <el-button @click="showQuarterSelector = true">季</el-button>
      <el-button @click="showYearSelector = true">年</el-button>

      <!-- 月选择下拉菜单 -->
      <el-popover placement="bottom-start" v-model:visible="showMonthSelector" title="选择月份" trigger="manual">
        <template #content>
          <el-select v-model="selectedMonth" placeholder="选择月份" @change="handleMonthSelect">
            <el-option
              v-for="month in 12"
              :key="month"
              :label="`${currentYear}-${month.toString().padStart(2, '0')}`"
              :value="month"
            />
          </el-select>
        </template>
        <template #reference>
          <span></span>
        </template>
      </el-popover>

      <!-- 季选择下拉菜单 -->
      <el-popover placement="bottom-start" v-model:visible="showQuarterSelector" title="选择季度" trigger="manual">
        <template #content>
          <el-select v-model="selectedQuarter" placeholder="选择季度" @change="handleQuarterSelect">
            <el-option v-for="quarter in 4" :key="quarter" :label="`${currentYear} 第 ${quarter} 季度`" :value="quarter" />
          </el-select>
        </template>
        <template #reference>
          <span></span>
        </template>
      </el-popover>

      <!-- 年选择下拉菜单 -->
      <el-popover placement="bottom-start" v-model:visible="showYearSelector" title="选择年份" trigger="manual">
        <template #content>
          <el-select v-model="selectedYear" placeholder="选择年份" @change="handleYearSelect">
            <el-option v-for="year in getYearRange()" :key="year" :label="year.toString()" :value="year" />
          </el-select>
        </template>
        <template #reference>
          <span></span>
        </template>
      </el-popover>
    </div>
    <!-- 上半部分 -->
    <div class="top-section">
      <div class="chart-box left">
        <div ref="profitChart" style="height: 400px"></div>
      </div>

      <div class="table-box right">
        <el-table :data="tableData" height="400" style="width: 100%" stripe border>
          <el-table-column prop="date" label="记录日期" width="120" />
          <el-table-column prop="income_total" label="收入(元)" width="120" />
          <el-table-column prop="expense_total" label="支出(元)" width="120" />
          <el-table-column prop="sub_sheep_asset" label="Δ草地库存资产(元)" width="140" />
          <el-table-column prop="profit" label="盈利(元)" width="120" />
        </el-table>
      </div>
    </div>

    <!-- 下半部分 -->
    <div class="bottom-section">
      <div class="left-stock">
        <div ref="sheepStockChart" style="height: 300px; margin-bottom: 20px"></div>
        <div ref="materialStockChart" style="height: 300px"></div>
      </div>

      <div class="right-stats">
        <div ref="salesIncomeChart" style="height: 300px; margin-bottom: 20px"></div>
        <!-- <div ref="byproductIncomeChart" style="height: 300px; margin-bottom: 20px"></div> -->
        <div ref="directExpenseChart" style="height: 300px; margin-bottom: 20px"></div>
        <!-- <div ref="indirectExpenseChart" style="height: 300px"></div> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import * as echarts from "echarts";
import { getTest } from "../api/manu";
import axios from "axios"; // 引入 axios 库

// 图表Ref
const profitChart = ref(null);
const sheepStockChart = ref(null);
const materialStockChart = ref(null);
const salesIncomeChart = ref(null);
const byproductIncomeChart = ref(null);
const directExpenseChart = ref(null);
const indirectExpenseChart = ref(null);

// 颜色方案
const colorPalette = [
  "#5470C6",
  "#91CC75",
  "#FAC858",
  "#EE6666",
  "#73C0DE",
  "#3BA272",
  "#FC8452",
  "#9A60B4",
  "#EA7CCC",
  "#27727B",
  "#FADB61",
  "#6E7074"
];
const tableData = ref([]); // 初始化 tableData 为空数组
const currentTimeRange = ref("day"); // 当前选择的时间范围
const showMonthSelector = ref(false);
const showQuarterSelector = ref(false);
const showYearSelector = ref(false);
const selectedMonth = ref(new Date().getMonth() + 1);
const selectedQuarter = ref(Math.floor((new Date().getMonth() + 1) / 3) + 1);
const selectedYear = ref(new Date().getFullYear());
const currentYear = ref(new Date().getFullYear());

// 图表配置生成器
const createTimeChartOption = (title, series) => ({
  color: colorPalette,
  title: {
    text: title,
    left: "center",
    textStyle: {
      fontSize: 16,
      color: "#333",
      fontWeight: "normal"
    }
  },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "cross",
      label: {
        backgroundColor: "#6a7985"
      }
    }
  },
  legend: {
    type: "scroll",
    top: 30,
    textStyle: {
      color: "#666",
      fontSize: 12
    },
    pageTextStyle: {
      color: "#666"
    },
    pageIconColor: "#666",
    pageIconInactiveColor: "#bbb",
    padding: [0, 50]
  },
  grid: {
    top: 80,
    bottom: 100,
    containLabel: true
  },
  xAxis: {
    type: "time",
    boundaryGap: false,
    axisLabel: {
      formatter: "{yyyy}-{MM}-{dd}",
      color: "#666",
      fontSize: 12
    },
    axisLine: {
      lineStyle: {
        color: "#999",
        width: 1
      }
    },
    splitLine: {
      show: false
    }
  },
  yAxis: {
    type: "value",
    axisLabel: {
      color: "#666",
      fontSize: 12
    },
    axisLine: {
      lineStyle: {
        color: "#999",
        width: 1
      }
    },
    splitLine: {
      lineStyle: {
        color: "#eee",
        type: "dashed"
      }
    }
  },
  // dataZoom: [
  //   {
  //     type: "slider",
  //     show: true,
  //     xAxisIndex: 0,
  //     bottom: 25,
  //     height: 25,
  //     handleSize: "80%",
  //     filterMode: "none",
  //     labelFormatter: value => {
  //       const date = new Date(value);
  //       return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")}`;
  //     },
  //     borderColor: "#ddd",
  //     fillerColor: "rgba(84, 112, 198, 0.2)",
  //     textStyle: {
  //       color: "#666",
  //       fontSize: 12
  //     },
  //     brushSelect: false
  //   }
  // ],
  series: series.map(item => ({
    ...item,
    type: "line",
    smooth: true,
    showSymbol: false,
    lineStyle: {
      width: 2,
      cap: "round"
    },
    emphasis: {
      focus: "series",
      itemStyle: {
        borderWidth: 2
      }
    }
  }))
});

// 初始化图表
const initChart = (chartRef, title, series) => {
  const option = createTimeChartOption(title, series);
  option.legend.data = series.map(s => s.name);
  const chart = echarts.init(chartRef.value);
  chart.setOption(option);
  return chart;
};

// 初始化所有图表
let charts = [];
const initCharts = () => {
  const filteredData = filterDataByTimeRange(tableData.value, currentTimeRange.value);
  charts = [
    initChart(profitChart, "盈利趋势分析", [{ name: "盈利", data: tableData.value.map(i => [i.date, i.profit]) }]),

    initChart(sheepStockChart, "草地库存资产趋势", [
      { name: "库存价值", data: tableData.value.map(i => [i.date, i.sheep_asset]) }
    ]),

    initChart(materialStockChart, "物料库存资产趋势", [
      { name: "库存价值", data: tableData.value.map(i => [i.date, i.stock_asset]) }
    ]),

    initChart(salesIncomeChart, "销售收入", [
      { name: "种苗", data: tableData.value.map(i => [i.date, i.income_sales.breeding_sheep.value]) },
      { name: "生长期草地", data: tableData.value.map(i => [i.date, i.income_sales.fattening_sheep.value]) },
      { name: "幼苗期地块", data: tableData.value.map(i => [i.date, i.income_sales.lamb.value]) },
      { name: "其他草地记录", data: tableData.value.map(i => [i.date, i.income_sales.other_sheep.value]) },
      { name: "草地残渣", data: tableData.value.map(i => [i.date, i.income_byproducts.dung]) },
      { name: "采收产物", data: tableData.value.map(i => [i.date, i.income_byproducts.wool]) },
      { name: "地表覆盖物", data: tableData.value.map(i => [i.date, i.income_byproducts.skin]) },
      { name: "有机肥", data: tableData.value.map(i => [i.date, i.income_byproducts.manure]) },
      { name: "草地投入", data: tableData.value.map(i => [i.date, i.income_byproducts.feed]) },
      { name: "草地副产品", data: tableData.value.map(i => [i.date, i.income_byproducts.producted]) },
      { name: "其他", data: tableData.value.map(i => [i.date, i.income_byproducts.other]) }
    ]),

    // initChart(byproductIncomeChart, "草地副产品收入", [
    //   { name: "粪肥", data: tableData.value.map(i => [i.date, i.income_byproducts.dung]) },
    //   { name: "采收产物", data: tableData.value.map(i => [i.date, i.income_byproducts.wool]) },
    //   { name: "草皮", data: tableData.value.map(i => [i.date, i.income_byproducts.skin]) },
    //   { name: "有机肥", data: tableData.value.map(i => [i.date, i.income_byproducts.manure]) },
    //   { name: "饲料", data: tableData.value.map(i => [i.date, i.income_byproducts.feed]) },
    //   { name: "副产品", data: tableData.value.map(i => [i.date, i.income_byproducts.producted]) },
    //   { name: "其他", data: tableData.value.map(i => [i.date, i.income_byproducts.other]) }
    // ]),

    initChart(directExpenseChart, "费用支出", [
      { name: "种苗购买费", data: tableData.value.map(i => [i.date, i.expense_direct.detail.buysheep]) },
      { name: "草地投入费", data: tableData.value.map(i => [i.date, i.expense_direct.detail.forage]) },
      { name: "精准投入费", data: tableData.value.map(i => [i.date, i.expense_direct.detail.fine_fodder]) },
      { name: "防护费", data: tableData.value.map(i => [i.date, i.expense_direct.detail.vaccine]) },
      { name: "药物费", data: tableData.value.map(i => [i.date, i.expense_direct.detail.medicine]) },
      { name: "人工费", data: tableData.value.map(i => [i.date, i.expense_direct.detail.labor]) },
      { name: "直接总费用", data: tableData.value.map(i => [i.date, i.expense_direct.total]) },
      { name: "间接总费用", data: tableData.value.map(i => [i.date, i.expense_indirect.total]) }
    ])

    // initChart(indirectExpenseChart, "间接费用支出", [
    //   { name: "间接总费用", data: tableData.value.map(i => [i.date, i.expense_indirect.total]) }
    // ])
  ];
};
// 过滤数据
const filterDataByTimeRange = (data, timeRange) => {
  let startDate;
  let endDate;

  switch (timeRange) {
    case "day":
      startDate = new Date(currentYear.value, new Date().getMonth(), new Date().getDate());
      endDate = new Date(currentYear.value, new Date().getMonth(), new Date().getDate() + 1);
      break;
    case "month":
      startDate = new Date(currentYear.value, selectedMonth.value - 1, 1);
      endDate = new Date(currentYear.value, selectedMonth.value, 0);
      break;
    case "quarter":
      const startMonth = (selectedQuarter.value - 1) * 3;
      startDate = new Date(currentYear.value, startMonth, 1);
      endDate = new Date(currentYear.value, startMonth + 3, 0);
      break;
    case "year":
      startDate = new Date(selectedYear.value, 0, 1);
      endDate = new Date(selectedYear.value, 11, 31);
      break;
    default:
      startDate = new Date(currentYear.value, new Date().getMonth(), new Date().getDate());
      endDate = new Date(currentYear.value, new Date().getMonth(), new Date().getDate() + 1);
  }

  return data.filter(item => {
    const itemDate = new Date(item.date);
    return itemDate >= startDate && itemDate <= endDate;
  });
};

// 切换时间范围
const changeTimeRange = range => {
  currentTimeRange.value = range;
  if (range === "day") {
    showMonthSelector.value = false;
    showQuarterSelector.value = false;
    showYearSelector.value = false;
  }
  charts.forEach(chart => chart.dispose());
  initCharts();
};

// 处理月份选择
const handleMonthSelect = () => {
  currentTimeRange.value = "month";
  showMonthSelector.value = false;
  charts.forEach(chart => chart.dispose());
  initCharts();
};

// 处理季度选择
const handleQuarterSelect = () => {
  currentTimeRange.value = "quarter";
  showQuarterSelector.value = false;
  charts.forEach(chart => chart.dispose());
  initCharts();
};

// 处理年份选择
const handleYearSelect = () => {
  currentTimeRange.value = "year";
  showYearSelector.value = false;
  charts.forEach(chart => chart.dispose());
  initCharts();
};

// 获取年份范围
const getYearRange = computed(() => {
  const minYear = Math.min(...tableData.value.map(item => new Date(item.date).getFullYear()));
  const maxYear = Math.max(...tableData.value.map(item => new Date(item.date).getFullYear()));
  const years = [];
  for (let year = minYear; year <= maxYear; year++) {
    years.push(year);
  }
  return years;
});

// 窗口resize处理
const handleResize = () => {
  charts.forEach(chart => chart.resize());
};

// 调用后端接口获取数据
const getData = async () => {
  try {
    const response = await getTest(); // 替换为实际的后端接口地址
    tableData.value = response.data; // 使用从后端获取的数据更新 tableData
    initCharts(); // 重新初始化图表以使用新数据
  } catch (error) {
    console.error("获取数据失败:", error);
  }
};

onMounted(() => {
  getData(); // 调用后端接口获取数据
  window.addEventListener("resize", handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  charts.forEach(chart => chart.dispose());
  charts = [];
});
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  padding: 20px;
  background: #f8f9fa;
}
.time-selector {
  margin-bottom: 20px;
}
.top-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
.chart-box,
.table-box {
  flex: 1;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgb(0 0 0 / 8%);
  transition: box-shadow 0.2s ease;
}
.chart-box:hover,
.table-box:hover {
  box-shadow: 0 4px 16px rgb(0 0 0 / 12%);
}
.bottom-section {
  display: flex;
  gap: 20px;
}
.left-stock {
  display: flex;
  flex: 0 0 35%;
  flex-direction: column;
  gap: 20px;
}
.right-stats {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 20px;
}
.el-table {
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgb(0 0 0 / 8%);
}
.echarts {
  width: 100% !important;
  height: 100% !important;
}
</style>
