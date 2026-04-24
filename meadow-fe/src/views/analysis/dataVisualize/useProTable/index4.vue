<template>
  <div class="dashboard-container">
    <!-- 时间选择按钮 -->
    <div class="time-selector">
      <!-- 月份选择 -->
      <el-popover placement="bottom-start" v-model:visible="showMonthSelector" trigger="manual">
        <template #reference>
          <el-button @click="showMonthSelector = !showMonthSelector">选择月份</el-button>
        </template>
        <el-select v-model="selectedMonth" placeholder="选择月份" @change="changeTimeRange('month')">
          <el-option
            v-for="month in 12"
            :key="month"
            :label="`${currentYear}-${month.toString().padStart(2, '0')}`"
            :value="month"
          />
        </el-select>
      </el-popover>
      <el-button @click="getMonth">查看月度</el-button>
      <el-button @click="getQuarter">查看季度</el-button>
      <el-button @click="getYear">查看年度</el-button>
      <div class="block">
        <span class="起止日期">选择日期</span>
        <el-date-picker
          v-model="value1"
          type="daterange"
          range-separator="To"
          start-placeholder="起始时间"
          end-placeholder="结束时间"
          size="default"
        />
      </div>

      <!-- 季度选择 -->
      <!-- <el-popover placement="bottom-start" v-model:visible="showQuarterSelector" trigger="manual">
        <template #reference>
          <el-button @click="showQuarterSelector = !showQuarterSelector">季</el-button>
        </template>
        <el-select v-model="selectedQuarter" placeholder="选择季度" @change="changeTimeRange('quarter')">
          <el-option v-for="quarter in 4" :key="quarter" :label="`${currentYear} 第 ${quarter} 季度`" :value="quarter" />
        </el-select>
      </el-popover> -->

      <!-- 年份选择 -->
      <!-- <el-popover placement="bottom-start" v-model:visible="showYearSelector" trigger="manual">
        <template #reference>
          <el-button @click="showYearSelector = !showYearSelector">年</el-button>
        </template>
        <el-select v-model="selectedYear" placeholder="选择年份" @change="changeTimeRange('year')">
          <el-option v-for="year in getYearRange()" :key="year" :label="year.toString()" :value="year" />
        </el-select>
      </el-popover> -->
    </div>

    <!-- 上半部分 -->
    <div class="top-section">
      <div class="chart-box left">
        <div ref="profitChart" style="height: 400px"></div>
      </div>

      <div class="table-box right">
        <el-table :data="filteredData" height="400" style="width: 100%" stripe border>
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
        <div ref="directExpenseChart" style="height: 300px"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, watch, nextTick } from "vue";
import * as echarts from "echarts";
import { getTest, getTestMonth, getTestQuarter } from "../api/manu";

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

// 图表 Ref
const profitChart = ref(null);
const sheepStockChart = ref(null);
const materialStockChart = ref(null);
const salesIncomeChart = ref(null);
const directExpenseChart = ref(null);

// 修改1：为每个图表创建独立的实例引用
const profitChartInstance = ref(null);
const sheepStockChartInstance = ref(null);
const materialStockChartInstance = ref(null);
const salesIncomeChartInstance = ref(null);
const directExpenseChartInstance = ref(null);

// 数据相关
const tableData = ref([]);
const filteredData = ref([]);
const currentYear = ref(new Date().getFullYear());

// 时间选择相关
const showMonthSelector = ref(false);
// const showQuarterSelector = ref(false);
// const showYearSelector = ref(false);
const selectedMonth = ref(new Date().getMonth() + 1);
// const selectedQuarter = ref(Math.floor((new Date().getMonth() + 3) / 3));
const selectedYear = ref(new Date().getFullYear());

// 图表配置生成器
const createTimeChartOption = (title, series) => ({
  color: colorPalette,
  title: {
    text: title,
    left: "center",
    textStyle: { fontSize: 16, color: "#333", fontWeight: "normal" }
  },
  tooltip: {
    trigger: "axis",
    axisPointer: { type: "cross", label: { backgroundColor: "#6a7985" } }
  },
  legend: {
    type: "scroll",
    top: 30,
    textStyle: { color: "#666", fontSize: 12 },
    pageTextStyle: { color: "#666" },
    pageIconColor: "#666",
    pageIconInactiveColor: "#bbb",
    padding: [0, 50]
  },
  grid: { top: 80, bottom: 100, containLabel: true },
  xAxis: {
    type: "time",
    boundaryGap: false,
    axisLabel: { formatter: "{yyyy}-{MM}-{dd}", color: "#666", fontSize: 12 },
    axisLine: { lineStyle: { color: "#999", width: 1 } },
    splitLine: { show: false }
  },
  yAxis: {
    type: "value",
    axisLabel: { color: "#666", fontSize: 12 },
    axisLine: { lineStyle: { color: "#999", width: 1 } },
    splitLine: { lineStyle: { color: "#eee", type: "dashed" } }
  },
  series: series.map(item => ({
    ...item,
    type: "line",
    smooth: true,
    showSymbol: false,
    lineStyle: { width: 2, cap: "round" },
    emphasis: { focus: "series", itemStyle: { borderWidth: 2 } }
  }))
});

