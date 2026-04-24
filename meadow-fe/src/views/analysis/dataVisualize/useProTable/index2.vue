<template>
  <div class="dashboard-container">
    <!-- 上半部分 -->
    <div class="top-section">
      <!-- 左侧图表 -->
      <div class="chart-box left">
        <div ref="profitChart" style="height: 400px"></div>
      </div>

      <!-- 右侧表格 -->
      <div class="table-box right">
        <el-table :data="tableData" height="400" style="width: 100%" stripe border>
          <el-table-column prop="date" label="日期" width="120" />
          <el-table-column prop="income" label="收入(元)" width="120" />
          <el-table-column prop="expense" label="支出(元)" width="120" />
          <el-table-column prop="assets" label="固定资产(元)" width="130" />
          <el-table-column prop="profit" label="盈利(元)" width="120" />
        </el-table>
      </div>
    </div>

    <!-- 下半部分 -->
    <div class="bottom-section">
      <!-- 左侧库存 -->
      <div class="left-stock">
        <div ref="sheepStockChart" style="height: 200px; margin-bottom: 20px"></div>
        <div ref="materialStockChart" style="height: 200px"></div>
      </div>

      <!-- 右侧统计 -->
      <div class="right-stats">
        <!-- 收入统计 -->
        <div class="income-stats">
          <div ref="salesIncomeChart" style="height: 250px"></div>
          <div ref="byproductIncomeChart" style="height: 250px"></div>
        </div>

        <!-- 支出统计 -->
        <div class="expense-stats">
          <div ref="directExpenseChart" style="height: 250px"></div>
          <div ref="indirectExpenseChart" style="height: 250px"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import * as echarts from "echarts";

// 图表Ref
const profitChart = ref(null);
const sheepStockChart = ref(null);
const materialStockChart = ref(null);
const salesIncomeChart = ref(null);
const byproductIncomeChart = ref(null);
const directExpenseChart = ref(null);
const indirectExpenseChart = ref(null);

// 模拟数据
const generateMockData = () => {
  const data = [];
  const startDate = new Date("2025-01-01");
  const today = new Date();

  while (startDate <= today) {
    const income = Math.floor(Math.random() * 10000) + 5000;
    const expense = Math.floor(Math.random() * 5000) + 2000;
    data.push({
      date: startDate.toISOString().split("T")[0],
      income,
      expense,
      assets: Math.floor(Math.random() * 100000),
      profit: income - expense
    });
    startDate.setDate(startDate.getDate() + 1);
  }
  return data;
};

const tableData = ref(generateMockData());

// 初始化图表
const initCharts = () => {
  // 盈利分析折线图
  const profitOption = {
    title: { text: "盈利趋势分析", left: "center" },
    tooltip: { trigger: "axis" },
    xAxis: {
      type: "category",
      data: tableData.value.map(item => item.date)
    },
    yAxis: { type: "value" },
    series: [
      {
        data: tableData.value.map(item => item.profit),
        type: "line",
        smooth: true,
        areaStyle: {}
      }
    ]
  };
  echarts.init(profitChart.value).setOption(profitOption);

  // 库存饼图
  const stockOption = {
    title: { text: "羊库存资产", left: "center" },
    tooltip: { trigger: "item" },
    series: [
      {
        type: "pie",
        radius: "50%",
        data: [
          { value: 1048, name: "成年羊" },
          { value: 735, name: "幼羊" },
          { value: 580, name: "种羊" }
        ]
      }
    ]
  };
  echarts.init(sheepStockChart.value).setOption(stockOption);

  // 其他图表初始化类似，根据需求配置不同option
  // 此处省略其他图表配置，实际开发中需要补充完整
};

onMounted(() => {
  initCharts();
  window.addEventListener("resize", () => {
    echarts.getInstanceByDom(profitChart.value)?.resize();
    // 其他图表也需要添加resize监听
  });
});
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}
.top-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
.chart-box {
  flex: 1;
  padding: 15px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgb(0 0 0 / 10%);
}
.table-box {
  flex: 1;
  padding: 15px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgb(0 0 0 / 10%);
}
.bottom-section {
  display: flex;
  gap: 20px;
}
.left-stock {
  flex: 0 0 35%;
  padding: 15px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgb(0 0 0 / 10%);
}
.right-stats {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 20px;
}
.income-stats,
.expense-stats {
  padding: 15px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgb(0 0 0 / 10%);
}
</style>