// 修改2：调整初始化图表方法
const initChart = (chartRef, title, series) => {
  if (!chartRef.value) return null;
  const option = createTimeChartOption(title, series);
  const chart = echarts.init(chartRef.value);
  chart.setOption(option);
  return chart; // 返回图表实例
};
// 修改3：正确的时间数据处理
const parseDate = dateStr => {
  const [year, month, day] = dateStr.split("-");
  return new Date(year, month - 1, day);
};
// 时间范围过滤
const filterDataByTimeRange = (data, rangeType) => {
  let startDate, endDate;
  const year = selectedYear.value;

  switch (rangeType) {
    case "month":
      startDate = new Date(year, selectedMonth.value - 1, 1);
      endDate = new Date(year, selectedMonth.value, 0);
      break;
    case "quarter":
      const startMonth = (selectedQuarter.value - 1) * 3;
      startDate = new Date(year, startMonth, 1);
      endDate = new Date(year, startMonth + 3, 0);
      break;
    case "year":
      startDate = new Date(year, 0, 1);
      endDate = new Date(year, 11, 31);
      break;
    default:
      return data;
  }
  // 处理日期边界（包含一整天）
  startDate.setHours(0, 0, 0, 0);
  endDate.setHours(23, 59, 59, 999);
  return data.filter(item => {
    const itemDate = new Date(item.date);
    return itemDate >= startDate && itemDate <= endDate;
  });
};
// // 修改3：自动同步时间选择器状态
// watch(selectedYear, newVal => {
//   // 当年份变化时，重置季度和月份为有效值
//   selectedQuarter.value = Math.min(selectedQuarter.value, 4);
//   selectedMonth.value = Math.min(selectedMonth.value, 12);
// });

// 修改4：更新图表方法
const updateCharts = () => {
  const seriesData = filteredData.value;

  console.log(seriesData);

  // 销毁旧实例
  [
    profitChartInstance,
    sheepStockChartInstance,
    materialStockChartInstance,
    salesIncomeChartInstance,
    directExpenseChartInstance
  ].forEach(instance => {
    if (instance.value) {
      instance.value.dispose();
      instance.value = null;
    }
  });

  // 初始化新实例
  profitChartInstance.value = initChart(profitChart, "盈利趋势分析", [
    {
      name: "盈利",
      data: seriesData.map(i => [
        parseDate(i.date).getTime(), // 转换为时间戳
        i.profit
      ])
    }
  ]);

  sheepStockChartInstance.value = initChart(sheepStockChart, "草地库存资产趋势", [
    {
      name: "库存价值",
      data: seriesData.map(i => [parseDate(i.date).getTime(), i.sheep_asset])
    }
  ]);

  materialStockChartInstance.value = initChart(materialStockChart, "物料库存资产趋势", [
    {
      name: "库存价值",
      data: seriesData.map(i => [parseDate(i.date).getTime(), i.stock_asset])
    }
  ]);

  salesIncomeChartInstance.value = initChart(salesIncomeChart, "销售收入", [
    { name: "种苗", data: seriesData.map(i => [parseDate(i.date).getTime(), i.income_sales.breeding_sheep.value]) },
    { name: "生长期草地", data: seriesData.map(i => [parseDate(i.date).getTime(), i.income_sales.fattening_sheep.value]) },
    { name: "幼苗期地块", data: seriesData.map(i => [parseDate(i.date).getTime(), i.income_sales.lamb.value]) },
    { name: "其他草地记录", data: seriesData.map(i => [parseDate(i.date).getTime(), i.income_sales.other_sheep.value]) },
    { name: "草地残渣", data: seriesData.map(i => [parseDate(i.date).getTime(), i.income_byproducts.dung]) },
    { name: "采收产物", data: seriesData.map(i => [parseDate(i.date).getTime(), i.income_byproducts.wool]) },
    { name: "地表覆盖物", data: seriesData.map(i => [parseDate(i.date).getTime(), i.income_byproducts.skin]) },
    { name: "有机肥", data: seriesData.map(i => [parseDate(i.date).getTime(), i.income_byproducts.manure]) },
    { name: "草地投入", data: seriesData.map(i => [parseDate(i.date).getTime(), i.income_byproducts.feed]) },
    { name: "草地副产品", data: seriesData.map(i => [parseDate(i.date).getTime(), i.income_byproducts.producted]) },
    { name: "其他", data: seriesData.map(i => [parseDate(i.date).getTime(), i.income_byproducts.other]) }
  ]);

  directExpenseChartInstance.value = initChart(directExpenseChart, "费用支出", [
    { name: "种苗购买费", data: seriesData.map(i => [parseDate(i.date).getTime(), i.expense_direct.detail.buysheep]) },
    { name: "草地投入费", data: seriesData.map(i => [parseDate(i.date).getTime(), i.expense_direct.detail.forage]) },
    { name: "精准投入费", data: seriesData.map(i => [parseDate(i.date).getTime(), i.expense_direct.detail.fine_fodder]) },
    { name: "防护费", data: seriesData.map(i => [parseDate(i.date).getTime(), i.expense_direct.detail.vaccine]) },
    { name: "药物费", data: seriesData.map(i => [parseDate(i.date).getTime(), i.expense_direct.detail.medicine]) },
    { name: "人工费", data: seriesData.map(i => [parseDate(i.date).getTime(), i.expense_direct.detail.labor]) },
    { name: "直接总费用", data: seriesData.map(i => [parseDate(i.date).getTime(), i.expense_direct.total]) },
    { name: "间接总费用", data: seriesData.map(i => [parseDate(i.date).getTime(), i.expense_indirect.total]) }
  ]);
};

// 获取数据
const getData = async () => {
  try {
    const response = await getTest();
    tableData.value = response.data;
    filteredData.value = filterDataByTimeRange(tableData.value, "year");
  } catch (error) {
    console.error("获取数据失败:", error);
  }
};
// 获取数据
const getMonth = async () => {
  try {
    const response = await getTestMonth();
    tableData.value = response.data;
    filteredData.value = filterDataByTimeRange(tableData.value, "year");
    console.log(filteredData.value);
    updateCharts();
  } catch (error) {
    console.error("获取数据失败:", error);
  }
};
// 获取数据
const getQuarter = async () => {
  try {
    const response = await getTestQuarter();
    tableData.value = response.data;
    filteredData.value = filterDataByTimeRange(tableData.value, "year");
    updateCharts();
  } catch (error) {
    console.error("获取数据失败:", error);
  }
};
// 获取数据
const getYear = async () => {
  try {
    const response = await getTestYear();
    tableData.value = response.data;
    filteredData.value = filterDataByTimeRange(tableData.value, "year");
    updateCharts();
  } catch (error) {
    console.error("获取数据失败:", error);
  }
};

// 时间范围变化处理
const changeTimeRange = async rangeType => {
  await getData();
  filteredData.value = filterDataByTimeRange(tableData.value, rangeType);
  await nextTick();
  updateCharts();
};

// // 年份范围计算
// const getYearRange = () => {
//   if (tableData.value.length === 0) return [currentYear.value];
//   const years = new Set(tableData.value.map(item => new Date(item.date).getFullYear()));
//   return Array.from(years).sort((a, b) => b - a);
// };

// 生命周期
onMounted(async () => {
  await getData();
  // 初始化年份选择范围
  // selectedYear.value = Math.max(...getYearRange());
  // 设置默认显示范围为最近一个月
  const latestDate = new Date(tableData.value[tableData.value.length - 1].date);
  selectedMonth.value = latestDate.getMonth() + 1;
  // selectedYear.value = latestDate.getFullYear();
  changeTimeRange("month");
  window.addEventListener("resize", handleResize);
});

// 组件卸载部分修改为：
onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  [profitChart.value, sheepStockChart.value, materialStockChart.value, salesIncomeChart.value, directExpenseChart.value].forEach(
    chart => {
      if (chart && chart.chartInstance) {
        chart.chartInstance.dispose();
      }
    }
  );
});

// 窗口调整处理修改为：
const handleResize = () => {
  [profitChart.value, sheepStockChart.value, materialStockChart.value, salesIncomeChart.value, directExpenseChart.value].forEach(
    chart => {
      if (chart && chart.chartInstance) {
        chart.chartInstance.resize();
      }
    }
  );
};
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  padding: 20px;
  background: #f8f9fa;
}
.time-selector {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
.top-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
.bottom-section {
  display: flex;
  gap: 20px;
}
.chart-box,
.table-box,
.left-stock,
.right-stats {
  flex: 1;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgb(0 0 0 / 8%);
}
.left-stock,
.right-stats {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
